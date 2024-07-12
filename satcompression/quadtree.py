import numpy as np


class QuadTreeNode:
    """
    Base quad tree data structure that handles the positioning,
    subdivision and rendering of nodes.
    """

    def __init__(self, position: tuple, size: tuple):
        # The position and size of the node.
        self.position = position
        self.size = size

        # The color of the node.
        self.color = None

        # A flag to indicate if the node is subdivided.
        self.is_subdivided = False

        # The child nodes of the current node.
        self.bottom_left_node = None
        self.bottom_right_node = None
        self.top_left_node = None
        self.top_right_node = None

    def _create_child_node(self, position: tuple, size: tuple) -> "QuadTreeNode":
        """Creates a new quad tree node with the given position and size.

        Args:
            position (tuple): The position of the node.
            size (tuple): The size of the node.

        Returns:
            QuadTreeNode: A new quad tree node.
        """
        return QuadTreeNode(position, size)

    def subdivide(self) -> tuple:
        """Splits the current quad into 4 child quads if this is possible.

        Returns:
            Child quads or None or an empty list if it
            cannot be further subdivided.
        """

        # If the node is already subdivided, return an empty list.
        if self.is_subdivided:
            return []

        # Save the current position and size of the node.
        width, height = self.size
        x, y = self.position

        # If the width or height is less than or equal to 1, return an empty list.
        if width <= 1 or height <= 1:
            return []

        # Create the child nodes.
        self.is_subdivided = True
        split_width = width // 2
        split_height = height // 2

        # Create the child nodes.
        self.bottom_left_node: QuadTreeNode = self._create_child_node(
            position=(x, y), size=(split_width, split_height)
        )

        self.bottom_right_node: QuadTreeNode = self._create_child_node(
            position=(x + split_width, y), size=(width - split_width, split_height)
        )

        self.top_left_node: QuadTreeNode = self._create_child_node(
            position=(x, y + split_height), size=(split_width, height - split_height)
        )

        self.top_right_node: QuadTreeNode = self._create_child_node(
            position=(x + split_width, y + split_height),
            size=(width - split_width, height - split_height),
        )

        # return the child nodes.
        return (
            self.bottom_left_node,
            self.bottom_right_node,
            self.top_left_node,
            self.top_right_node,
        )

    def draw(self, image_data: np.array) -> None:
        """Copies the color of the node to the image data.

        Args:
            image_data (np.array): The image data to draw on.
        """

        # If the node is subdivided, draw the child nodes.
        if self.is_subdivided:
            self.bottom_left_node.draw(image_data)
            self.bottom_right_node.draw(image_data)
            self.top_left_node.draw(image_data)
            self.top_right_node.draw(image_data)
        else:
            self.draw_self(image_data)

    def draw_self(self, image_data: np.array):
        """Draws the color of the node on the image data.

        Args:
            image_data (np.array): The image data to draw on.
        """

        # A color of None indicates that the node has not been assigned a color.
        if self.color is None:
            return

        start_x, start_y = self.position
        width, height = self.size
        end_x = start_x + width
        end_y = start_y + height
        image_data[..., start_y:end_y, start_x:end_x] = np.array(self.color).reshape(
            -1, 1, 1
        )

    def use_average_leaf_color(self):
        """Sets the color of the node to the average color of its child nodes.
        If the node is not subdivided, the color is not changed.

        Args:
            image_data (np.array): The image data to draw on
        """

        if not self.is_subdivided:
            return

        self.bottom_left_node.use_average_leaf_color()
        self.bottom_right_node.use_average_leaf_color()
        self.top_left_node.use_average_leaf_color()
        self.top_right_node.use_average_leaf_color()

        self.color = tuple(
            np.mean(
                [
                    self.bottom_left_node.color,
                    self.bottom_right_node.color,
                    self.top_left_node.color,
                    self.top_right_node.color,
                ],
                axis=0,
            )
        )
