import random, pygame, sys


def inital(settings, p1, p2):
    '''初始化游戏'''
    settings.numcard_list = list(range(1, 12))
    random.shuffle(settings.numcard_list)
    p1.numcard, p2.numcard = [], []
    p1.canchoose, p2.canchoose = True, True


def giveinicard(p1, p2, settings):
    '''每人发两张牌'''
    p1.wantcard(settings), p2.wantcard(settings), p1.wantcard(settings), p2.wantcard(settings)


def givecard(settings, p1, p2, ai):
    '''轮流要牌，两人连续都不要牌则结束循环'''
    if settings.tern == 'p1':
        settings.tern = 'p2'
        if (p1.canchoose or p2.canchoose) and p1.point <= settings.maxpoint:
            # print(p1.name, p1.numcard, p1.point)
            # print(p2.name, ['*']+p2.numcard[1:])
            p1.choice(ai.ai(settings, p1, p2), settings)  # 使用ai
    elif settings.tern == 'p2':
        if (p1.canchoose or p2.canchoose) and p2.point <= settings.maxpoint:
            # 改成if p2.canchoose，效果是只要不要牌，后面就不能再要牌
            print(p1.name, ['*'] + p1.numcard[1:])
            print(p2.name, p2.numcard, p2.point)
            choise_event(settings, p2)
        else:
            settings.tern = 'p1'


def checkwinner(p1point, p2point, settings, p1, p2):
    if p1point == p2point or (p1point > settings.maxpoint and p2point > settings.maxpoint):  # 点数相同或都>21
        winner = 'draw game'
    elif (p1point - (settings.maxpoint + 0.5)) * (p2point - (settings.maxpoint + 0.5)) < 0:  # 一个>21，一个<21
        winner = p1.name if p1point < p2point else p2.name
    else:  # 都<21
        winner = p1.name if p1point > p2point else p2.name
    return winner


def checkwinner_with_print(p1point, p2point, settings, p1, p2):
    print(p1.name, ':', p1.numcard, p1point)
    print(p2.name, ':', p2.numcard, p2point)
    winner = checkwinner(p1point, p2point, settings, p1, p2)
    print('winner is:', winner)
    return winner


def update_screen(screen, settings, button):
    screen.fill(settings.bgcolor)
    if not button.gameactive:
        button.draw_button()
    pygame.display.flip()


def keydown_event(event, settings, p1, p2, button):
    if event.key == settings.start_key:
        inital(settings, p1, p2)
        button.gameactive = True
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    # elif event.key==pygame.K_RIGHT:
    #     block.moving_right = True
    # elif event.key==pygame.K_UP:
    #     block.rotate=True


def keyup_event(event): pass


# if event.key==pygame.K_DOWN:
#     block.block_down_flag=True
#     settings.down_speed = 50
# elif event.key == pygame.K_LEFT:pass
#     # block.moving_left = False
# elif event.key==pygame.K_RIGHT:pass
#     # block.moving_right = False
# elif event.key==pygame.K_UP:pass
#     # block.rotate=False
def mousebuttondown_event(event):
    pass


def check_event(settings, p1, p2, button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_event(event, settings, p1, p2, button)
        elif event.type == pygame.KEYUP:
            keyup_event(event, )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown_event(event)
        elif event.type == pygame.USEREVENT + 1:
            pass
        # block.block_down=True


def choise_event(settings, p2):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                p2.choice('y', settings)
                settings.tern = 'p1'
            elif event.key == pygame.K_n:
                p2.choice('n', settings)
                settings.tern = 'p1'
