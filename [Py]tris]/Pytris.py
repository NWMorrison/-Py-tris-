import pygame.display
import json  # To save and load the leaderboard
import pygame.mixer  # For sound effects
from Board import Board


class Pytris:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._screen = pygame.display.set_mode((720, 920))
        pygame.display.set_caption("Pytris")
        self._clock = pygame.time.Clock()
        self._running = True
        self._speed = 120  # Initial speed (lower means faster)
        self._board = Board(self._screen)
        self.level = 1
        self.rows_cleared = 0
        self._score_font = pygame.font.SysFont('Arial', 30)
        self.leaderboard_file = "leaderboard.json"

        # Load music
        self.music_file = ''  # Replace with the path to your  music 
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.set_volume(0.5)

    def start_screen(self):
        """Display the start screen with buttons for Start and Exit."""
        self._screen.fill("black")
        font = pygame.font.SysFont('Arial', 50)
        button_font = pygame.font.SysFont('Arial', 40)

        # Render leaderboard
        leaderboard = self.load_leaderboard()
        font_small = pygame.font.SysFont('Arial', 30)
        leaderboard_text = font_small.render("Leaderboard:", True, (255, 255, 255))
        self._screen.blit(leaderboard_text, (150, 50))

        for idx, entry in enumerate(leaderboard[:5], start=1):
            text = f"{idx}. {entry['name']} - {entry['score']}"
            score_text = font_small.render(text, True, (255, 255, 255))
            self._screen.blit(score_text, (150, 80 + idx * 30))

        # Render buttons
        start_button = pygame.Rect(260, 400, 200, 60)
        exit_button = pygame.Rect(260, 500, 200, 60)

        pygame.draw.rect(self._screen, (0, 128, 0), start_button)
        pygame.draw.rect(self._screen, (128, 0, 0), exit_button)

        start_text = button_font.render("Start", True, (255, 255, 255))
        exit_text = button_font.render("Exit", True, (255, 255, 255))
        self._screen.blit(start_text, (310, 410))
        self._screen.blit(exit_text, (310, 510))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        waiting = False
                    if exit_button.collidepoint(event.pos):
                        self._running = False
                        waiting = False

    def run(self):
        """Main game loop."""
        self.start_screen()
        player_name = self.get_player_name()
        if not player_name:
            return  # Exit if no name is entered
        pygame.mixer.music.play(loops=-1)  # Play Tetris music in a loop
        counter = 0
        while self._running:
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
                if self._board.game_over:  # Check for game over
                    self.display_game_over()
                    self._running = False
                    break
                self.rows_cleared += self._board._ground.expire_rows()  # Count rows cleared
                self.check_level_up()
                counter = 1
                self._screen.fill("black")
                self._board.draw()

            pygame.display.flip()
            counter += 1
            self._clock.tick(120)
            score_text = self._score_font.render(
                f"Score: {self._board.score}  Level: {self.level}", True, (255, 255, 255)
            )
            self._screen.blit(score_text, (500, 150))
        self.save_score(player_name)
        pygame.mixer.music.stop()  # Stop music when game exits
        pygame.quit()

    def display_game_over(self):
        """Display a game-over message."""
        pygame.mixer.music.stop()
        self._screen.fill("black")
        font = pygame.font.SysFont('Arial', 50)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        score_text = font.render(f"Your Score: {self._board.score}", True, (255, 255, 255))
        self._screen.blit(game_over_text, (200, 300))
        self._screen.blit(score_text, (200, 400))
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds


    def check_level_up(self):
        """Increase the level based on rows cleared and adjust speed."""
        if self.rows_cleared >= self.level * 10:
            self.level += 1
            self._speed = max(10, self._speed - 10)  # Increase speed, but not below a limit

    def load_leaderboard(self):
        """Load leaderboard data from file."""
        try:
            with open(self.leaderboard_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_score(self, player_name):
        """Save the current score to the leaderboard."""
        leaderboard = self.load_leaderboard()
        leaderboard.append({"name": player_name, "score": self._board.score})
        leaderboard.sort(key=lambda x: x['score'], reverse=True)

        with open(self.leaderboard_file, "w") as f:
            json.dump(leaderboard, f)

    def get_player_name(self):
        """Display an input box to get the player's name."""
        input_box = pygame.Rect(260, 400, 200, 60)
        font = pygame.font.SysFont('Arial', 40)
        name = ""
        while True:
            self._screen.fill("black")
            prompt_text = font.render("Enter your name:", True, (255, 255, 255))
            self._screen.blit(prompt_text, (200, 300))

            pygame.draw.rect(self._screen, (255, 255, 255), input_box, 2)
            name_surface = font.render(name, True, (255, 255, 255))
            self._screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
