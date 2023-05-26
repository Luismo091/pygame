import pygame
import random
import math

# Dimensiones de la pantalla
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

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
        original_image = pygame.image.load("Hai.png")  # Cargar la imagen del jugador desde un archivo
        scaled_width = 50  # Ancho deseado para la imagen redimensionada
        scaled_height = 80  # Alto deseado para la imagen redimensionada
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.shoot_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Limitar el movimiento dentro de la pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Control del disparo
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullet_group.add(bullet)
            self.shoot_cooldown = 20

# Clase para representar las balas disparadas por el jugador
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 5])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Clase para representar los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        original_image = pygame.image.load("BICHO.png")  # Cargar la imagen del enemigo desde un archivo
        scaled_width = 50  # Ancho deseado para la imagen redimensionada
        scaled_height = 50  # Alto deseado para la imagen redimensionada
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.player = player
        self.speed = random.randint(3, 6)
        self.follow_player = True
        self.follow_timer = 300

    def update(self):
        if self.follow_player:
            self.follow_timer -= 1
            if self.follow_timer <= 0:
                self.follow_player = False
            else:
                dx = self.player.rect.x - self.rect.x
                dy = self.player.rect.y - self.rect.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if dist != 0:
                    self.rect.x += int(self.speed * dx / dist)
                    self.rect.y += int(self.speed * dy / dist)
        else:
            self.rect.x -= self.speed

        if self.rect.colliderect(self.player.rect):
            game_state = GAME_OVER

# Clase para representar los power-ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_up_type):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.power_up_type = power_up_type
        if self.power_up_type == "slow":
            self.image.fill((0, 0, 255))  # Power-up que ralentiza a los enemigos
        elif self.power_up_type == "rapid":
            self.image.fill((255, 0, 255))  # Power-up que dispara múltiples balas
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

# Clase para representar las balas disparadas automáticamente en 4 direcciones
class AutoBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Inicialización de Pygame
pygame.init()

# Creación de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desplazamiento, Esquivar Objetos y Power-ups")

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
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
power_up_group = pygame.sprite.Group()

# Variables para controlar los power-ups
power_up_timer = 0
slow_enemies = False
rapid_shoot = False

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == START:
        # Pantalla de inicio
        screen.fill(BLACK)
        start_text = font.render("Presiona ESPACIO para comenzar", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Reiniciar el juego
            all_sprites.empty()
            bullet_group.empty()
            enemy_group.empty()
            power_up_group.empty()
            player = Player()
            all_sprites.add(player)
            game_state = PLAYING
            score = 0

    elif game_state == PLAYING:
        # Actualización y dibujado del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualización de los sprites
        all_sprites.update()

        # Colisión entre las balas y los enemigos
        bullet_enemy_collisions = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
        for bullet, enemies in bullet_enemy_collisions.items():
            score += len(enemies)
            for _ in range(len(enemies)):
                # Generar power-up aleatoriamente al derrotar enemigos
                if random.randint(0, 100) < 30:
                    power_up = PowerUp(bullet.rect.x, bullet.rect.y, "slow")
                else:
                    power_up = PowerUp(bullet.rect.x, bullet.rect.y, "rapid")
                all_sprites.add(power_up)
                power_up_group.add(power_up)

        # Colisión entre el personaje y los enemigos
        player_enemy_collisions = pygame.sprite.spritecollide(player, enemy_group, False)
        if player_enemy_collisions:
            game_state = GAME_OVER

        # Colisión entre el personaje y los power-ups
        player_power_up_collisions = pygame.sprite.spritecollide(player, power_up_group, True)
        for power_up in player_power_up_collisions:
            if power_up.power_up_type == "slow":
                slow_enemies = True
                power_up_timer = 300
            elif power_up.power_up_type == "rapid":
                rapid_shoot = True
                power_up_timer = 300

        # Generar nuevos enemigos
        if random.randint(0, 100) < 5:
            enemy = Enemy(player)
            all_sprites.add(enemy)
            enemy_group.add(enemy)

        # Dibujado de la pantalla
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Dibujar la puntuación en la pantalla
        score_text = font.render("Puntuación: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Control de los power-ups
        if slow_enemies:
            for enemy in enemy_group:
                enemy.speed = 1
        if rapid_shoot:
            player.shoot_cooldown = 5
            if power_up_timer % 30 == 0:
                player_pos = player.rect.center
                bullet1 = AutoBullet(player_pos[0], player_pos[1])
                bullet2 = AutoBullet(player_pos[0], player_pos[1])
                bullet3 = AutoBullet(player_pos[0], player_pos[1])
                bullet4 = AutoBullet(player_pos[0], player_pos[1])
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullet_group.add(bullet1)
                bullet_group.add(bullet2)
                bullet_group.add(bullet3)
                bullet_group.add(bullet4)
                angle1 = math.radians(45)
                angle2 = math.radians(135)
                angle3 = math.radians(225)
                angle4 = math.radians(315)
                bullet1.speed_x = 5 * math.cos(angle1)
                bullet1.speed_y = -5 * math.sin(angle1)
                bullet2.speed_x = 5 * math.cos(angle2)
                bullet2.speed_y = -5 * math.sin(angle2)
                bullet3.speed_x = 5 * math.cos(angle3)
                bullet3.speed_y = -5 * math.sin(angle3)
                bullet4.speed_x = 5 * math.cos(angle4)
                bullet4.speed_y = -5 * math.sin(angle4)
        power_up_timer -= 1
        if power_up_timer <= 0:
            slow_enemies = False
            rapid_shoot = False

        pygame.display.flip()
        clock.tick(60)

    elif game_state == GAME_OVER:
        # Pantalla de fin de juego
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render("Puntuación: {}".format(score), True, WHITE)
        restart_text = font.render("Presiona ESPACIO para reiniciar", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 50))
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Reiniciar el juego
            all_sprites.empty()
            bullet_group.empty()
            enemy_group.empty()
            power_up_group.empty()
            player = Player()
            all_sprites.add(player)
            game_state = PLAYING
            score = 0

# Salir del juego
pygame.quit()
