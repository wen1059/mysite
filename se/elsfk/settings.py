import pygame
class Settings():
    def __init__(self):
        self.screen_width=500#屏幕宽度，block宽的整数倍
        self.screen_height=800
        self.bgcolor=(230,230,230)
        self.down_time=1    #每隔几秒下降一次
        self.down_speed=50   #每次自动下降的距离(50表示1格,方块像素）
        self.down_speed_down=4#按住下键时下降的速度，
        self.start_key=pygame.K_SPACE
