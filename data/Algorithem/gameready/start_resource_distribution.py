"""
게임 시작 후 초기 자원 분배 커맨드
"""
from ..command import Command
from ..global_repository import player_status_repository


def StartResourceDistribution():
    first = True
    print(player_status_repository)
    for player in player_status_repository:
        if first:
                player_status_repository[player].resource.set_food(3)
                player_status_repository[player].resource.set_first_turn(True)
                player_status_repository[player].set_worker(2)
                first = False
        else:
                player_status_repository[player].resource.set_food(4)
                player_status_repository[player].set_worker(2)
