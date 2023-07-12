import pygame
from settings import Settings
from ship import Ship
# from alien import Alien
import game_functions as gf
from pygame.sprite import Group
# from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    ship = Ship(ai_settings, screen)
    bullets = Group()
    # bullet=Bullet(ai_settings,screen,ship)
    # alien=Alien(ai_settings,screen)
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    play_button = Button(ai_settings, screen, 'play')

    while True:
        gf.cheak_events(ai_settings, screen, ship, bullets, stats, play_button, aliens)
        if stats.game_active:
            pygame.mouse.set_visible(False)
            ship.update()
            # gf.add_bullet(bullet,bullets,ai_settings, screen, ship)
            gf.update_bullets(aliens, bullets, ai_settings, screen, ship)
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        # print(len(bullets))


if __name__ == '__main__':
    run_game()
