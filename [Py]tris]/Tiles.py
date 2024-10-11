import numpy as np

from Detect_Collisions import Collisions

class Tiles:

    # Initialize tile with shape, color, position, and rotation
    def __init__(self, collision_detector, shape, color, pos_x=5, pos_y=0, rotation=0):
        self._shape = shape
        self._rotation = rotation
        self._color = color
        self._position = np.array([pos_x, pos_y])
        self._collision_detector = collision_detector
        self._is_locked = False # Indicates if the tile is locked in place

    # Render the tile on the board
    def render(self, board):
        matrix = self.get_coordinates()
        board.draw_tile(matrix, self._color)

    # Get the coordinates of the tile's current position and rotation
    def get_coordinates(self):
        return self._shape.get_matrix_with_offset(self._rotation, self._position)

    # Return the color of the tile
    def get_color(self):
        return self._color

    # Attempt to rotate the tile in the specified direction
    def rotate(self, direction):
        new_rotation = np.abs(np.mod(self._rotation + direction,  self._shape.rot_Count))
        new_matrix = self._shape.get_matrix_with_offset(new_rotation, self._position)
        collision = self._collision_detector.check(new_matrix, 0, 0)
        if collision is Collisions.BOTTOM:
            self._is_locked = True # Lock the tile if it hits the bottom
        if collision is Collisions.NONE:
            self._rotation = new_rotation # Update rotation if no collision

    # Attempt to move the tile by (dx, dy)
    def move(self, dx, dy):
        next_pos = self._position + np.array([dx, dy])
        new_matrix = self._shape.get_matrix_with_offset(self._rotation, next_pos)
        collision = self._collision_detector.check(new_matrix, dx, dy)

        if collision == Collisions.BOTTOM:
            self._is_locked = True # Lock the tile if it hits the bottom

        if collision is Collisions.NONE:
            self._position = next_pos # Update position if no collision

        return self._is_locked # Return tile lock status