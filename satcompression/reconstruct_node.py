from satcompression.quadtree import QuadTreeNode


class ReconstructNode(QuadTreeNode):
    """QuadTree node for reconstructing a compressed image."""

    def __init__(self, position, size, subdivided_flags: list, colors: list):
        super().__init__(position, size)

        # Hint:
        # subdivided_flags and colors must be reversed!
        # (Improves performance, as popping a value off the back is faster than removing from the front)

        self._subdivided_flags = subdivided_flags
        self._colors = colors

        is_subdivided = subdivided_flags.pop()
        if is_subdivided:
            self.subdivide()
        else:
            self.color = colors.pop()

    def _create_child_node(self, position, size):
        return ReconstructNode(position, size, self._subdivided_flags, self._colors)
