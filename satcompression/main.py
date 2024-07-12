from typing import Optional, Union

import numpy as np

from satcompression.image_compressor import ImageCompressor
from satcompression.reconstruct_node import ReconstructNode
from satcompression.utils import decode_image_data


def compress_image_data(
    image_data: np.array,
    iterations: int = 20000,
    detail_error_threshold: Union[int, float, None] = None,
) -> np.array:

    compressor = ImageCompressor(image_data)
    compressor.add_detail(
        max_iterations=iterations, detail_error_threshold=detail_error_threshold
    )
    return compressor.draw()


def compress_and_encode_image_data(
    image_data: np.array,
    iterations: Optional[int] = None,
    detail_error_threshold: float = None,
) -> bytes:
    compressor = ImageCompressor(image_data)
    compressor.add_detail(
        max_iterations=iterations, detail_error_threshold=detail_error_threshold
    )
    return compressor.encode_to_binary()


def reconstruct_quadtree(data: bytes, nchannels: int, dtype: str) -> ReconstructNode:
    width, height, subdivided_flags, colors = decode_image_data(
        compressed=data, nchannels=nchannels, dtype=dtype
    )

    # The ReconstructNode requires these to be reversed for performance reasons.
    subdivided_flags = list(reversed(subdivided_flags))
    colors = list(reversed(colors))
    return ReconstructNode((0, 0), (width, height), subdivided_flags, colors)


def reconstruct_image_data(
    data: bytes, dtype: str = "uint16", nchannels: int = 13
) -> np.array:

    tree = reconstruct_quadtree(data, dtype=dtype, nchannels=nchannels)
    width, height = tree.size
    image_data = np.zeros((nchannels, height, width), dtype=dtype)
    tree.draw(image_data)
    return image_data
