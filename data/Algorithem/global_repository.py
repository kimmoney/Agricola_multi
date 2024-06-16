from .repository import *
game_status_repository = game_status.GameStatus()

# player_status_repository = [player_status.PlayerStatus() for i in range(4)]
player_status_repository = {}

round_status_repository = round_status.RoundStatus()

def add_player(name,ip):
    global player_status_repository
    player_status_repository[name]=player_status.PlayerStatus(name,ip)
    return player_status_repository
def del_player(name):
    del player_status_repository[name]