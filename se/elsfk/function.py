import pygame
import sys
import random
from block import Block

def keydown_event(event,blocks_line,blocks,settings,block,button):
    if event.key==settings.start_key:
        blocks.empty()
        blocks_line.empty()
        button.gameactive=True
    elif event.key==pygame.K_ESCAPE:
        sys.exit()
    elif event.key==pygame.K_DOWN:
        block.block_down=True
        block.block_down_flag = False
        settings.down_speed=settings.down_speed_down
    elif event.key==pygame.K_LEFT:
        block.moving_left = True
    elif event.key==pygame.K_RIGHT:
        block.moving_right = True
    elif event.key==pygame.K_UP:
        block.rotate=True

def keyup_event(event,settings,block):
    if event.key==pygame.K_DOWN:
        block.block_down_flag=True
        settings.down_speed = 50
    elif event.key == pygame.K_LEFT:pass
        # block.moving_left = False
    elif event.key==pygame.K_RIGHT:pass
        # block.moving_right = False
    elif event.key==pygame.K_UP:pass
        # block.rotate=False

def mousebuttondown_event():
    pass

def check_event(blocks_line,blocks,settings,block,button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_event(event,blocks_line,blocks,settings,block,button)
        elif event.type == pygame.KEYUP:
            keyup_event(event,settings,block)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown_event()
        elif event.type==pygame.USEREVENT+1:
            block.block_down=True

def create_blocks(screen,blocks):#随机生成7种类型中的一种
    type_list=['T','O','I','L','J','Z','N']
    a=random.choice(type_list)
    new_block1 = Block(screen)
    new_block2 = Block(screen)
    new_block3 = Block(screen)
    new_block4 = Block(screen)
    new_block1.image = pygame.image.load('image/block1.bmp')
    new_block2.image = pygame.image.load('image/block2.bmp')
    new_block3.image = pygame.image.load('image/block3.bmp')
    new_block4.image = pygame.image.load('image/block4.bmp')
    blocks.add(new_block1)
    new_block2.rect.x = new_block1.rect.x + new_block1.rect.width
    blocks.add(new_block2)
    if a=='Z' or a=='O' or a=='N':
        new_block3.rect.y = new_block1.rect.y + new_block1.rect.width
        blocks.add(new_block3)
        if a=='O':
            new_block4.rect.x = new_block1.rect.x + new_block1.rect.width
            new_block4.rect.y = new_block1.rect.y + new_block1.rect.width
            blocks.add(new_block4)
        elif a=='N':
            new_block4.rect.x = new_block1.rect.x - new_block1.rect.width
            new_block4.rect.y = new_block1.rect.y + new_block1.rect.width
            blocks.add(new_block4)
        elif a=='Z':
            new_block4.rect.x = new_block1.rect.x + new_block1.rect.width
            new_block4.rect.y = new_block1.rect.y - new_block1.rect.width
            blocks.add(new_block4)
    elif a=='I' or a=='L' or a=='J' or a=='T':
        new_block3.rect.x = new_block1.rect.x - new_block1.rect.width
        blocks.add(new_block3)
        if a=='J':
            new_block4.rect.x = new_block1.rect.x + new_block1.rect.width
            new_block4.rect.y = new_block1.rect.y + new_block1.rect.width
            blocks.add(new_block4)
        elif a=='L':
            new_block4.rect.x = new_block1.rect.x - new_block1.rect.width
            new_block4.rect.y = new_block1.rect.y + new_block1.rect.width
            blocks.add(new_block4)
        elif a=='T':
            new_block4.rect.y = new_block1.rect.y + new_block1.rect.width
            blocks.add(new_block4)
        elif a == 'I':
            new_block4.rect.x = new_block1.rect.x + 2*new_block1.rect.width
            blocks.add(new_block4)

def updatescreen(screen,settings,blocks,blocks_line,button):
    screen.fill(settings.bgcolor)
    blocks.draw(screen)
    blocks_line.draw(screen)
    if not button.gameactive:
        button.draw_button()
    pygame.display.flip()

def updateblocks_down(blocks,settings,block):#下降
    if block.block_down:#由用户事件控制
        for new_block in blocks.sprites():
            new_block.rect.y+=settings.down_speed
        if block.block_down_flag:#实现按住持续下降
            block.block_down=False

def updateblocks_move(blocks,block,blocks_line):#左右移动
    if block.moving_left:
        flag_left=True
        for new_block in blocks.sprites():
            if new_block.rect.x==block.screen_rect.x:
                flag_left=False#先检测全部4个方块，只要有一个碰边就不再移动
            for new_block_line in blocks_line:
                if new_block_line.rect.y-new_block.rect.height < new_block.rect.y \
                        < new_block_line.rect.y+new_block.rect.height \
                        and new_block.rect.x==new_block_line.rect.x+new_block_line.rect.width:
                    flag_left = False#旁边有方块的话就不能继续移动
        if flag_left:
            for new_block in blocks.sprites():
                new_block.rect.x -= new_block.rect.width
        block.moving_left = False
    if block.moving_right:
        flag_right = True
        for new_block in blocks.sprites():
            if new_block.rect.x == block.screen_rect.right-new_block.rect.width:
                flag_right = False
            for new_block_line in blocks_line:
                if new_block_line.rect.y-new_block.rect.height < new_block.rect.y \
                        < new_block_line.rect.y+new_block.rect.height \
                        and new_block.rect.x==new_block_line.rect.x+new_block_line.rect.width:
                    flag_right = False#旁边有方块的话就不能继续移动
        if flag_right:
            for new_block in blocks.sprites():
                new_block.rect.x += new_block.rect.width
        block.moving_right = False

def updateblocks_rotate(blocks,block):#顺时针旋转
    rotate_x, rotate_y=None,None#记录第一个方块的坐标，绕其旋转
    if block.rotate:
        for block_1 in blocks.sprites():
            rotate_x=block_1.rect.x
            rotate_y=block_1.rect.y
            break
        for new_block in blocks.sprites():
            new_block_x=new_block.rect.x#待旋转方块旋转前的坐标
            new_block_y=new_block.rect.y
            new_block.rect.x = rotate_x- (new_block_y - rotate_y)
            new_block.rect.y = rotate_y+ (new_block_x - rotate_x)
    block.rotate = False

def check_collision_blocks_bottom(block,blocks):#检测方块碰底部屏幕
    for new_block in blocks.sprites():
        if new_block.rect.bottom>=block.screen_rect.bottom:
            col=new_block.rect.y+new_block.rect.height-block.screen_rect.bottom
            for new_block in blocks.sprites():
                new_block.rect.y -= col
            return True
def check_collision_blocks_blocks_line(blocks,blocks_line):#检测方块碰到下方堆
    for new_block_line in blocks_line.sprites():
        for new_block in blocks.sprites():
            if new_block.rect.x==new_block_line.rect.x and \
                    new_block_line.rect.y-new_block.rect.height <= new_block.rect.y \
                    <= new_block_line.rect.y+new_block.rect.height:#遍历两个group，当方块碰到下方堆,结果为True
                col=new_block.rect.y+new_block.rect.height-new_block_line.rect.y#下降过多重叠部分像素
                for new_block in blocks.sprites():
                    new_block.rect.y-=col#校正像素
                return True
def transfer_blocks(blocks,blocks_line):#方块添加到底部堆
    for new_block in blocks.sprites():
        blocks_line.add(new_block)
        blocks.empty()
def check_collision(block,blocks,blocks_line):
    if check_collision_blocks_bottom(block,blocks) or check_collision_blocks_blocks_line(blocks,blocks_line):
        transfer_blocks(blocks,blocks_line)
        block.block_down_flag = True#按住down键，下一个出现的图形不会持续下降

def check_block_line_full(block,block_line):#消除
    count=[0]*(int(block.screen_rect.height/50))
    list_full=[]
    for y in range(0,block.screen_rect.height,50):#检测是否填满一行
        for new_block in block_line.sprites():
            if new_block.rect.y==y:
                count[int(y/50)]+=1
        if count[int(y/50)]==block.screen_rect.width/block.rect.width:
            list_full.append(y)
    for y in list_full:#删除填满的行
        for new_block in block_line.sprites():
            if new_block.rect.y==y:
                block_line.remove(new_block)
            elif new_block.rect.y<y:
                new_block.rect.y+=new_block.rect.height

def check_gameover(block_line,button):
    for new_block in block_line.sprites():
        if new_block.rect.y<=0:
            button.gameactive=False
            break