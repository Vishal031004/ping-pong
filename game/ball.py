import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        """Move the ball and detect wall bounces"""
        self.x += self.velocity_x
        self.y += self.velocity_y

        wall_bounce = False
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_bounce = True
        return wall_bounce

    def check_collision(self, player, ai):
        """Check collision with paddles and return True if hit"""
        hit_paddle = False
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1
            hit_paddle = True
        return hit_paddle

    def reset(self):
        """Reset ball to center and reverse direction"""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
