import pygame
import random


# Classes and Game Logic-----------------------------------------------------------

# Use Class to integrate charactor
class Charactor:
    def __init__(self, name, health, attack_power, status):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        # Status for defend set
        self.status = status
        self.special_cooldown = 0

    # Attack method
    def attack(self, other):
        # Let charactor stop defend status in a new turn
        self.status = "Normal"

        # When other is defended, half damage
        if other.status == "defend":
            other.health -= self.attack_power / 2
        else:
            other.health -= self.attack_power

    # Defend method
    def defend(self):
        self.status = "defend"

    # Special Ability method
    def special(self, other):
        # Could be used only cooldown
        if self.special_cooldown == 0:
            # Stop the defend status
            self.status = "Normal"
            # Double damage
            other.health -= self.attack_power * 2
            if other.status == "defend":
                other.health -= self.attack_power
            # Use three rounds apart, that is, the fourth round is available
            self.special_cooldown = 4
            return True
        else:
            return False

    # Enemy's action logic
    def AI(self, other):
        # When special cooldown, special first.
        if self.health < 50 and self.special_cooldown == 0:
            self.special(other)
            action_log.append(("Enemy used a special attack!", "enemy"))
            return "special"
        # When health < 50, increase the priority of defense
        elif self.health < 50:
            self.defend()
            action_log.append(("Enemy defended.", "enemy"))
            return "defend"
        elif self.special_cooldown == 0:
            self.special(other)
            action_log.append(("Enemy used a special attack!", "enemy"))
            return "special"
        else:
            # Normal condition, random choose
            action = random.choice(["Attack", "Defend"])
            if action == "Attack":
                self.attack(other)
                action_log.append((f"Enemy attacked for {self.attack_power} damage.", "enemy"))
                return "attack"
            else:
                self.defend()
                action_log.append(("Enemy defended.", "enemy"))
                return "defend"

# class Game to manage the game conveniently
class Game:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        # Default start with player
        self.turn = "player"

    # Switch turn between player and enemy
    def switch_turn(self):
        self.turn = "enemy" if self.turn == "player" else "player"

    # Check whether game is over
    def is_over(self):
        return self.player.health <= 0 or self.enemy.health <= 0

# Sound materials collection
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.bgm_playing = True
        self.bgm = "sound/bgmusic.mp3"
        self.sounds = {
            "attack": pygame.mixer.Sound("sound/attack.mp3"),
            "defend": pygame.mixer.Sound("sound/defend.mp3"),
            "win": pygame.mixer.Sound("sound/win.mp3"),
            "lose": pygame.mixer.Sound("sound/lose.mp3"),
            "special": pygame.mixer.Sound("sound/special.mp3")
        }
        self.volume = 0.5
        pygame.mixer.music.load(self.bgm)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    #Toggle background music on or off
    def toggle_bgm(self):
        if self.bgm_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.bgm_playing = not self.bgm_playing

    # Play the corresponding sound effects
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.volume)
            self.sounds[sound_name].play()



# Initialization and Assets--------------------------------------------------------------------------

pygame.init()

# Screen setup
screen = pygame.display.set_mode((1440, 900))
pygame.display.set_caption("A Game")

# Fonts, large font for title
font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 50)

# Images
bg_image = pygame.image.load("image/background.png")
music_icon = pygame.image.load("image/music.png")
mute_icon = pygame.image.load("image/mute.png")
player_image = pygame.image.load("image/player.png")
enemy_image = pygame.image.load("image/enemy.png")
attack_flag = pygame.image.load("image/attack.png")
defense_flag = pygame.image.load("image/defend.png")

# Colors will be used in this program
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Game variables
action_log = []
sound_manager = SoundManager()

# Instance Charactor and Game
player = Charactor("Player", 100, random.randint(10, 15), "Normal")
enemy = Charactor("Enemy", 100, random.randint(10, 15), "Normal")
game = Game(player, enemy)

# Initialize flag
player_flag = None
enemy_flag = None
player_flag_timer = 0
enemy_flag_timer = 0

# Start with Menu page
game_state = "menu"

# To start the main loop
running = True


# Define Functions-------------------------------------------------------------------------------

# For special, it will CD with turns
def reduce_cooldowns():
    if player.special_cooldown > 0:
        player.special_cooldown -= 1
    if enemy.special_cooldown > 0:
        enemy.special_cooldown -= 1

# Draw Health Bar
def draw_health_bar(x, y, current_hp, label):
    max_hp = 100
    bar_width, bar_height = 400, 40
    health_ratio = current_hp / max_hp

    # Two color to indicate current hp and lost hp
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_ratio, bar_height))

    # Text to indicate current hp
    health_text = font.render(f"{label}: {current_hp}/{max_hp}", True, WHITE)
    screen.blit(health_text, (x, y + bar_height + 5))

# Draw Action Log
def draw_action_log():
    # Start position, lower right corner
    log_x, log_y = 1000, 750
    # Area size
    log_width, log_height = 400, 100
    log_surface = pygame.Surface((log_width, log_height), pygame.SRCALPHA)
    #Set transparency
    log_surface.fill((0, 0, 0, 128))
    screen.blit(log_surface, (log_x, log_y))

    y = log_y
    # Show lasted 5 message in action log
    for log, log_type in action_log[-5:]:
        # action from player is green, form enemy is red
        color = GREEN if log_type == "player" else RED
        text_surface = font.render(log, True, color)
        screen.blit(text_surface, (log_x, y))
        y += 20

# Draw Button
def draw_button(x, y, width, height, text, cooldown=0):
    # If mouse on button, give a highlight feedback
    mouse = pygame.mouse.get_pos()
    color = GRAY if x < mouse[0] < x + width and y < mouse[1] < y + height else DARK_GRAY
    # For special, if the CD is not ready, no light to indicate it can not be used
    if cooldown > 0:
        color = DARK_GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 10))

# Start Menu
def draw_start_menu():
    title_text = large_font.render("A Game", True, WHITE)
    screen.blit(title_text, (1440 // 2 - 75, 330))
    draw_button(1440 // 2 - 100, 400, 200, 50, "Start Game")
    draw_button(1440 // 2 - 100, 500, 200, 50, "Exit")

# Display flags
def draw_flags():
    if player_flag and pygame.time.get_ticks() < player_flag_timer:
        screen.blit(player_flag, (250, 350))
    if enemy_flag and pygame.time.get_ticks() < enemy_flag_timer:
        screen.blit(enemy_flag, (900, 350))

# Reset the game to its initial state.
def restart_game():
    global player, enemy, game, action_log, game_state
    attack_power = random.randint(10, 15)
    player = Charactor("Player", 100, attack_power, "Normal")
    enemy = Charactor("Enemy", 100, attack_power, "Normal")
    game = Game(player, enemy)
    action_log.clear()
    game_state = "running"


# Main Game Loop--------------------------------------------------------------------------------------

while running:
    # Load Background Image
    screen.blit(bg_image, (0, 0))

    if game_state == "menu":
        # Draw the start menu
        draw_start_menu()
        for event in pygame.event.get():
            # Could stop the game by click "X" on windows
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Button X coordinate
                if 1440 // 2 - 100 <= event.pos[0] <= 1440 // 2 + 100:
                    # Y coordinate
                    # Start button
                    if 400 <= event.pos[1] <= 450:
                        restart_game()
                    # Exit Button
                    elif 500 <= event.pos[1] <= 550:
                        running = False
    # Game page
    elif game_state == "running":
        # Create UI
        draw_health_bar(50, 50, player.health, "Player Health")
        draw_health_bar(1000, 50, enemy.health, "Enemy Health")
        draw_action_log()
        draw_flags()

        draw_button(50, 400, 100, 40, "Attack")
        draw_button(50, 500, 100, 40, "Defend")
        draw_button(50, 600, 100, 40, "Special", player.special_cooldown)

        # Music button image call
        if sound_manager.bgm_playing:
            screen.blit(music_icon, (10, 850))
        # Mute button image call
        else:
            screen.blit(mute_icon, (10, 850))

        # Load charactor image
        screen.blit(player_image, (200, 500))
        screen.blit(enemy_image, (1000, 500))

        # Player's handle
        for event in pygame.event.get():
            # Close window to stop the game
            if event.type == pygame.QUIT:
                running = False
            # Click action get
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mute and play music switch
                if 10 <= event.pos[0] <= 60 and 850 <= event.pos[1] <= 900:
                    sound_manager.toggle_bgm()

                # Game Play, player's turn
                elif game.turn == "player":
                    # Attack button area
                    if 50 <= event.pos[0] <= 150 and 400 <= event.pos[1] <= 440:
                        player.attack(enemy)
                        # Add action into log
                        action_log.append(("Player attacked!", "player"))
                        # Music effect call
                        sound_manager.play_sound("attack")
                        # Flag Call
                        player_flag = attack_flag
                        player_flag_timer = pygame.time.get_ticks() + 1000
                        # Switch turn
                        game.switch_turn()
                    # Defense button area
                    elif 50 <= event.pos[0] <= 150 and 500 <= event.pos[1] <= 540:
                        player.defend()
                        action_log.append(("Player defended!", "player"))
                        sound_manager.play_sound("defend")
                        player_flag = defense_flag
                        player_flag_timer = pygame.time.get_ticks() + 1000
                        game.switch_turn()
                    elif 50 <= event.pos[0] <= 150 and 600 <= event.pos[1] <= 640:
                        # Check CD
                        if player.special(enemy):
                            action_log.append(("Player used special!", "player"))
                            sound_manager.play_sound("special")
                            player_flag = attack_flag
                            player_flag_timer = pygame.time.get_ticks() + 1000
                            game.switch_turn()

        # Enemy's turn
        if game.turn == "enemy" and not game.is_over():
            # Receive an action
            enemy_action = enemy.AI(player)
            if enemy_action == "attack":
                enemy_flag = attack_flag
            elif enemy_action == "defend":
                enemy_flag = defense_flag
            elif enemy_action == "special":
                enemy_flag = attack_flag
                # Enemy's other action does not have music effect, but special has, to indicate player a higher damage
                sound_manager.play_sound("special")
            enemy_flag_timer = pygame.time.get_ticks() + 1000
            reduce_cooldowns()
            game.switch_turn()

        # When Game Over, set winner and Call music effect
        if game.is_over():
            winner = "Player" if player.health > 0 else "Enemy"
            sound_manager.play_sound("win" if winner == "Player" else "lose")
            game_state = "end"

    # End page
    elif game_state == "end":
        # End state
        winner = "Player" if player.health > 0 else "Enemy"

        # Indicate the Winner
        title_text = large_font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(title_text, (1440 // 2-100, 350))

        # Create Button to replay and quit
        draw_button(1440 // 2 - 100, 400, 200, 50, "Replay")
        draw_button(1440 // 2 - 100, 500, 200, 50, "Quit")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check Button area, Same X coordinate range
                if 1440 // 2 - 100 <= event.pos[0] <= 1440 // 2 + 100:
                    # Replay button Y coordinate range
                    if 400 <= event.pos[1] <= 450:
                        restart_game()
                    # Quit button Y coordinate range
                    elif 500 <= event.pos[1] <= 550:
                        running = False
    # Refresh the screen
    pygame.display.flip()
