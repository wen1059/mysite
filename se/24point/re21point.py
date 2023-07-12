import settings
import ai
import player
import game_func
import pygame
import button

pygame.init()
settings = settings.Settings()
ai = ai.Ai()
p1, p2 = player.Player('computer'), player.Player('player2')
screen = pygame.display.set_mode((settings.screensize[0], settings.screensize[1]))
button = button.Button(screen, 'space')
pygame.display.set_caption('RE7-DLC21')

while True:
    game_func.check_event(settings, p1, p2,button)
    if button.gameactive:
        game_func.giveinicard(p1,p2,settings)
        game_func.givecard(settings,p1,p2,ai)
        if not (p1.canchoose or p2.canchoose):
            game_func.checkwinner_with_print(p1.point,p2.point,settings,p1,p2)
            button.gameactive=False
    game_func.update_screen(screen,settings,button)
