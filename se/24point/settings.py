import pygame
class Settings:
    def __init__(self):
        self.maxpoint=21 #王牌：挑战24点预留
        self.numcard_list=[] #牌库，list[-1]是牌面,由game_func.inital()初始化
        self.screensize=(1440,900)
        self.bgcolor=230,230,230
        self.start_key=pygame.K_SPACE
        self.tern='p1'
