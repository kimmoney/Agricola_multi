from .repository import *
game_status_repository = game_status.GameStatus()

player_status_repository = [player_status.PlayerStatus() for i in range(4)]

round_status_repository = round_status.RoundStatus()

