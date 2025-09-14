import pygame
import random
import time
import sys


class Charactor:
    def __init__(self, name, health, attack_power, status):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.status = status
        self.special_cooldown = 0

    def attack(self, other):
        self.status = "Normal"
        if other.status == "defend":
            other.health -= self.attack_power / 2
        else:
            other.health -= self.attack_power

    def defend(self):
        self.status = "defend"

    def special(self, other):
        if self.special_cooldown == 0:  # Only allow if cooldown is 0
            self.status = "Normal"
            other.health -= self.attack_power * 2
            if other.status == "defend":
                other.health -= self.attack_power
            self.special_cooldown = 4  # Set cooldown to 3 turns
            return True  # Indicate success
        else:
            return False

    def AI(self, other):
        action = random.choice(["Attack", "Defend"])
        if action == "Attack":
            self.attack(other)
        else:
            self.defend()

class Game:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 'player'

    def switch_turn(self):
        self.turn = 'enemy' if self.turn == 'player' else 'player'

    def is_over(self):
        return self.player.health <= 0 or self.enemy.health <= 0


pygame.init()

# Create Windows
screen = pygame.display.set_mode((1440, 900))
pygame.display.set_caption("My First Game")

# Fonts
font = pygame.font.Font(None, 30)

# Background
bg_image = pygame.image.load("image/background.png")
screen.blit(bg_image,(0,0))
pygame.display.flip()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Action Log
action_log = []

def reduce_cooldowns():
    if player.special_cooldown > 0:
        player.special_cooldown -= 1



def draw_health_bar(x, y, current_hp):
    max_hp = 100
    bar_width, bar_height = 400, 40
    health_ratio = current_hp / max_hp
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_ratio, bar_height))

def draw_button(x, y, width, height, text, cooldown = 0):
    mouse = pygame.mouse.get_pos()
    # Change color on hover
    color = GRAY if x < mouse[0] < x + width and y < mouse[1] < y + height else DARK_GRAY

    # Disable button if on cooldown
    if cooldown > 0:
        color = DARK_GRAY

    pygame.draw.rect(screen, color, (x, y, width, height))
    # Button text
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 10))

def draw_action_log():
    # Define the area for the action log
    log_area_x, log_area_y = 1000, 750
    log_area_width, log_area_height = 400, 100

    # Create a transparent surface
    log_surface = pygame.Surface((log_area_width, log_area_height), pygame.SRCALPHA)
    log_surface.fill((0, 0, 0, 128))  # RGBA: Black with 50% transparency (128 alpha)

    # Blit the transparent surface onto the screen
    screen.blit(log_surface, (log_area_x, log_area_y))

    # Draw the last 5 messages on top of the transparent background
    y = log_area_y
    for log in action_log[-5:]:
        text_surface = font.render(log, True, WHITE)
        screen.blit(text_surface, (log_area_x, y))
        y += 20  # Increment y position for the next line

def draw_end_screen(winner):
    # Display the winner message
    text_surface = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(text_surface, (1440 // 2 - 100, 900 // 2 - 100))

    # Draw Replay button
    draw_button(1440 // 2 - 150, 900 // 2, 100, 40, "Replay")

    # Draw Quit button
    draw_button(1440 // 2 + 50, 900 // 2, 100, 40, "Quit")

# Main Loop
attack_power = random.randint(10, 15)
player = Charactor("Player", 100, attack_power, "Normal")
enemy = Charactor("Enemy", 100, attack_power, "Normal")

game = Game(player, enemy)

running = True
while running:


    # Draw health bars
    draw_health_bar(50, 50, player.health)
    draw_health_bar(1000, 50, enemy.health)

    # Draw action log
    draw_action_log()

    # Draw buttons
    draw_button(50, 400, 100, 40, "Attack")
    draw_button(50, 500, 100, 40, "Defend")
    draw_button(50, 600, 100, 40, "Special", player.special_cooldown)

    #Draw Charactor
    player_image = pygame.image.load("image/player.png")
    screen.blit(player_image, (200, 500))
    pygame.display.update()

    enemy_image = pygame.image.load("image/enemy.png")
    screen.blit(enemy_image,(1000,500))
    pygame.display.update()

    # Game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # sys.exit()
            running = False
        # Click mouse
        if event.type == pygame.MOUSEBUTTONDOWN and game.turn == 'player':
            # If mouse was clicked on the button area
            if 50 <= event.pos[0] <= 150 and 400 <= event.pos[1] <= 440:
                player.attack(enemy)
                action_log.append(f"Player attacked for {player.attack_power} damage.")
            elif 50 <= event.pos[0] <= 150 and 500 <= event.pos[1] <= 540:
                player.defend()
                action_log.append("Player defended.")
            elif 50 <= event.pos[0] <= 150 and 600 <= event.pos[1] <= 640:
                if player.special(enemy):
                    action_log.append(f"Player used special for {player.attack_power * 2} damage.")
                else:
                    action_log.append("Special is on cooldown!")

            game.switch_turn()
            pygame.display.update()

    # Enemy turn logic
    if game.turn == 'enemy' and not game.is_over():

        enemy.AI(player)
        action_log.append(f"Enemy attacked for {enemy.attack_power} damage." if enemy.status == "Normal" else "Enemy defended.")
        game.switch_turn()
        reduce_cooldowns()
        pygame.display.update()

    # Check game over
    if game.is_over():
        winner = "Player" if player.health > 0 else "Enemy"
        text_surface = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(text_surface, (1440 // 2 - 50, 900 // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()