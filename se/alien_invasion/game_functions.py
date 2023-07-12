import sys
from  time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def cheak_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key== pygame.K_z:
        # bullet.add=True
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key==pygame.K_ESCAPE:
        sys.exit()

def cheak_keyup_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_z:
        # bullet.add = False
        pass

def cheak_events(ai_settings,screen,ship,bullets,stats,play_button,aliens):
    pygame.mouse.set_visible(True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            cheak_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            cheak_keyup_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,aliens,bullets,screen,ship)

def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,aliens,bullets,screen,ship):
    if not stats.game_active:
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True
            aliens.empty()
            bullets.empty()
            create_fleet(ai_settings, screen, aliens, ship)
            ship.center_ship()

# def add_bullet(bullet,bullets,ai_settings, screen, ship):
#     if bullet.add:
#         new_bullet = Bullet(ai_settings, screen, ship)
#         bullets.add(new_bullet)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
     screen.fill(ai_settings.bg_color)
     for bullet in bullets.sprites():
         bullet.draw_bullet()
     ship.blitme()
     aliens.draw(screen)
     sb.show_score()
     if not stats.game_active:
         play_button.draw_button()
     pygame.display.flip()

def update_bullets(aliens,bullets,ai_settings, screen,ship):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets)
def check_bullet_alien_collisions(ai_settings, screen,aliens,ship,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if len(aliens)==0:
        bullets.empty()
        create_fleet(ai_settings, screen,aliens,ship)

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_alien_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows
def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)
def create_fleet(ai_settings, screen,aliens,ship):
    alien = Alien(ai_settings, screen)
    number_alien_x=get_number_alien_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1
def ship_hit(ai_settings,aliens,ship,stats,screen,bullets):
    if stats.ships_left>0:
        stats.ships_left-=1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active=False
def check_aliens_bottom(ai_settings,aliens,ship,stats,screen,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,aliens,ship,stats,screen,bullets)
            break
def update_aliens(ai_settings,aliens,ship,stats,screen,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,aliens,ship,stats,screen,bullets)
    check_aliens_bottom(ai_settings, aliens, ship, stats, screen, bullets)