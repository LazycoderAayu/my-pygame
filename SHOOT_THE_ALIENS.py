import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load or initialize high score
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Use default font
base_font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_gradient_text(text, font, start_color, end_color, surface, x, y):
    text_surface = font.render(text, True, start_color)
    width, height = text_surface.get_size()
    gradient_surface = pygame.Surface((width, height)).convert_alpha()
    
    for i in range(height):
        color = (
            start_color[0] + (end_color[0] - start_color[0]) * i // height,
            start_color[1] + (end_color[1] - start_color[1]) * i // height,
            start_color[2] + (end_color[2] - start_color[2]) * i // height
        )
        pygame.draw.line(gradient_surface, color, (0, i), (width, i))

    text_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def game_over_screen():
    game_over_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)
        draw_gradient_text("Game Over", game_over_font, RED, BLUE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        
        mx, my = pygame.mouse.get_pos()

        button_restart = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)

        if button_restart.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
            return True  # Restart the game
        if button_quit.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()

        pygame.draw.rect(screen, GREEN, button_restart)
        pygame.draw.rect(screen, RED, button_quit)
        
        draw_gradient_text("Restart", button_font, BLACK, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)
        draw_gradient_text("Quit", button_font, BLACK, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 85)

        pygame.display.flip()
        clock.tick(15)

def main():
    global all_sprites, bullets, aliens, high_score

    # Group to hold all sprites
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create aliens
    for i in range(8):
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(-100, -40)
        alien = Alien(x, y)
        all_sprites.add(alien)
        aliens.add(alien)

    score = 0
    last_score_change = pygame.time.get_ticks()

    # Main game loop
    running = True
    while running:
        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        aliens.update()

        # Check for collisions
        if pygame.sprite.spritecollideany(player, aliens):
            running = False

        hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if hits:
            score += 10
            last_score_change = pygame.time.get_ticks()
            for hit in hits:
                x = random.randint(0, SCREEN_WIDTH - 50)
                y = random.randint(-100, -40)
                alien = Alien(x, y)
                all_sprites.add(alien)
                aliens.add(alien)

        # Update high score
        if score > high_score:
            high_score = score

        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display score
        current_time = pygame.time.get_ticks()
        if current_time - last_score_change < 200:  # Pulsing effect duration
            scale = 1.5
            color = (255, 215, 0)  # Gold color
        else:
            scale = 1.0
            color = WHITE
        scaled_font = pygame.font.Font(None, int(36 * scale))
        draw_gradient_text(f"Score: {score}", scaled_font, color, RED, screen, 70, 20)
        draw_gradient_text(f"High Score: {high_score}", base_font, WHITE, BLUE, screen, 150, 60)

        pygame.display.flip()

        # Maintain frame rate
        clock.tick(60)

    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

    return False  # Game over, not restarting

if __name__ == "__main__":
    restart_game = True
    while restart_game:
        restart_game = main()
        pygame.time.delay(1000)  # Delay before restarting to avoid immediate key events

