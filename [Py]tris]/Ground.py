import numpy as np

"""Represents a game board."""
class Ground:
    """Initializes a new Ground object with the specified width and height."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.zeros([width, height], dtype=int)
        self.coordinates = list()

    """Merges a given tile onto the Ground."""
    def merge(self, tile):
        coordinates = tile.get_coordinates()
        for position in coordinates:
            if (self .matrix[position[0], position[1]] != 0) or (position[0] >= self .width) \
                    or (position[1] >= self.height):
                print("ERROR")
            self .matrix[position[0], [position[1]]] = tile.get_color()
            self .coordinates.append(position)

    """Returns the matrix representing the game board."""
    def get_matrix(self):
        return self .matrix

    """Returns the coordinates list containing the positions of non-zero tiles."""
    def get_coordinates(self):
        return self .coordinates

    """Removes any completed rows from the Ground."""
    def expire_rows(self):
        row_count = 0
        for h in np.arange(1, self.height - 1):
            while np.all(self.matrix[:, self.height - h] != 0):
                self.cascade(self.height - h)
                row_count = row_count + 1
        if row_count != 0:
            self.recompute_coordinates()
        return row_count

    """Shifts all rows above the specified up_to row down by one position."""
    def cascade(self, up_to):
        rows = np.arange(0, up_to)[::-1]
        for h in rows:
            self.matrix[:, h + 1] = self .matrix[:, h]
        self.matrix[:, 0] = 0

    """Clears the existing coordinates list and recomputes the coordinates of non-zero tiles."""
    def recompute_coordinates(self):
        self .coordinates.clear()
        for x in np.arange(len(self .matrix)):
            for y in np.arange(len(self .matrix[x])):
                if self .matrix[x][y] != 0:
                    self .coordinates.append(np.array([x, y]))