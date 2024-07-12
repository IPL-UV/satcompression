import numpy as np

from satcompression.quadtree import QuadTreeNode


class CompressNode(QuadTreeNode):
    """A class for compressing an image using a QuadTree structure."""

    def __init__(self, position: tuple[int, int], image_data: np.array):
        channels, height, width = image_data.shape
        super().__init__(position, (width, height))

        self.image_data = image_data

        # Compute the detail as the sum of the standard deviation of each channel
        # weighted by the number of pixels in this region.

        # normalize the image data
        self.detail = np.median(
            np.std(image_data, axis=(1, 2))
        )  # * self.image_data.size
        self.color = np.mean(image_data, axis=(1, 2))

    def _create_child_node(
        self, position: tuple[int, int], size: tuple[int, int]
    ) -> "CompressNode":
        """Creates a child node with the given position and size.

        Args:
            position (tuple[int, int]): The position of the child node.
            size (tuple[int, int]): The size of the child node.

        Returns:
            CompressNode: A new child node.
        """

        # Create a new child node with the given position and size.
        width, height = size
        child_x, child_y = position
        own_x, own_y = self.position

        # Compute the start position of the child node in the image data.
        start_x = child_x - own_x
        start_y = child_y - own_y

        return CompressNode(
            position=position,
            image_data=self.image_data[
                ..., start_y : start_y + height, start_x : start_x + width
            ],
        )

    def subdivide(self) -> tuple:
        """Splits the current node into 4 child nodes if possible.

        Returns:
            tuple: The child nodes or an empty list if the node
                cannot be subdivided.
        """
        # Subdivide the node.
        nodes = super().subdivide()

        # Memory of the image is no longer needed as the relevant areas
        # have been passed on to the child nodes.
        self.image_data = None

        return nodes

    def extract_data(self, subdivided_flags: list[bool], colors: list[tuple]) -> None:
        subdivided_flags.append(self.is_subdivided)

        if self.is_subdivided:
            self.bottom_left_node.extract_data(subdivided_flags, colors)
            self.bottom_right_node.extract_data(subdivided_flags, colors)
            self.top_left_node.extract_data(subdivided_flags, colors)
            self.top_right_node.extract_data(subdivided_flags, colors)
        else:
            colors.append(self.color)
