"""
게임 시작 후 초기 자원 분배 커맨드
"""
from ..command import Command
from ..global_repository import player_status_repository


def StartResourceDistribution():
        player_status_repository[0].resource.set_food(3)
        player_status_repository[0].resource.set_first_turn(True)
        player_status_repository[0].set_worker(2)
        player_status_repository[1].resource.set_food(4)
        player_status_repository[1].set_worker(2)
        player_status_repository[2].resource.set_food(4)
        player_status_repository[2].set_worker(2)
        player_status_repository[3].resource.set_food(4)
        player_status_repository[3].set_worker(2)
