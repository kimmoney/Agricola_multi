from .repository import *
game_status_repository = game_status.GameStatus()

# player_status_repository = [player_status.PlayerStatus() for i in range(4)]
player_status_repository = {}

round_status_repository = round_status.RoundStatus()


server_game_status = game_status.GameStatus()

# player_status_repository = [player_status.PlayerStatus() for i in range(4)]
server_player_status = {}

server_round_status = round_status.RoundStatus()
def add_player(name,ip):
    global server_player_status
    server_player_status[name]=player_status.PlayerStatus(name,ip)
    return server_player_status
def del_player(name):
    del server_player_status[name]