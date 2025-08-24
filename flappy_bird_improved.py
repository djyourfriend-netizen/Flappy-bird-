import pygame, sys, random

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
JUMP = -6.5

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

# Game state
GAME_ACTIVE = True
GAME_OVER = False

# Bird settings
bird_movement = 0
bird = pygame.Rect(50, HEIGHT//2, 30, 30)

# Pipe settings
pipe_width = 70
pipe_gap = 150
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

score = 0
high_score = 0

def create_pipe():
    height = random.randint(100, 400)
    bottom = pygame.Rect(WIDTH, height, pipe_width, HEIGHT-height)
    top = pygame.Rect(WIDTH, 0, pipe_width, height - pipe_gap)
    return bottom, top

def draw_pipes(pipes):
    for p in pipes:
        pygame.draw.rect(screen, GREEN, p)
        # Add pipe borders for better visibility
        pygame.draw.rect(screen, BLACK, p, 2)

def check_collision(pipes):
    for p in pipes:
        if bird.colliderect(p):
            return False
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return False
    return True

def reset_game():
    global bird_movement, bird, pipes, score, GAME_ACTIVE, GAME_OVER
    bird_movement = 0
    bird.y = HEIGHT//2
    pipes.clear()
    score = 0
    GAME_ACTIVE = True
    GAME_OVER = False

def draw_game_over():
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = big_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
    
    # Final score
    final_score_text = font.render(f"Final Score: {int(score)}", True, WHITE)
    screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 - 30))
    
    # High score
    if score > high_score:
        high_score_text = font.render(f"New High Score!", True, YELLOW)
    else:
        high_score_text = font.render(f"High Score: {int(high_score)}", True, YELLOW)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 10))
    
    # Restart instruction
    restart_text = font.render("Press SPACE to restart", True, WHITE)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

def draw_bird():
    # Draw bird with better visuals
    pygame.draw.rect(screen, YELLOW, bird)
    pygame.draw.rect(screen, BLACK, bird, 2)
    
    # Add bird eye
    eye_rect = pygame.Rect(bird.x + 20, bird.y + 5, 8, 8)
    pygame.draw.circle(screen, BLACK, (eye_rect.centerx, eye_rect.centery), 4)
    pygame.draw.circle(screen, WHITE, (eye_rect.centerx, eye_rect.centery), 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if GAME_ACTIVE:
                    bird_movement = JUMP
                elif GAME_OVER:
                    reset_game()
        if event.type == SPAWNPIPE and GAME_ACTIVE:
            pipes.extend(create_pipe())

    if GAME_ACTIVE:
        # Bird physics
        bird_movement += GRAVITY
        bird.y += int(bird_movement)

        # Move pipes
        pipes = [p.move(-3, 0) for p in pipes if p.right > 0]

        # Score (fixed to count only once per pipe pair)
        for i in range(0, len(pipes), 2):
            if i < len(pipes) and pipes[i].centerx <= bird.centerx < pipes[i].centerx + 3:
                score += 1

        # Draw
        screen.fill(BLUE)
        draw_bird()
        draw_pipes(pipes)

        # Display score
        text = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(text, (10, 10))

        # Collision check
        if not check_collision(pipes):
            GAME_ACTIVE = False
            GAME_OVER = True
            if score > high_score:
                high_score = score

    elif GAME_OVER:
        # Draw the game state
        screen.fill(BLUE)
        draw_bird()
        draw_pipes(pipes)
        draw_game_over()

    pygame.display.update()
    clock.tick(FPS)

print("Game Over! Final Score:", int(score))
if score > high_score:
    print("New High Score!")
else:
    print(f"High Score: {int(high_score)}")
    