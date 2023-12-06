# Need to install ( pip install pygame )
import pygame

# Standard python library
import random

# To initialize and configure pygame
pygame.init()

# --------------- Configs ---------------

WIDTH, HEIGHT = 600, 400
BALL_SPEED = 7
PADDLE_SPEED = 7

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

score1 = 0
score2 = 0

player_name1 = "A"
player_name2 = "B"

ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)

paddle1 = pygame.Rect(50, HEIGHT // 2 - 50, 10, 100)
paddle2 = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 50, 10, 100)

# Movement of the ball in the x-axis
ball_dx = BALL_SPEED * random.choice((1, -1))

# Movement of the ball in the y-axis
ball_dy = BALL_SPEED * random.choice((1, -1))

# Position of the paddles on the y-axis
paddle1_dy = 0
paddle2_dy = 0

ball_in_motion = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")


# --------------- Functions ---------------

# Title for players' scores
def draw_scores():
    font = pygame.font.Font(None, 36)

    score1_text = font.render(f"{player_name1}: {score1}", True, GREEN)
    score2_text = font.render(f"{player_name2}: {score2}", True, GREEN)

    screen.blit(score1_text, (10, 10))
    screen.blit(score2_text, (WIDTH - score2_text.get_width() - 10, 10))


# Function to check ball collision
def check_collision(ball, paddle):
    if ball.colliderect(paddle):
        return True
    return False


# Location of the ball after the goal
def reset_ball_position():
    side = random.choice(("left", "right"))
    if side == "left":
        ball.x = 10 + 50 + 10
        ball_dx = BALL_SPEED

    else:
        ball.x = WIDTH - 50 - 10 - 30 - 10
        ball_dx = - BALL_SPEED
    ball.y = HEIGHT // 2 - 15
    return ball_dx

# --------------- Game loop ---------------


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Paddle 2 movement settings
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2_dy = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                paddle2_dy = PADDLE_SPEED
            elif event.key == pygame.K_SPACE:
                ball_in_motion = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle2_dy = 0

    # Paddle 1 movement settings
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_dy = -PADDLE_SPEED
    elif keys[pygame.K_s]:
        paddle1_dy = PADDLE_SPEED
    else:
        paddle1_dy = 0

    # Ball movement settings
    if ball_in_motion:
        ball.x += ball_dx
        ball.y += ball_dy

    # Checking the collision of the ball on the upper and lower walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # Checking the collision of the ball with the paddles
    if check_collision(ball, paddle1) or check_collision(ball, paddle2):
        ball_dx *= -1

    # Counting goals and checking the continuation of the game
    if ball.left <= 0:
        score2 += 1
        if score2 == 5:
            running = False
        else:
            ball_dx = reset_ball_position()
            ball_in_motion = False

    elif ball.right >= WIDTH:
        score1 += 1
        if score1 == 5:
            running = False
        else:
            ball_dx = reset_ball_position()
            ball_in_motion = False

    # Controlling the movement of paddles
    paddle1.y += paddle1_dy
    paddle2.y += paddle2_dy

    if paddle1.top <= 0:
        paddle1.top = 0
    if paddle1.bottom >= HEIGHT:
        paddle1.bottom = HEIGHT

    if paddle2.top <= 0:
        paddle2.top = 0
    if paddle2.bottom >= HEIGHT:
        paddle2.bottom = HEIGHT

    screen.fill(BLACK)

    # Drawing ball and paddles
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, RED, ball)

    # Show scores on the screen
    draw_scores()

    # Show game changes on the screen
    pygame.display.flip()

    # Game speed control
    pygame.time.delay(30)

# Exit the game
pygame.quit()
