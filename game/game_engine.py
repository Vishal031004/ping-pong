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

        # Initialize mixer first
        pygame.mixer.init()

        # Load sounds
        self.sound_paddle = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("assets/score.wav")

        # Game objects
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Scores & font
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Game settings
        self.best_of = 3
        self.game_over = False

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        prev_vx, prev_vy = self.ball.velocity_x, self.ball.velocity_y
        prev_x = self.ball.x

        self.ball.move()

        # Detect wall bounce sound
        if self.ball.velocity_y != prev_vy:
            self.sound_wall.play()

        self.ball.check_collision(self.player, self.ai)

        # Detect paddle hit sound
        if self.ball.velocity_x != prev_vx:
            self.sound_paddle.play()

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()

        # Check for game over
        if self.player_score >= self.best_of or self.ai_score >= self.best_of:
            self.game_over = True

        # AI tracks ball
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        screen.fill((0, 0, 0))

        # Draw paddles, ball, center line
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Game over menu
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.reset_game(best_of=3)
            elif event.key == pygame.K_5:
                self.reset_game(best_of=5)
            elif event.key == pygame.K_7:
                self.reset_game(best_of=7)
            elif event.key == pygame.K_ESCAPE:
                return False
        return True

    def reset_game(self, best_of=None):
        if best_of:
            self.best_of = best_of
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
