import pytest
from unittest.mock import Mock
from game import Charactor, Game, SoundManager


# Test the Charactor class
def test_charactor_attack():
    player = Charactor("Player", 100, 20, "Normal")
    enemy = Charactor("Enemy", 100, 20, "Normal")

    # Player attacks Enemy
    player.attack(enemy)
    assert enemy.health == 80  # Full damage applied
    assert player.status == "Normal"  # Status reset after attack

    # Enemy defends and Player attacks
    enemy.defend()
    player.attack(enemy)
    assert enemy.health == 70  # Half damage applied when defending


def test_charactor_defend():
    char = Charactor("Player", 100, 20, "Normal")
    char.defend()
    assert char.status == "defend"  # Status set to defend


def test_charactor_special():
    player = Charactor("Player", 100, 20, "Normal")
    enemy = Charactor("Enemy", 100, 20, "Normal")

    # Use special when not on cooldown
    result = player.special(enemy)
    assert result is True
    assert enemy.health == 60  # Double damage applied
    assert player.special_cooldown == 4  # Cooldown set

    # Attempt to use special when on cooldown
    result = player.special(enemy)
    assert result is False


def test_charactor_AI():
    enemy = Charactor("Enemy", 30, 20, "Normal")
    player = Charactor("Player", 100, 20, "Normal")

    # Special attack when health < 50
    action = enemy.AI(player)
    assert action == "special"
    assert player.health == 60  # Double damage applied

    # Defend when health < 50 and special on cooldown
    enemy.special_cooldown = 4
    action = enemy.AI(player)
    assert action == "defend"
    assert enemy.status == "defend"


# Test the Game class
def test_game_switch_turn():
    player = Charactor("Player", 100, 20, "Normal")
    enemy = Charactor("Enemy", 100, 20, "Normal")
    game = Game(player, enemy)

    # Switch turns
    assert game.turn == "player"
    game.switch_turn()
    assert game.turn == "enemy"
    game.switch_turn()
    assert game.turn == "player"


def test_game_is_over():
    player = Charactor("Player", 0, 20, "Normal")  # Player has 0 health
    enemy = Charactor("Enemy", 100, 20, "Normal")
    game = Game(player, enemy)

    # Check if the game is over
    assert game.is_over() is True

    player.health = 50
    enemy.health = 0  # Enemy has 0 health
    assert game.is_over() is True

    player.health = 50
    enemy.health = 50  # Both players have health
    assert game.is_over() is False


# Test the SoundManager class
def test_sound_manager_toggle_bgm(mocker):
    mocker.patch("pygame.mixer.music.pause")
    mocker.patch("pygame.mixer.music.unpause")

    sound_manager = SoundManager()
    assert sound_manager.bgm_playing is True

    # Toggle background music off
    sound_manager.toggle_bgm()
    assert sound_manager.bgm_playing is False

    # Toggle background music on
    sound_manager.toggle_bgm()
    assert sound_manager.bgm_playing is True


def test_sound_manager_play_sound(mocker):
    mocker.patch("pygame.mixer.Sound.play")

    sound_manager = SoundManager()
    sound_manager.play_sound("attack")
    assert "attack" in sound_manager.sounds
