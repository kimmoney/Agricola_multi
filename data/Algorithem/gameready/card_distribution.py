"""
카드 분배 커맨드
각 player_status 의 card 객체에 6장의 카드 번호를 넣는다.
"""
import random
from copy import deepcopy


from ..global_repository import player_status_repository


def CardDistribution():
        sub_card_list = random.sample(range(12), 12)
        for i in range(4):
            for j in range(3):
                if sub_card_list[i * 3 + j] == 0:
                    player_status_repository[i].card.hand_sub_card.append("Basket")
                if sub_card_list[i * 3 + j] == 1:
                    player_status_repository[i].card.hand_sub_card.append("Bottle")
                if sub_card_list[i * 3 + j] == 2:
                    player_status_repository[i].card.hand_sub_card.append("Canoe")
                if sub_card_list[i * 3 + j] == 3:
                    player_status_repository[i].card.hand_sub_card.append("GiantFarm")
                if sub_card_list[i * 3 + j] == 4:
                    player_status_repository[i].card.hand_sub_card.append("GrainShovel")
                if sub_card_list[i * 3 + j] == 5:
                    player_status_repository[i].card.hand_sub_card.append("JunkWarehouse")
                if sub_card_list[i * 3 + j] == 6:
                    player_status_repository[i].card.hand_sub_card.append("LoamMiningSite")
                if sub_card_list[i * 3 + j] == 7:
                    player_status_repository[i].card.hand_sub_card.append("Manger")
                if sub_card_list[i * 3 + j] == 8:
                    player_status_repository[i].card.hand_sub_card.append("Pincer")
                if sub_card_list[i * 3 + j] == 9:
                    player_status_repository[i].card.hand_sub_card.append("Pitchfork")
                if sub_card_list[i * 3 + j] == 10:
                    player_status_repository[i].card.hand_sub_card.append("SilPan")
                if sub_card_list[i * 3 + j] == 11:
                    player_status_repository[i].card.hand_sub_card.append("WoolBlanket")
            player_status_repository[i].card.start_sub_card = \
                deepcopy(player_status_repository[i].card.hand_sub_card)

        job_card_list = random.sample(range(12), 12)
        for i in range(4):
            for j in range(3):
                if job_card_list[i * 3 + j] == 0:
                    player_status_repository[i].card.hand_job_card.append("Greengrocer")
                if job_card_list[i * 3 + j] == 1:
                    player_status_repository[i].card.hand_job_card.append("Hedger")
                if job_card_list[i * 3 + j] == 2:
                    player_status_repository[i].card.hand_job_card.append("KilnBaker")
                if job_card_list[i * 3 + j] == 3:
                    player_status_repository[i].card.hand_job_card.append("LivestockDealer")
                if job_card_list[i * 3 + j] == 4:
                    player_status_repository[i].card.hand_job_card.append("Lumberjack")
                if job_card_list[i * 3 + j] == 5:
                    player_status_repository[i].card.hand_job_card.append("Magician")
                if job_card_list[i * 3 + j] == 6:
                    player_status_repository[i].card.hand_job_card.append("Priest")
                if job_card_list[i * 3 + j] == 7:
                    player_status_repository[i].card.hand_job_card.append("Roofer")
                if job_card_list[i * 3 + j] == 8:
                    player_status_repository[i].card.hand_job_card.append("SkilledBrickLayer")
                if job_card_list[i * 3 + j] == 9:
                    player_status_repository[i].card.hand_job_card.append("SmallFarmer")
                if job_card_list[i * 3 + j] == 10:
                    player_status_repository[i].card.hand_job_card.append("SubCultivator")
                if job_card_list[i * 3 + j] == 11:
                    player_status_repository[i].card.hand_job_card.append("WarehouseManager")
            player_status_repository[i].card.start_job_card = \
                deepcopy(player_status_repository[i].card.hand_job_card)
