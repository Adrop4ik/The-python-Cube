import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический уклонятель")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Игрок
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 6
player_health = 3

# Враги
enemies = []
enemy_size = 40
enemy_speed = 3
enemy_spawn_rate = 30

# Пули
bullets = []
bullet_speed = 7
bullet_cooldown = 0

# Бонусы
powerups = []
powerup_types = ["health", "double", "slow"]

# Взрывы
explosions = []

# Счёт
score = 0
high_score = 0
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

# Игровые состояния
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Фон
stars = []
for _ in range(100):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

# Игровой цикл
clock = pygame.time.Clock()
running = True

def draw_player():
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    # Рисуем "нос" корабля для лучшей визуализации
    pygame.draw.polygon(screen, YELLOW, [
        (player_x + player_size//2, player_y - 10),
        (player_x + 10, player_y + 10),
        (player_x + player_size - 10, player_y + 10)
    ])

def draw_enemy(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, enemy_size, enemy_size))
    # Рисуем "глаза" врагам
    pygame.draw.circle(screen, BLACK, (x + 10, y + 15), 5)
    pygame.draw.circle(screen, BLACK, (x + enemy_size - 10, y + 15), 5)

def draw_bullet(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, 5, 15))

def draw_powerup(x, y, type_):
    if type_ == "health":
        pygame.draw.circle(screen, RED, (x + 15, y + 15), 15)
        pygame.draw.circle(screen, WHITE, (x + 15, y + 15), 10, 2)
        pygame.draw.line(screen, WHITE, (x + 15, y + 5), (x + 15, y + 25), 2)
        pygame.draw.line(screen, WHITE, (x + 5, y + 15), (x + 25, y + 15), 2)
    elif type_ == "double":
        pygame.draw.circle(screen, BLUE, (x + 15, y + 15), 15)
        pygame.draw.rect(screen, WHITE, (x + 5, y + 10, 20, 10))
    else:
        pygame.draw.circle(screen, GREEN, (x + 15, y + 15), 15)
        pygame.draw.line(screen, BLACK, (x + 5, y + 15), (x + 25, y + 15), 3)

def draw_explosion(x, y, size):
    for _ in range(15):
        pygame.draw.circle(screen, WHITE, 
                          (x + random.randint(-size, size), 
                          y + random.randint(-size, size)), 
                          random.randint(2, 4))

def show_menu():
    screen.fill(BLACK)
    # Рисуем звёзды
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
    
    title = big_font.render("КОСМИЧЕСКИЙ УКЛОНЯТЕЛЬ", True, YELLOW)
    start = font.render("Нажмите ПРОБЕЛ чтобы начать", True, WHITE)
    controls1 = font.render("Управление: WASD или стрелки", True, WHITE)
    controls2 = font.render("Стрельба: W или стрелка вверх", True, WHITE)
    
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
    screen.blit(controls1, (WIDTH//2 - controls1.get_width()//2, HEIGHT//2 + 50))
    screen.blit(controls2, (WIDTH//2 - controls2.get_width()//2, HEIGHT//2 + 80))

def reset_game():
    global player_x, player_y, player_health, enemies, bullets, powerups, score, game_state
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    player_health = 3
    enemies = []
    bullets = []
    powerups = []
    score = 0
    game_state = PLAYING

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == MENU and event.key == pygame.K_SPACE:
                reset_game()
            elif game_state == GAME_OVER and event.key == pygame.K_r:
                reset_game()
    
    # Отрисовка фона
    screen.fill(BLACK)
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        star[1] += 1
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
    
    # Игровая логика
    if game_state == PLAYING:
        # Движение игрока
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_size:
            player_x += player_speed
        
        # Стрельба
        if bullet_cooldown > 0:
            bullet_cooldown -= 1
            
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and bullet_cooldown == 0:
            bullets.append([player_x + player_size//2 - 2, player_y])
            bullet_cooldown = 15
        
        # Спавн врагов
        if random.randint(1, enemy_spawn_rate) == 1:
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemy_y = -enemy_size
            enemies.append([enemy_x, enemy_y])
        
        # Движение пуль
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        
        # Движение врагов и проверка столкновений
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            
            # Столкновение с игроком
            if (player_x < enemy[0] + enemy_size and
                player_x + player_size > enemy[0] and
                player_y < enemy[1] + enemy_size and
                player_y + player_size > enemy[1]):
                player_health -= 1
                explosions.append([enemy[0] + enemy_size//2, enemy[1] + enemy_size//2, 30, 10])
                enemies.remove(enemy)
                if player_health <= 0:
                    game_state = GAME_OVER
                    if score > high_score:
                        high_score = score
            
            # Столкновение с пулями
            for bullet in bullets[:]:
                if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_size and
                    bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_size):
                    score += 10
                    explosions.append([enemy[0] + enemy_size//2, enemy[1] + enemy_size//2, 30, 10])
                    enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    
                    # Случайный дроп бонуса
                    if random.randint(1, 5) == 1:
                        powerup_type = random.choice(powerup_types)
                        powerups.append([enemy[0], enemy[1], powerup_type, 180])
                    break
            
            # Удаление врагов за пределами экрана
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
        
        # Обработка бонусов
        for powerup in powerups[:]:
            powerup[1] += 2
            powerup[3] -= 1
            
            # Столкновение с игроком
            if (player_x < powerup[0] + 30 and
                player_x + player_size > powerup[0] and
                player_y < powerup[1] + 30 and
                player_y + player_size > powerup[1]):
                
                if powerup[2] == "health":
                    player_health = min(5, player_health + 1)
                elif powerup[2] == "double":
                    bullet_cooldown = 0
                    for _ in range(5):
                        bullets.append([player_x + player_size//2 - 2, player_y])
                elif powerup[2] == "slow":
                    for enemy in enemies:
                        enemy[1] -= 5
                
                powerups.remove(powerup)
                explosions.append([powerup[0] + 15, powerup[1] + 15, 20, 5])
            
            # Удаление бонусов
            if powerup[1] > HEIGHT or powerup[3] <= 0:
                powerups.remove(powerup)
        
        # Увеличение сложности
        if score > 0 and score % 100 == 0:
            enemy_speed = min(8, 3 + score // 100)
            enemy_spawn_rate = max(10, 30 - score // 50)
    
    # Отрисовка игровых объектов
    if game_state == PLAYING:
        # Отрисовка взрывов
        for explosion in explosions[:]:
            draw_explosion(explosion[0], explosion[1], explosion[2])
            explosion[3] -= 1
            if explosion[3] <= 0:
                explosions.remove(explosion)
        
        # Отрисовка игрока
        draw_player()
        
        # Отрисовка врагов
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        
        # Отрисовка пуль
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        
        # Отрисовка бонусов
        for powerup in powerups:
            draw_powerup(powerup[0], powerup[1], powerup[2])
        
        # Отрисовка HUD
        health_text = font.render(f"Жизни: {player_health}", True, WHITE)
        score_text = font.render(f"Счёт: {score}", True, WHITE)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (10, 40))
    
    elif game_state == MENU:
        show_menu()
    
    elif game_state == GAME_OVER:
        game_over_text = big_font.render("ИГРА ОКОНЧЕНА", True, RED)
        restart_text = font.render("Нажмите R для рестарта", True, WHITE)
        score_text = font.render(f"Ваш счёт: {score}", True, WHITE)
        high_score_text = font.render(f"Рекорд: {high_score}", True, YELLOW)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()