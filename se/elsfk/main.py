import pygame
from settings import Settings
import function
from block import Block
from pygame.sprite import Group
from button import Button


def main():
    pygame.init()
    pygame.display.set_caption('elsfk')
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    block = Block(screen)
    blocks = Group()  # 7种图形
    blocks_line = Group()  # 底下的图形
    button = Button(screen, 'Space')
    pygame.mouse.set_visible(False)
    pygame.time.set_timer(pygame.USEREVENT + 1, settings.down_time * 1000)  # 每格一秒发送一次用户事件（下降一次）

    while True:
        function.check_event(blocks_line, blocks, settings, block, button)
        if button.gameactive:
            function.check_collision(block, blocks, blocks_line)
            function.check_gameover(blocks_line, button)
            function.check_block_line_full(block, blocks_line)
            if len(blocks) == 0:
                function.create_blocks(screen, blocks)
            function.updateblocks_down(blocks, settings, block)
            function.updateblocks_move(blocks, block, blocks_line)
            function.updateblocks_rotate(blocks, block)
        function.updatescreen(screen, settings, blocks, blocks_line, button)


if __name__ == '__main__':
    main()
