import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
POWER_UP_SIZE = 20
POWER_UP_DURATION = 300  # Duration in frames

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

# Power-up variables
power_up_active = False
power_up_timer = 0
power_up_type = None
power_ups = []

# Game states
start_screen = True
game_over = False

# AI function for the opponent paddle
def ai_opponent():
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += PADDLE_SPEED
    elif opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= PADDLE_SPEED

# Power-up functions
def spawn_power_up():
    power_up_type = random.choice(["speed", "slow", "extra_point"])
    power_up = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), POWER_UP_SIZE, POWER_UP_SIZE)
    power_ups.append((power_up, power_up_type))

def apply_power_up(power_up_type, player_scored):
    global BALL_SPEED_X, BALL_SPEED_Y, PADDLE_SPEED
    if power_up_type == "speed":
        BALL_SPEED_X *= 1.2
        BALL_SPEED_Y *= 1.2
    elif power_up_type == "slow":
        PADDLE_SPEED = 2 if player_scored else PADDLE_SPEED
    elif power_up_type == "extra_point":
        if player_scored:
            global player_score
            player_score += 1
        else:
            global opponent_score
            opponent_score += 1

def reset_power_up():
    global BALL_SPEED_X, BALL_SPEED_Y, PADDLE_SPEED
    BALL_SPEED_X = 5
    BALL_SPEED_Y = 5
    PADDLE_SPEED = 5

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

    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player paddle with mouse
    mouse_y = pygame.mouse.get_pos()[1]
    player_paddle.y = mouse_y - PADDLE_HEIGHT // 2

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
        reset_power_up()
    elif ball.right >= WIDTH:
        player_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
        reset_power_up()

    # Power-up logic
    if random.randint(1, 1000) > 995 and not power_up_active:
        spawn_power_up()
    for power_up, power_up_type in power_ups:
        pygame.draw.rect(screen, BLUE if power_up_type == "speed" else RED, power_up)
        if ball.colliderect(power_up):
            apply_power_up(power_up_type, ball_speed_x > 0)
            power_up_active = True
            power_up_timer = POWER_UP_DURATION
            power_ups.remove((power_up, power_up_type))
    if power_up_active:
        power_up_timer -= 1
        if power_up_timer <= 0:
            reset_power_up()
            power_up_active = False

    # Draw paddles, ball, power-ups, and scores
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
