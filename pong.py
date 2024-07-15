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

# Power-ups
power_up_active = False
power_up = pygame.Rect(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, 20)
power_up_effect_time = 5000  # 5 seconds
power_up_end_time = 0

# Game states
start_screen = True
game_over = False
paused = False

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

# Activate power-up
def activate_power_up():
    global power_up_active, power_up_end_time
    power_up_active = True
    power_up_end_time = pygame.time.get_ticks() + power_up_effect_time
    if random.choice([True, False]):
        # Increase player paddle speed
        global PADDLE_SPEED
        PADDLE_SPEED = 10
    else:
        # Decrease opponent paddle speed
        global opponent_paddle_speed
        opponent_paddle_speed = 2

# Deactivate power-up
def deactivate_power_up():
    global power_up_active, PADDLE_SPEED, opponent_paddle_speed
    power_up_active = False
    PADDLE_SPEED = 5
    opponent_paddle_speed = PADDLE_SPEED

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

    # Move player paddle with keyboard
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # Mobile touch control
    if pygame.mouse.get_pressed()[0]:
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
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
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

    # Draw power-up
    if not power_up_active and random.randint(0, 1000) < 5:
        power_up = pygame.Rect(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, 20)
    pygame.draw.rect(screen, (0, 255, 0), power_up)
    if ball.colliderect(power_up):
        activate_power_up()
        power_up.x = -100  # Move off-screen

    # Deactivate power-up after time
    if power_up_active and pygame.time.get_ticks() > power_up_end_time:
        deactivate_power_up()

    # Draw paddles, ball, and scores
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 50))
    screen.blit(opponent_text, (WIDTH // 4 * 3, 50))

    # Update the display
    pygame.display.flip()

    # Check for game over
    if player_score >= 10 or opponent_score >= 10:
        game_over = True

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
