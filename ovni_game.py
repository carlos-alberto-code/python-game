import pygame
import random
import sys
import os
from sqlalchemy.orm import Mapped

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
SHIP_GREEN = (0, 255, 0)
GRASS_GREEN = (0, 100, 0)
STAR_COUNT = int(WIDTH * HEIGHT * 0.001)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Abduction Game")

# Create simple surfaces for UFO and cow if images don't load
def create_ufo_surface():
    surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    # Draw UFO shape
    pygame.draw.ellipse(surface, (112, 112, 112), (0, 20, 50, 15))  # Main body
    pygame.draw.ellipse(surface, (64, 64, 64), (10, 10, 30, 20))    # Dome
    # Lights
    pygame.draw.circle(surface, YELLOW, (12, 25), 3)
    pygame.draw.circle(surface, YELLOW, (25, 25), 3)
    pygame.draw.circle(surface, YELLOW, (38, 25), 3)
    return surface

def create_cow_surface():
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    # Draw cow shape
    pygame.draw.ellipse(surface, WHITE, (5, 15, 30, 20))  # Body
    pygame.draw.rect(surface, WHITE, (0, 10, 15, 15))     # Head
    # Spots
    pygame.draw.circle(surface, BLACK, (15, 20), 5)
    pygame.draw.circle(surface, BLACK, (25, 25), 6)
    # Legs
    pygame.draw.rect(surface, BLACK, (10, 30, 3, 10))
    pygame.draw.rect(surface, BLACK, (15, 30, 3, 10))
    pygame.draw.rect(surface, BLACK, (20, 30, 3, 10))
    pygame.draw.rect(surface, BLACK, (25, 30, 3, 10))
    return surface

# Try to load images, use simple shapes if failed
try:
    ovni = pygame.image.load(os.path.join("assets", "ovni.png"))
    ovni = pygame.transform.scale(ovni, (50, 50))
except:
    ovni = create_ufo_surface()

try:
    cow = pygame.image.load(os.path.join("assets", "vaca.png"))
    cow = pygame.transform.scale(cow, (40, 40))
except:
    cow = create_cow_surface()

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player (alien spaceship)
player_rect = pygame.Rect(WIDTH // 2 - 25, 10, 50, 50)
player_speed = 5

# List to store targets (animals)
targets = []

# Set initial score
score = 0

# Font for displaying text
font = pygame.font.Font(None, 36)

# Flag to track if spacebar is pressed
space_pressed = False

# List to store stars
stars = [{'x': random.randint(0, WIDTH),
          'y': random.randint(0, HEIGHT),
          'size': random.randint(1, 3),
          'color': LIGHT_BLUE} for _ in range(STAR_COUNT)]

# Grassy area at the bottom
grass_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)

# Level and Countdown Variables
current_level = 1
abduction_target = 10  # Initial target
countdown_timer = 60  # Initial countdown timer in seconds
current_score = 0  # Counter to track the score for current level

# Counter to control target appearances
target_spawn_counter = 0
TARGET_SPAWN_RATE = max(30, 120 - (current_level * 90))

# List of colors for each level
level_colors = [
    LIGHT_BLUE,
    ORANGE,
    RED,
    YELLOW,
    GRAY,
    (0, 255, 0),  # Green
    (255, 0, 255),  # Purple
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Indigo
]

def show_text_on_screen(screen, text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def start_screen(screen):
    screen.fill(BLACK)
    intro_text = [
        "Welcome, Alien Abductor!",
        "You're behind on your weekly quota of abductions.",
        "Help the alien catch up by abducting targets on Earth!",
        "",
        "----------------------------------------------------------------------------------------------",
        "Move the UFO with ARROWS and",
        "press SPACE to abduct cows with the track bean.",
        "----------------------------------------------------------------------------------------------",
        "",
        "Press any key to start the game...",
        "",
    ]
    y_position = HEIGHT // 4
    for line in intro_text:
        show_text_on_screen(screen, line, 30, y_position)
        y_position += 30

    pygame.display.flip()
    wait_for_key()

def game_over_screen(screen):
    screen.fill(BLACK)
    show_text_on_screen(screen, "Game Over", 50, HEIGHT // 3)
    show_text_on_screen(screen, f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def victory_screen(screen):
    screen.fill(BLACK)
    show_text_on_screen(screen, "Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(screen, f"You've completed all levels with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def main():
    global score, current_score, current_level, countdown_timer, abduction_target, space_pressed, target_spawn_counter

    # Show start screen
    start_screen(screen)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_pressed = False

        keys = pygame.key.get_pressed()

        # Move the player
        player_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
        player_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

        # Keep player within screen boundaries
        player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
        player_rect.y = max(0, min(player_rect.y, HEIGHT - player_rect.height))

        # Spawn new targets
        target_spawn_counter += 1
        if target_spawn_counter >= TARGET_SPAWN_RATE:
            target_rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT - 50, 50, 50)
            targets.append(target_rect)
            target_spawn_counter = 0

        # Update star animation
        for star in stars:
            star['size'] += 0.05
            if star['size'] > 3:
                star['size'] = 1
            star['color'] = level_colors[current_level - 1]

        # Clear screen and draw elements
        screen.fill(BLACK)

        # Draw stars
        for star in stars:
            pygame.draw.circle(screen, star['color'], (int(star['x']), int(star['y'])), int(star['size']))

        # Draw grass
        pygame.draw.rect(screen, GRASS_GREEN, grass_rect)

        # Draw player and targets
        screen.blit(ovni, player_rect)
        for target in targets:
            screen.blit(cow, target)

        # Draw tractor beam when spacebar is pressed
        if space_pressed:
            tractor_beam_rect = pygame.Rect(player_rect.centerx - 2, player_rect.centery, 4, HEIGHT - player_rect.centery)
            pygame.draw.line(screen, YELLOW, (player_rect.centerx, player_rect.centery),
                           (player_rect.centerx, HEIGHT), 2)

            # Check for collisions
            for target in targets[:]:
                if tractor_beam_rect.colliderect(target):
                    pygame.draw.line(screen, YELLOW, (player_rect.centerx, player_rect.centery),
                                   (player_rect.centerx, target.bottom), 2)
                    pygame.draw.rect(screen, RED, target)
                    targets.remove(target)
                    current_score += 1
                    score += 1

        # Draw UI elements
        info_line_y = 10
        info_spacing = 75

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(10, info_line_y))
        pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
        screen.blit(score_text, score_rect)

        # Draw level
        level_text = font.render(f"Level: {current_level}", True, WHITE)
        level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
        screen.blit(level_text, level_rect)

        # Draw timer
        timer_text = font.render(f"Time: {int(countdown_timer)}", True, WHITE)
        timer_rect = timer_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, RED, timer_rect.inflate(10, 5))
        screen.blit(timer_text, timer_rect)

        # Draw abduction target
        targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
        targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))
        pygame.draw.rect(screen, GRAY, targets_rect.inflate(10, 5))
        screen.blit(targets_text, targets_rect)

        # Update display
        pygame.display.flip()

        # Cap frame rate
        clock.tick(FPS)

        # Countdown Timer Logic
        countdown_timer -= 1 / FPS
        if countdown_timer <= 0:
            if current_score < abduction_target:
                game_over_screen(screen)
                running = False
            else:
                current_level += 1
                if current_level <= 10:
                    current_score = 0
                    abduction_target = 10 * current_level
                    countdown_timer = 60

        # Check level completion
        if current_score >= abduction_target:
            current_level += 1
            if current_level <= 10:
                current_score = 0
                abduction_target = 10 * current_level
                countdown_timer = 60
            else:
                victory_screen(screen)
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
