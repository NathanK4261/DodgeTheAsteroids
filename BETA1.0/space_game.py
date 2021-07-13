#!/usr/bin/env python 3
# Import modules and initialize
import pygame as p
import sys
import random
import time
import socket
from datetime import datetime
p.init()
p.mixer.pre_init()

# Read high score now to optimize
with open('high_score/high_score.txt', 'r+') as f:
    score_contents = f.read().replace("\n", " ")
    f.close()

# Create some variables
player_movement = 0
GRAVITY = 0.25
asteroid_height = [300, 100, 400, 200]
game_font = p.font.Font('fonts/PressStart2P-Regular.ttf',20)
asteroid_increase = True
game_active = False
in_high_score = False
score = 0
high_score = score_contents

# Make some functions
def send_data_online():
    lsock = socket.socket()

    host = '192.168.158.155'
    port = 5555

    lsock.connect((host, port))

    ready_message = score_contents
    ready_message = ready_message.encode()
    lsock.send(ready_message)

    new_high_score = lsock.recv(1024)
    new_high_score = new_high_score.decode()
    with open('high_score/GLOBALhigh_score.txt', 'r+') as GLOBALf:
        GLOBALf.truncate()
        GLOBALscore_contents = GLOBALf.write(f'Highest Score: {new_high_score}')
        GLOBALf.close()
def readscore():
    with open('high_score/high_score.txt', 'r+') as f:
        score_contents = f.read()
        f.close()
def create_asteroid():
    random_asteroid_pos = random.choice(asteroid_height)
    new_asteroid = asteroid_surface.get_rect(midtop = (650, random_asteroid_pos))
    return new_asteroid
def move(asteroids):
    for asteroid in asteroids:
        asteroid.centerx -= 5
    return asteroids
def draw(asteroids):
    for asteroid in asteroids:
        sc.blit(asteroid_surface, asteroid)
def collision(asteroids):
    for asteroid in asteroids:
        if player_rect.colliderect(asteroid):
            time.sleep(0.2)
            hit_sound.play()
            return False
        if player_rect.top <= -100 or player_rect.bottom >= 800:
            return False
    return True
def display_score(game_state):
    if game_state == 'in_game':
        score_surface = game_font.render(f'Score: {score}',True, (255,255,255))
        score_rect = score_surface.get_rect(center = (110, 30))
        sc.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        with open('high_score/high_score.txt', 'r+') as f:
            score_contents = f.read()
            f.close()
        high_score_surface = game_font.render(f'High Score: {str(score_contents)}',True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (320, 370))
        sc.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    with open('high_score/high_score.txt', 'r+') as f:
        score_contents = f.read()
        f.close()
    if score > int(score_contents):
        score_contents = score
        high_score = score_contents
        with open('high_score/high_score.txt', 'r+') as f:
            f.truncate(0)
            f.write(f'{str(high_score)}')
            f.close()
    return high_score
def DisplayCurrentTime():
    Font = p.font.Font('fonts/PressStart2P-Regular.ttf', 10)
    CurrentTime = datetime.now()
    DisplayTime = Font.render(f'Current time: {CurrentTime}', True, (255, 255, 255))
    DisplayTimeRect = DisplayTime.get_rect(center = (220, 680))
    sc.blit(DisplayTime, DisplayTimeRect)
def main_menu():
    game_over_surface = game_font.render('Dodge the Asteroids',True, (255,255,255))
    game_over_rect = game_over_surface.get_rect(center = (320, 330))
    sc.blit(game_over_surface, game_over_rect)
    game_over_surface1 = game_font.render('SPACE to play!',True, (255,255,255))
    game_over_rect1 = game_over_surface1.get_rect(center = (320, 350))
    sc.blit(game_over_surface1, game_over_rect1)

    # Get GLOBALhigh_score
    with open('high_score/GLOBALhigh_score.txt', 'r+') as GLOBALf:
        GLOBALscore_contents = GLOBALf.read()
        GLOBALf.close()

    highest_score_surface = game_font.render((f'{GLOBALscore_contents}'),True, (255,255,255))
    highest_score_rect = highest_score_surface.get_rect(center = (350, 490))
    sc.blit(highest_score_surface, highest_score_rect)
# Load high score and regular score
readscore()

# Make a screen
sc = p.display.set_mode((700, 700))

# Make a backround
bg = p.image.load('images/backround.png')
bg = p.transform.scale2x(bg)

# Put in main music
p.mixer.music.load('sound/game_music.wav')

# Play main music
p.mixer.music.play(-1)

# Import character
ship = p.image.load('images/ship.png').convert()

# Import asteroid
asteroid_surface = p.image.load('images/asteroid.png').convert()

# Asteroid logic
asteroid_list = []
SPAWN = p.USEREVENT
p.time.set_timer(SPAWN, 1200)

# Hitbox variables
player_rect = ship.get_rect(center = (100, 350))

# Sound FX
jump_sound = p.mixer.Sound('sound/jump.wav')
hit_sound = p.mixer.Sound('sound/impact.wav')

# Access server and send data
send_data_online()

# Begin code logic
while True:
    # Make the game exit cleanly
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit()
        if event.type == p.KEYDOWN:
            if event.key == p.K_SPACE and game_active and in_high_score == False:
                player_movement = 0
                player_movement -= 8
                jump_sound.play()
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE and game_active == False and in_high_score == False:
                    game_active = True
                    in_high_score = False
                    asteroid_list.clear()
                    player_movement = 0
                    score = 0
                    player_rect.center = (100, 350)
        if game_active:
            if event.type == SPAWN:
                asteroid_list.append(create_asteroid())
                score += 1
        # INDENTATION

    #<--|

    sc.blit(bg, (0, 0))
    DisplayCurrentTime()
    if game_active:
        display_score('in_game')
        player_movement += GRAVITY
        player_rect.centery += player_movement
        
        # Draw asteroids and player
        sc.blit(ship,player_rect)
        asteroid_list = move(asteroid_list)
        draw(asteroid_list)
        game_active = collision(asteroid_list)
        
        # Game info
        info_surface = game_font.render('SPACE to move!',True, (255,255,255))
        info_rect = info_surface.get_rect(center = (550, 30))
        sc.blit(info_surface, info_rect)
        in_high_score = False
    else:
        high_score = update_score(score, high_score)
        display_score('game_over')
            
        # Make the main menu/game over screen
        send_data_online()
        main_menu()
    p.display.update()
