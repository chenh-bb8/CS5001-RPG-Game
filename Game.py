import pygame
import sys
import random

pygame.init()

# Create Windows
screen = pygame.display.set_mode((1440, 900))
pygame.display.set_caption("My First Game")

# Fonts
font = pygame.font.Font(None,30)

# Def color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables
player_hp = 100
enemy_hp = 100
turn_count = 1
player_turn = True
action_log = []

# Define Functions
# Enemy AI
def enemy_AI():
    global player_hp,player_turn
    action = random.choice(["Attack", "Defend"])
    if action == "Attack":
        damage = random.randint(10,15)
        player_hp -= damage
        action_log.append(f'Enemy attacked for {damage} damage.')

    else:
        action_log.append("Enemy defended.")

    player_turn = True

# End Turn
def end_turn():
    global player_turn, turn_count
    player_turn = False
    turn_count += 1

# Attack
def attack_action():
    global enemy_hp, player_turn

    damage = random.randint(10, 15)
    enemy_hp -= damage
    action_log.append(f'Player attacked for {damage} damage.')
    end_turn()

# Defend
def defend_action():
    global player_turn
    action_log.append("Player defended.")
    end_turn()

# Special Attack
def special_action():
    global enemy_hp, player_turn
    damage = random.randint(20, 30)
    enemy_hp -= damage
    action_log.append(f"Player used a special attack for {damage} damage.")
    end_turn()

# Health Bar
def draw_health_bar(x,y, current_hp):
    max_hp = 100
    bar_width, bar_height = 400,40
    health_ratio = current_hp / max_hp
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen,GREEN, (x,y, bar_width * health_ratio, bar_height))

# Draw Button
def draw_button(x,y,width,height,text, action = None):
    global player_turn

    mouse = pygame.mouse.get_pos()


    # Edge Check
    color = GRAY if x < mouse[0] < x + width and y < mouse[1] < y + height else DARK_GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))

    # Button text
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 10))

    if event.type == pygame.MOUSEBUTTONDOWN and x < mouse[0] < x + width and y < mouse[1] < y + height:
        action()

#Draw Action Log
def draw_action_log():
    y = 450
    for log in action_log[-5:]:
        text_surface = font.render(log,True,WHITE)
        screen.blit(text_surface,(1000,y))
        y += 20


# Main Loop
# game = True
while True:
    # Game could be stopped
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # game = False
            sys.exit()

    # Draw health bars
    draw_health_bar(250, 50, player_hp)
    draw_health_bar(1000,50, enemy_hp)

    # Draw action log
    draw_action_log()


    if player_turn:
        draw_button(50, 400, 100, 40, "Attack", attack_action)
        draw_button(50, 500, 100, 40, "Defend", defend_action)
        draw_button(50, 600, 100, 40, "Special", special_action)
        pygame.display.flip()
    else:
        enemy_AI()
        pygame.display.flip()


    # Check Game over
    if player_hp <= 0 or enemy_hp <= 0:
        if player_hp <= 0:
            winner = "Enemy"
        else:
            winner = "Player"

        text_surface = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(text_surface, (1440 // 2 - 50, 900 // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        # game = False

    pygame.display.flip()

