import math
from typing import Optional, Union

import numpy as np
from sortedcontainers import SortedListWithKey
from tqdm import trange

from satcompression.compress_node import CompressNode
from satcompression.utils import check_node, encode_image_data


class ImageCompressor:
    """Helper class that manages the CompressNodes and allows you to incrementally add detail."""

    def __init__(self, image_data: np.array):
        self.areas = SortedListWithKey(key=lambda node: node.detail)
        self._image_shape = image_data.shape
        self._data_type = image_data.dtype
        self.channels, self.height, self.width = self._image_shape
        self.root_node = CompressNode((0, 0), image_data)
        self.areas.add(self.root_node)

    def add_detail(
        self, max_iterations: Optional[int], detail_error_threshold: Union[int, float]
    ):
        """Adds detail to the image by subdividing the nodes
        with the most detail.

        Args:
            max_iterations (int, optional): The maximum number
                of iterations to subdivide nodes. Defaults to 1.
        """
        if max_iterations is None:
            max_iterations = 2_000_000_000_000

        # Subdivide the nodes with the most detail.
        for i in trange(max_iterations, leave=False):
            if not self.areas:
                break

            node_with_most_detail = self.areas.pop()
            for node in node_with_most_detail.subdivide():
                if node.detail >= detail_error_threshold:
                    self.areas.add(node)

            if i > max_iterations:
                break

    def draw(self):
        new_image_data = np.zeros(self._image_shape, dtype=self._data_type)
        self.root_node.draw(new_image_data)
        return new_image_data

    def extract_data(self):
        subdivided_flags = []
        colors = []

        self.root_node.extract_data(subdivided_flags, colors)

        return subdivided_flags, colors

    def encode_to_binary(self) -> bytes:
        subdivided_flags, colors = self.extract_data()
        colors = [color.astype(self._data_type) for color in colors]
        return encode_image_data(
            width=self.width,
            height=self.height,
            subdivided_flags=subdivided_flags,
            colors=colors,
            dtype=self._data_type,
        )


def quadtree_mtf(
    image_data: np.array,
    ground_sampling_distance: float,
    detail_error_threshold: float = 25,
):
    """Obtain the quadtree compressed image data.

    Args:
        image_data (np.array): The image data to compress.
        ground_sampling_distance (float): The ground sampling distance of the image.
        detail_error_threshold (float, optional): The detail error threshold. Defaults to 25.
    """

    # Obtain the image quadtree compressed
    compressor = ImageCompressor(image_data)
    compressor.add_detail(
        max_iterations=None, detail_error_threshold=detail_error_threshold
    )

    # Check the amount of node in each level
    graph = compressor.root_node
    max_level = int(math.log2(max(compressor.width, compressor.height)))
    values = [1] + [check_node(graph, level=i) for i in range(0, max_level)]
    perfect = [4**i for i in range(0, max_level + 1)]
    graph_mtf = [values[i] / perfect[i] for i in range(0, max_level + 1)]

    # Generate the x-axis
    x_axis = []
    for i in reversed(range(max_level + 1)):
        gsd_meters = ground_sampling_distance * 2**i
        if gsd_meters > 1000:
            x_axis.append(f"{gsd_meters / 1000} km")
        else:
            x_axis.append(f"{gsd_meters} m")

    return graph_mtf, x_axis
