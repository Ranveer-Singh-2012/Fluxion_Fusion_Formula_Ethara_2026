import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Formula Ethara Racing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 102, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load or create track
track_rect = pygame.Rect(50, 50, WIDTH-100, HEIGHT-100)  # Simple rectangle track

# Car class
class Car:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.max_speed = 6
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.turn_speed = 4
        self.color = color
        self.width = 40
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lap = 0
        self.lap_started = False

    def draw(self, surface):
        rotated_car = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rotated_car.fill(self.color)
        rotated_car = pygame.transform.rotate(rotated_car, -self.angle)
        rect = rotated_car.get_rect(center=(self.x, self.y))
        surface.blit(rotated_car, rect.topleft)

    def update(self):
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed += self.acceleration
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed -= self.acceleration
        else:
            # Friction
            if self.speed > 0:
                self.speed -= self.deceleration
            elif self.speed < 0:
                self.speed += self.deceleration

        # Clamp speed
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed/2:
            self.speed = -self.max_speed/2

        # Turning
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += self.turn_speed * (self.speed / self.max_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= self.turn_speed * (self.speed / self.max_speed)

        # Speed boost
        if keys[pygame.K_SPACE]:
            self.speed = self.max_speed + 2

        # Update position
        rad = math.radians(self.angle)
        self.x += -self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)

        # Track boundaries collision
        if not track_rect.collidepoint(self.x, self.y):
            self.speed = -self.speed/2  # Bounce back slightly

        # Update rect
        self.rect.topleft = (self.x - self.width//2, self.y - self.height//2)

# Create player car
player_car = Car(WIDTH//2, HEIGHT-100, RED)

# Lap line
lap_line = pygame.Rect(WIDTH//2 - 50, 50, 100, 5)

font = pygame.font.SysFont(None, 30)

def draw_track():
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, track_rect)
    pygame.draw.rect(screen, WHITE, track_rect, 5)
    pygame.draw.rect(screen, GREEN, lap_line)

def draw_info():
    lap_text = font.render(f"Lap: {player_car.lap}", True, WHITE)
    screen.blit(lap_text, (10, 10))

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update car
    player_car.update()

    # Check lap
    if lap_line.collidepoint(player_car.x, player_car.y):
        if not player_car.lap_started:
            player_car.lap += 1
            player_car.lap_started = True
    else:
        player_car.lap_started = False

    # Draw everything
    draw_track()
    player_car.draw(screen)
    draw_info()

    pygame.display.flip()

pygame.quit()
sys.exit()
