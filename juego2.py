import pygame
import random

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Estados del juego
START = 0
PLAYING = 1
GAME_OVER = 2

# Clase para representar el personaje controlado por el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Limitar el movimiento dentro de la pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Clase para representar los obstáculos en el aire
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.player = player

    def update(self):
        speed = random.randint(3, 6)
        if self.rect.x > self.player.rect.x:
            self.rect.x -= speed
        else:
            self.rect.x += speed
        if self.rect.y > self.player.rect.y:
            self.rect.y -= speed
        else:
            self.rect.y += speed

# Inicialización de Pygame
pygame.init()

# Creación de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desplazamiento y Esquivar Objetos")

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Fuente de texto
font = pygame.font.Font(None, 36)

# Estado inicial del juego
game_state = START

# Puntuación
score = 0

# Grupos de sprites
all_sprites = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (game_state == START or game_state == GAME_OVER):
                # Reiniciar el juego
                all_sprites.empty()
                obstacle_group.empty()
                player = Player()
                all_sprites.add(player)
                game_state = PLAYING
                score = 0

    if game_state == START:
        # Pantalla de inicio
        screen.fill(BLACK)
        start_text = font.render("Presiona ESPACIO para comenzar", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        pygame.display.flip()

    elif game_state == PLAYING:
        # Actualización y dibujado del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualización de los sprites
        all_sprites.update()

        # Colisión entre el personaje y los obstáculos
        collisions = pygame.sprite.spritecollide(player, obstacle_group, False)
        if collisions:
            game_state = GAME_OVER

        # Generar nuevos obstáculos
        if random.randint(0, 100) < 5:
            obstacle = Obstacle(player)
            all_sprites.add(obstacle)
            obstacle_group.add(obstacle)

        # Dibujado de la pantalla
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Dibujar la puntuación en la pantalla
        score_text = font.render("Puntuación: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Control de la velocidad de actualización
        clock.tick(60)

    elif game_state == GAME_OVER:
        # Pantalla de juego terminado
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        score_text = font.render("Puntuación: {}".format(score), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + score_text.get_height() // 2))
        restart_text = font.render("Presiona ESPACIO para reiniciar", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + restart_text.get_height() // 2 + 50))
        pygame.display.flip()

# Cierre de Pygame
pygame.quit()
