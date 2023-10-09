import pygame
import sys

pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))

# Set up assets
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ball_radius = 10

# Set up paddle properties
paddle_width = 10
paddle_height = 100
paddle_speed = 10

# Set up ball properties
ball_speed_x = 6
ball_speed_y = 6
ball_pos_x = width // 2
ball_pos_y = height // 2

# Set up paddle positions
player1_pos = (height - paddle_height) // 2
player2_pos = (height - paddle_height) // 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys
    keys = pygame.key.get_pressed()

    # Control player1 paddle
    if keys[pygame.K_w] and player1_pos > 0:
        player1_pos -= paddle_speed
    if keys[pygame.K_s] and player1_pos < height - paddle_height:
        player1_pos += paddle_speed

    # Control player2 paddle
    if keys[pygame.K_UP] and player2_pos > 0:
        player2_pos -= paddle_speed
    if keys[pygame.K_DOWN] and player2_pos < height - paddle_height:
        player2_pos += paddle_speed

    # Update ball position
    ball_pos_x += ball_speed_x
    ball_pos_y += ball_speed_y

    # Ball collision with walls
    if ball_pos_y - ball_radius <= 0 or ball_pos_y + ball_radius >= height:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball_pos_x - ball_radius <= paddle_width and player1_pos < ball_pos_y < player1_pos + paddle_height or \
            ball_pos_x + ball_radius >= width - paddle_width and player2_pos < ball_pos_y < player2_pos + paddle_height:
        ball_speed_x = -ball_speed_x

    # Check for score
    if ball_pos_x - ball_radius < 0 or ball_pos_x + ball_radius > width:
        ball_pos_x = width // 2
        ball_pos_y = height // 2
        ball_speed_x = -ball_speed_x

    # Clear screen
    window.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(window, WHITE, (0, player1_pos, paddle_width, paddle_height))
    pygame.draw.rect(window, WHITE, (width - paddle_width, player2_pos, paddle_width, paddle_height))

    # Draw ball
    pygame.draw.circle(window, WHITE, (ball_pos_x, ball_pos_y), ball_radius)

    # Refresh screen
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
