"""
카드 분배 커맨드
각 player_status 의 card 객체에 6장의 카드 번호를 넣는다.
"""
import random
from copy import deepcopy




def CardDistribution():
        from ..global_repository import player_status_repository
        print(player_status_repository)
        sub_card = ["Basket","Bottle","Canoe","GiantFarm","GrainShovel","JunkWarehouse","LoamMiningSite","Manger","Pincer","Pitchfork","SilPan","WoolBlanket"]
        job_card = ["Greengrocer","Hedger","KilnBaker","LivestockDealer","Lumberjack","Magician","Priest","Roofer","SkilledBrickLayer","SmallFarmer","SubCultivator","WarehouseManager"]
        random.shuffle(sub_card)
        random.shuffle(job_card)
        for player in player_status_repository:
            player_status_repository[player].card.hand_sub_card.append(sub_card.pop(0))
            player_status_repository[player].card.hand_sub_card.append(sub_card.pop(0))
            player_status_repository[player].card.hand_sub_card.append(sub_card.pop(0))
            player_status_repository[player].card.start_sub_card = deepcopy(player_status_repository[player].card.hand_sub_card)
            player_status_repository[player].card.hand_job_card.append(job_card.pop(0))
            player_status_repository[player].card.hand_job_card.append(job_card.pop(0))
            player_status_repository[player].card.hand_job_card.append(job_card.pop(0))
            player_status_repository[player].card.start_job_card = deepcopy(player_status_repository[player].card.hand_job_card)
