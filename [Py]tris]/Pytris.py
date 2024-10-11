import pygame.display

# This class handles the game board logic
from Board import Board

""" This class represents the main game loop and manages the overall Pytris experience. """
class Pytris:


    def __init__(self):
        """
            Initializes Pygame, creates the display window, clock, and game board objects.
        """
        pygame.init()
        self._screen = pygame.display.set_mode((720, 920))
        pygame.display.set_caption("Pytris")
        self._clock = pygame.time.Clock()
        self._running = True
        self._speed = 120 # Number of frames per second for automatic piece movement
        self._board = Board(self._screen) # Create the game board instance
        pygame.font.init()
        self._score_font = pygame.font.SysFont('Arial', 30)
        self.run() # Starts The Game Loop

    def run(self):
        """
            The main game loop that handles user input, game logic updates, rendering, and score display.
        """
        counter = 0
        while self._running:
            """ 
                Handles key presses for game controls
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._board.on_key_up()
                    if event.key == pygame.K_DOWN:
                        self._board.on_key_down()
                    if event.key == pygame.K_LEFT:
                        self._board.on_key_left()
                    if event.key == pygame.K_RIGHT:
                        self._board.on_key_right()
                    if event.key == pygame.K_SPACE:
                        self._board.slam_tile()
                    self._screen.fill("black")
                    self._board.update(False)
                    self._board.draw()

            if counter % self._speed == 0:
                self._board.update()
                counter = 1
                self._screen.fill("black")
                self._board.draw()

            # Updates the display
            pygame.display.flip()
            counter += 1
            self._clock.tick(120)
            text_surface = self._score_font.render('Pytris Score: ' + str(self._board.score), False, (255, 255, 255))
            self._screen.blit(text_surface, (500, 150))
        pygame.quit()