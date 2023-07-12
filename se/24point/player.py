class Player:
    def __init__(self, name):
        self.name = name
        self.numcard = []  # 桌面的牌
        self._point = 0  # 桌面牌的点数和
        self.canchoose = True  # 是否能选择继续要牌

    @property
    def point(self):
        '''装饰器实现每次调用总点数时更新计算'''
        self._point = sum(self.numcard)
        return self._point

    def wantcard(self, settings):
        '''从牌库顶抽出一张牌，加入玩家桌面'''
        self.numcard.append(settings.numcard_list.pop())

    def choice(self, ch, settings):
        '''选择是否要牌'''
        if ch.upper() in ['Y', 'YES']:
            self.wantcard(settings)
            self.canchoose = True
        elif ch.upper() in ['N', 'NO']:
            self.canchoose = False
        # else:
        #     print('intut error')
        #     return self.choice(useAI,settings)
        if self.point >= settings.maxpoint:
            self.canchoose = False
