import pgzrun
import random
import math
from animation import animate
from animation import animateDirection
from pgzero import music
from pgzero.keyboard import keys
import menu
#from pygame import Rect  

score = 0
game_over = False

WIDTH = 800
HEIGHT = 600

idle_spritesRight = ["hero_idle", "herorun1r_idle", "herorun2r_idle"]
idle_spritesLeft = ["hero_idlel", "herorun1l_idle", "herorun2l_idle"]

enemy_spritesRight = ["enemy_idler","enemy_idle1r","enemy_idle2r"]
enemy_spritesLeft = ["enemy_idle","enemy_idle1l","enemy_idle2l"]

hero = Actor("hero_idle")
hero.y = HEIGHT - 50  # Fica no fundo da tela
hero.x = WIDTH // 2   # Centraliza no meio

hero.vy = 0          # Velocidade vertical do herói
hero.on_ground = True

enemy = Actor("enemy_idle")
enemy.y = 100  # Fica no alto da tela
enemy.x = WIDTH // 2   # Centraliza no meio
enemy_speed = 4


# Inimigo que cruza por baixo
ground_enemy = Actor("enemy_idle")  # pode trocar para "enemy_bottom"
ground_enemy.y = HEIGHT - 50
ground_enemy.x = WIDTH + 100  # começa fora da tela, à direita
ground_enemy_speed = -4       # vem da direita para a esquerda

projectiles = []  # Lista para armazenar projéteis

def egg_projectile():
    p = Actor("projectile")  # Lembre de ter a imagem 'projectile.png'
    p.pos = enemy.pos
    projectiles.append(p)

def draw():
    screen.clear()
    if menu.game_state == "menu":
        menu.draw_menu(screen, WIDTH)
    elif menu.game_state == "playing":
        draw_game()

def on_key_down(key):
    if menu.game_state == "menu":
        menu.update_menu_input(key, music)
    elif key == keys.ESCAPE:
        menu.game_state = "menu"
        music.stop()

def draw_game():
        
        screen.draw.text("Jogo em andamento!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50)
        screen.clear()
        screen.fill((30, 30, 30))  # fundo cinza escuro

        if game_over:
            screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=80, color="red")
            screen.draw.text(f"Score final: {score}", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=50, color="white")
        else:
            hero.draw()
            enemy.draw()
            ground_enemy.draw()

        for p in projectiles:
            p.draw()

        screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")

def update():
        if menu.game_state != "playing":
            return

        global enemy_speed, ground_enemy_speed, score, game_over

        if game_over:
            return

        if keyboard.left and hero.left > 0:
            hero.x -= 5
            animate(hero, idle_spritesLeft)
            
            
        if keyboard.right and hero.right < WIDTH:
            hero.x += 5 
            animate(hero, idle_spritesRight)

        # PULO
        gravity = 1
        hero.vy += gravity
        hero.y += hero.vy

        if hero.y >= HEIGHT - hero.height // 2:
            hero.y = HEIGHT - hero.height // 2
            hero.vy = 0
            hero.on_ground = True
        else:
            hero.on_ground = False

        if keyboard.space and hero.on_ground:
            hero.vy = -25
            hero.on_ground = False

        # Movimento lateral do inimigo
        
        enemy.x += enemy_speed
        
        if enemy.right > WIDTH:
            enemy_speed = -4
        
        elif enemy.left < 0:
            enemy_speed = 4
            
        animateDirection(enemy_speed, enemy, enemy_spritesRight, enemy_spritesLeft)
        animate(ground_enemy, enemy_spritesLeft)

        randomInt = random.randint(1,50)
        if randomInt == 1:
            enemy_speed *= -1

            # Movimento do inimigo que vem de baixo (direita -> esquerda)
        ground_enemy.x += ground_enemy_speed
        if ground_enemy.right < 0:
            ground_enemy.x = WIDTH + random.randint(50, 200)  # reaparece da direita
            

        # Colisão com o inimigo de baixo
        if hero.colliderect(ground_enemy):
            game_over = True

        # Controle de tempo para disparar (a cada 60 frames)
        if not hasattr(update, "frame_count"):
            update.frame_count = 0
        update.frame_count += 1

        if update.frame_count % 60 == 0:
            egg_projectile()

        # Movimento dos projéteis para baixo
        for p in projectiles[:]:  # copia da lista para poder remover durante o loop
            p.y += 10  # continua caindo
        
            if p.colliderect(hero):
                projectiles.remove(p)
                score += 1  # conta o coletado
        
            elif p.top > HEIGHT:
                projectiles.remove(p)  # remove se passar da tela
pgzrun.go()


