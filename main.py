# main.py
import pygame
import sys
from player import Player
from ball import Ball
from score import Score
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BALL_SPEED_X, BALL_SPEED_Y, CPU_SPEED, PLAYER_SPEED
from config import *



def draw_net(screen):
    net_height = 4
    net_width = 15
    gap = 10
    y = SCREEN_HEIGHT // 2 - net_height // 2

    for x in range(0, SCREEN_WIDTH, net_width + gap):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, net_width, net_height))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("NES Tennis Clone")
    clock = pygame.time.Clock()

    # Create player paddle
    paddle = Player(x=SCREEN_WIDTH//2 - 40, y=SCREEN_HEIGHT - 40, width=80, height=10, speed=PLAYER_SPEED)

    # Top CPU paddle
    cpu = Player(x=SCREEN_WIDTH // 2 - 40, y=40, width=80, height=10, speed=CPU_SPEED)

    # Create Ball
    ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
    # ball_held = True  # Waiting for serve
    serve_state = "ready"  # ready → toss → waiting_for_strike
    if serve_state == "ready":
        ball.x = paddle.rect.centerx
        ball.y = paddle.rect.top - ball.radius
        ball.z = 0
        ball.z_speed = 0



    # Create score:
    score = Score()



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if serve_state == "ready":
                        serve_state = "toss"
                        ball.z = 0
                        ball.z_speed = 8  # vertical toss
                    elif serve_state == "waiting_for_strike":
                        # Time to hit!
                        keys = pygame.key.get_pressed()
                        # Ensure the ball is at a high enough point to clear the net
                        ball.z = max(ball.z, 5)

                        if keys[pygame.K_z]:  # Flat
                            ball.z_speed = 2
                            ball.speed_y = -3
                            ball.speed_x = 3
                        elif keys[pygame.K_x]:  # Lob
                            ball.z_speed = 8
                            ball.speed_y = -2
                            ball.speed_x = 2
                        else:  # Default medium
                            ball.z_speed = 4
                            ball.speed_y = -2.5
                            ball.speed_x = 2.5

                        serve_state = "in_play"


        keys = pygame.key.get_pressed()
        paddle.move(keys)

        if serve_state == "toss":
            # Ball floats above player paddle
            ball.x = paddle.rect.centerx
            ball.y = paddle.rect.top - ball.radius
            ball.move()

            if ball.z >= 12:  # peak height for toss
                serve_state = "waiting_for_strike"


        # if serve_state == "waiting_for_strike":
        #     ball.move()

        if serve_state == "waiting_for_strike" and ball.z <= 0:
            # Serve failed
            score.point_to_cpu()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            serve_state = "ready"

        # # BALL MOVEMENT LOGIC:
        # if ball_held:
        #     ball.x = paddle.rect.centerx
        #     ball.y = paddle.rect.top - ball.radius
        # else:
        #     ball.move()

        if ball.bounce_count > 1:
            # Award point to opponent of last hitter (simplified for now)
            score.point_to_cpu()  # or .point_to_player() depending on last hit logic
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            # ball_held = True
            serve_state = "ready"

        if serve_state == "in_play":
            ball.move()
            # CPU movement
            if ball.x < cpu.rect.centerx:
                cpu.rect.x -= cpu.speed
            elif ball.x > cpu.rect.centerx:
                cpu.rect.x += cpu.speed

        #  # Basic CPU AI: move toward the ball's x-position
        # if not ball_held:
        #     if ball.x < cpu.rect.centerx:
        #         cpu.rect.x -= cpu.speed
        #     elif ball.x > cpu.rect.centerx:
        #         cpu.rect.x += cpu.speed


        # Keep CPU on screen
        cpu.rect.x = max(0, min(cpu.rect.x, SCREEN_WIDTH - cpu.rect.width))

        # CPU misses → point to player
        if ball.y + ball.radius < 0:
            print("Player scores!")
            score.point_to_player()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            ball_held = True
            serve_state = "ready"

        # Player misses → point to CPU
        elif ball.y - ball.radius > SCREEN_HEIGHT:
            print("CPU scores!")
            score.point_to_cpu()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            ball_held = True
            serve_state = "ready"

        else:
            # Then: check collisions
            ball.check_collision(paddle.rect)
            ball.check_collision(cpu.rect)


        screen.fill((0, 128, 0))  # Court background
        draw_net(screen)          # Center net
        paddle.draw(screen)
        cpu.draw(screen)
        ball.draw(screen)
        score.draw(screen)
        # if ball_held:
        if serve_state == "ready":
            font = pygame.font.SysFont("Courier", 24)
            label = font.render("Press SPACE to Serve", True, (255, 255, 255))
            label2 = font.render("SHIFT + SPACE to Lob Serve", True, (255, 255, 255))
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(label2, (SCREEN_WIDTH // 2 - label2.get_width() // 2, SCREEN_HEIGHT // 2 + label2.get_width() // 5))


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


