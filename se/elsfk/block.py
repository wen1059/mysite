import pygame
from pygame.sprite import Sprite
class Block(Sprite):
    def __init__(self,screen):
        super().__init__()
        self.image=pygame.image.load('image/block.bmp')
        self.rect=self.image.get_rect()
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.rect.x=self.screen_rect.centerx
        self.block_down=False
        self.block_down_flag=True
        self.moving_right=False
        self.moving_left=False
        self.rotate=False
