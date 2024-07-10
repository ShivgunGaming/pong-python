import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
POWERUP_SIZE = 20
POWERUP_DURATION = 5000  # milliseconds

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Pong")

# Create paddles
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create ball
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Ball movement
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

# Score variables
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Game states
start_screen = True
game_over = False
paused = False

# Power-up variables
powerup = None
powerup_active = False
powerup_start_time = 0

# AI function for the opponent paddle
def ai_opponent():
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += PADDLE_SPEED
    elif opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= PADDLE_SPEED
    # Ensure the paddle doesn't move out of the screen
    if opponent_paddle.top < 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom > HEIGHT:
        opponent_paddle.bottom = HEIGHT

# Start screen
def draw_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Enhanced Pong", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Game over screen
def draw_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Pause screen
def draw_pause_screen():
    pause_text = font.render("Paused", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    if start_screen:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen = False
        continue

    if game_over:
        draw_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_score = 0
                    opponent_score = 0
                    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
                    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    game_over = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if paused:
        draw_pause_screen()
        continue

    screen.fill(BLACK)

    # Move player paddle with mouse
    mouse_y = pygame.mouse.get_pos()[1]
    player_paddle.y = mouse_y - PADDLE_HEIGHT // 2
    # Ensure the paddle doesn't move out of the screen
    if player_paddle.top < 0:
        player_paddle.top = 0
    if player_paddle.bottom > HEIGHT:
        player_paddle.bottom = HEIGHT

    # Call AI function for opponent paddle
    ai_opponent()

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle):
        ball_speed_x = -ball_speed_x
        ball_speed_y += random.uniform(-1, 1)
    if ball.colliderect(opponent_paddle):
        ball_speed_x = -ball_speed_x
        ball_speed_y += random.uniform(-1, 1)

    # Ball out of bounds
    if ball.left <= 0:
        opponent_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
    elif ball.right >= WIDTH:
        player_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    # Draw paddles, ball, and scores
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 50))
    screen.blit(opponent_text, (WIDTH // 4 * 3, 50))

    # Power-up generation
    if not powerup and random.randint(1, 1000) <= 2:  # Randomly generate power-up
        powerup = pygame.Rect(random.randint(0, WIDTH - POWERUP_SIZE), random.randint(0, HEIGHT - POWERUP_SIZE), POWERUP_SIZE, POWERUP_SIZE)

    # Power-up collision
    if powerup and ball.colliderect(powerup):
        powerup_active = True
        powerup_start_time = pygame.time.get_ticks()
        PADDLE_SPEED *= 2  # Example power-up effect
        powerup = None

    # Power-up duration check
    if powerup_active and pygame.time.get_ticks() - powerup_start_time > POWERUP_DURATION:
        powerup_active = False
        PADDLE_SPEED //= 2  # Revert power-up effect

    # Draw power-up
    if powerup:
        pygame.draw.rect(screen, (0, 255, 0), powerup)

    # Update the display
    pygame.display.flip()

    # Check for game over
    if player_score >= 10 or opponent_score >= 10:
        game_over = True

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
