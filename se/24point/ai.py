import game_func
class Ai: #ai不作弊，不知道对方底牌
    def __init__(self):
        pass

    def ai_1(self,settings,p1,p2):
        '''判断自己再抽一张牌爆牌的概率 '''
        want=0
        leftcard=list(range(1,12)) #初始牌库
        showcard=p1.numcard+p2.numcard[1:] #桌面的明牌
        for card in showcard:
            leftcard.remove(card) #剩余牌库
        for card in leftcard:
            want+=1 if p1.point+card<=settings.maxpoint else -1 #再抽一张牌不爆牌+1，爆牌-1
        return want if want>=0 else False

    def ai_2(self,settings,p1,p2):
        '''判断再抽一张牌获胜的概率'''
        leftcard=list(range(1,12)) #初始牌库
        showcard=p1.numcard+p2.numcard[1:] #桌面的明牌
        for card in showcard:
            leftcard.remove(card) #剩余牌库
        win_nomore=0 #不要牌赢的概率
        for p2card in leftcard:
            p2guess=p2card+sum(p2.numcard[1:]) #p2guess:p2可能的点数
            if p2guess>=15:
                continue
            win_nomore+=1 if game_func.checkwinner(p1.point,p2guess,settings,p1,p2)==p1.name else -1
        win_another=0 #要牌赢的概率
        for p2card in leftcard:
            p2guess = p2card + sum(p2.numcard[1:])
            if p2guess>=15:
                continue
            leftcardcopy=leftcard.copy()
            leftcardcopy.remove(p2card)
            for p1card in leftcardcopy:
                p1_newpoint=p1.point+p1card
                win_another += 1 if game_func.checkwinner(p1_newpoint, p2guess,settings,p1,p2) == p1.name else -1
        return (win_nomore,win_another) if win_another>=win_nomore else False
    def ai(self,settings,p1,p2):
        if self.ai_1(settings,p1,p2):
            return 'y'
        elif self.ai_2(settings,p1,p2) and self.ai_2(settings,p1,p2)[0]<0: #原本输的概率就大，抽排后赢的概率增加或不变
            return 'y'
        else: #原本赢的概率就大（再抽排有爆牌风险），或者抽排后赢的概率减小
            return 'n'