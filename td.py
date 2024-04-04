import pygame
import sys

# Initialize pygame
pygame.init()

# Define window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tower Defense")

# Define Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = 10
        self.range = 100

    def attack(self, enemies):
        for enemy in enemies:
            distance = ((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                        self.rect.centery - enemy.rect.centery) ** 2) ** 0.5
            if distance <= self.range:
                enemy.take_damage(self.damage)

# Define Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, path, target):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = path[0]
        self.path = path
        self.path_index = 0
        self.health = 100
        self.speed = 2
        self.target = target

    def move(self):
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 0:
                if distance <= self.speed:
                    self.rect.center = (target_x, target_y)
                    self.path_index += 1
                else:
                    self.rect.x += (dx / distance) * self.speed
                    self.rect.y += (dy / distance) * self.speed
            else:
                self.path_index += 1
        else:
            dx = self.target[0] - self.rect.centerx
            dy = self.target[1] - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 0:
                if distance <= self.speed:
                    self.rect.center = self.target
                else:
                    self.rect.x += (dx / distance) * self.speed
                    self.rect.y += (dy / distance) * self.speed

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# Create path for enemies to follow
path = [(100, 100), (200, 100), (300, 200), (400, 200), (500, 300), (600, 300), (700, 400)]
target = (100, 100)  # Tower position

# Create group for enemies
enemies = pygame.sprite.Group()
for _ in range(2):
    enemy = Enemy(path, target)
    enemies.add(enemy)

for enemy in enemies:
    enemy.rect.center = path[0]

# Create tower
tower = Tower(100, 100)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        tower.attack(enemies)

    enemies.update()

    screen.fill(WHITE)

    # Draw path
    for i in range(len(path) - 1):
        pygame.draw.line(screen, RED, path[i], path[i + 1], 2)

    enemies.draw(screen)
    pygame.draw.circle(screen, RED, (tower.rect.centerx, tower.rect.centery), 30)  # Draw tower

    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
