from enum import Enum
import numpy as np

"""Defines types of collisions that can occur."""
class Collisions(Enum):
    NONE = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    ROTATION = 4

"""Handles collision detection."""
class DetectCollisions:


    def __init__(self, board, ground):
        """Initializes the class with the game board and ground objects."""
        self.board = board
        self.ground = ground

    def check(self, coordinates_of_tile, dx, dy):
        """
        Checks for collisions between the tile and the board or ground.
            Args:
                coordinates_of_tile: The coordinates of the tile.
                dx: The horizontal displacement of the tile.
                dy: The vertical displacement of the tile.
            Returns:
                The type of collision that occurred, or Collisions.
                NONE if no collision occurred.
        """
        collisions = self.check_board(coordinates_of_tile)
        if collisions != Collisions.NONE:
            return collisions
        return self.check_ground(coordinates_of_tile, dx, dy)

    def check_board(self, coordinates_of_shape):
        """
        Checks for collisions with the game board's boundaries.
            Args:
                coordinates_of_shape: The coordinates of the shape.

            Returns:
                The type of collision that occurred, or Collisions.
                NONE if no collision occurred.
        """
        if np.max(coordinates_of_shape[:, 1]) >= self.board.height:
            return Collisions.BOTTOM

        if np.max(coordinates_of_shape[:, 0]) >= self.board.width:
            return Collisions.LEFT

        if np.min(coordinates_of_shape[:, 0]) < 0:
            return Collisions.RIGHT

        return Collisions.NONE

    def check_ground(self, coordinates_of_tile, dx, dy):
        """
        Checks for collisions with the ground or other tiles.
            Args:
                coordinates_of_tile: The coordinates of the tile.
                dx: The horizontal displacement of the tile.
                dy: The vertical displacement of the tile.
            Returns:
                The type of collision that occurred, or Collisions.
                NONE if no collision occurred.
        """
        coordinates_of_ground = self.ground.get_coordinates()
        for ground_coordinates1 in coordinates_of_ground:
            for tile_coordinates1 in coordinates_of_tile:
                if np.all(ground_coordinates1 == tile_coordinates1):
                    if dy > 0:
                        return Collisions.BOTTOM
                    if dx > 0:
                        return Collisions.RIGHT
                    if dx < 0:
                        return Collisions.LEFT
                    if dx == 0 and dy == 0:
                        return Collisions.ROTATION
                    return Collisions.NONE
        return Collisions.NONE

