""" Import necessary modules for game logic, graphics, and random number generation """
import random
import numpy as np
import pygame

""" Imports From Other Python Files"""
import Shapes
from Detect_Collisions import DetectCollisions
from Ground import Ground
from Tiles import Tiles

"""Represents the game board, handling tile placement, movement, and collisions."""
class Board:
    """
    Initializes the Board object with the given screen dimensions.
        Args:
            screen: The Pygame screen object.
            height: The desired height of the board (default: 24).
            width: The desired width of the board (default: 10).
    """
    def __init__(self, screen, height=24, width=10):
        self.height = height
        self.width = width
        self._screen = screen
        self._ground = Ground(width, height)
        self._collision_detector = DetectCollisions(self, self._ground)
        self._matrix = np.zeros([width, height], dtype=int)
        self._current_tile = None
        self.score = 0
        self._colours = Shapes.block_Colors()
        self._shapes = Shapes.generating_Blocks()
        self.game_over = False

    """Draws the entire game board, including the ground and current tiles."""
    def draw(self):
        block_size = 35  # Set the size of the grid block
        x_offset = 100
        y_offset = 50
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(x_offset + x * block_size, y_offset + y * block_size, block_size, block_size)
                pygame.draw.rect(self._screen, self._colours[self._matrix[x, y]], rect,
                                 1 if self._matrix[x, y] == 0 else 0)


    def update(self, on_timer=True):
        """
        Updates the game state, including tile movement, collision detection, and scoring.
            Args:
                on_timer: Indicates whether the update is
                triggered by a timer (default: True).
        """
        if self._current_tile is None:
            self.create_tile()
        if on_timer:
            self.drop_tile()

        self._matrix[:, :] = 0
        self.draw_tile(self._current_tile)
        self.draw_ground(self._ground)

    def drop_tile(self):
        """
            Attempts to move the current tile down by one unit.
            If the tile is locked (cannot move further),
            merges it with the ground and updates the score.
        """
        is_locked = self._current_tile.move(0, 1)
        if is_locked:
            """Check if the tile locked at the top of the board"""
            if any(pos[1] == 0 for pos in self._current_tile.get_coordinates()):
                self.game_over = True  # Signal game over
                return
            self._ground.merge(self._current_tile)
            self.score += self._ground.expire_rows()
            self.create_tile()

    """Creates a new tile with a random shape and color."""
    def create_tile(self):
        self._current_tile = Tiles(self._collision_detector, self.get_shape(), self.get_colour(), random.randint(0, 6))

    """Returns a random shape from the available shapes."""
    def get_shape(self):
        return self._shapes[random.randint(0, len(self._shapes) - 1)]

    """Returns a random color from the available colors."""
    def get_colour(self):
        return random.randint(1, len(self._colours) - 1)

    def draw_tile(self, tile):
        """
        Draws the given tile onto the matrix.
            Args:
                tile: The tile to be drawn.
        """
        matrix = tile.get_coordinates()
        for pos in matrix:
            if pos[1] < self.height:
                self._matrix[pos[0], pos[1]] = tile.get_color()

    def draw_ground(self, ground):
        """
        Updates the matrix with the ground's matrix to represent the ground's presence.
            Args:
                ground: The ground object.
        """
        self._matrix = np.maximum(self._matrix, ground.get_matrix())

    """Rotates the current tile clockwise."""
    def on_key_up(self):
        self._current_tile.rotate(1)
        self.draw()

    """Rotates the current tile clockwise."""
    def on_key_down(self):
        self._current_tile.move(0, 1)
        self.draw()

    """Moves the current tile left."""
    def on_key_left(self):
        self._current_tile.move(-1, 0)
        self.draw()

    """Moves the current tile right."""
    def on_key_right(self):
        self._current_tile.move(1, 0)
        self.draw()

    """Moves the current tile down until it locks in place."""
    def slam_tile(self):
        while not self._current_tile.move(0, 1):
            pass
        self._ground.merge(self._current_tile)
        self.score = self.score + self._ground.expire_rows()
        self.create_tile()
        self.draw()

