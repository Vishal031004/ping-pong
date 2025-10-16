import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.best_of = 3          # Default winning target
        self.game_over = False    # Game state flag

    def handle_input(self):
        if self.game_over:
            return  # No movement while menu is shown

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return  # Freeze updates while menu is visible

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Check if game over
        if self.player_score >= self.best_of or self.ai_score >= self.best_of:
            self.game_over = True

        # Update AI paddle movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        screen.fill((0, 0, 0))

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # If game over, show replay menu overlay
        if self.game_over:
            self.show_game_over_menu(screen)

    def show_game_over_menu(self, screen):
        lines = [
            "GAME OVER!",
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit",
        ]
        for i, line in enumerate(lines):
            text = self.font.render(line, True, WHITE)
            rect = text.get_rect(center=(self.width//2, self.height//2 - 80 + i*40))
            screen.blit(text, rect)

    def handle_game_over_input(self, event):
        """Handle key presses during the game over menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.reset_game(best_of=3)
            elif event.key == pygame.K_5:
                self.reset_game(best_of=5)
            elif event.key == pygame.K_7:
                self.reset_game(best_of=7)
            elif event.key == pygame.K_ESCAPE:
                return False  # signal to quit
        return True

    def reset_game(self, best_of=None):
        """Resets scores, ball, and sets new winning target."""
        if best_of:
            self.best_of = best_of
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
