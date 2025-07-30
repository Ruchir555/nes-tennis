# ball.py

import pygame

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off left and right walls
        if self.x - self.radius <= 0 or self.x + self.radius >= 640:
            self.speed_x *= -1

        # Bounce off top
        if self.y - self.radius <= 0:
            self.speed_y *= -1

    def check_collision(self, paddle_rect):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)
        # if ball_rect.colliderect(paddle_rect):
        #     self.speed_y *= -1
        #     self.y = paddle_rect.top - self.radius  # Prevent sticking

        if ball_rect.colliderect(paddle_rect):
            if self.speed_y > 0 and self.y < paddle_rect.centery:
                # Ball is moving down, must be player paddle
                self.speed_y *= -1
                self.y = paddle_rect.top - self.radius
            elif self.speed_y < 0 and self.y > paddle_rect.centery:
                # Ball is moving up, must be CPU paddle
                self.speed_y *= -1
                self.y = paddle_rect.bottom + self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
