import random

list_all = ['A', 'J', 'Q', 'K']
for i in range(2, 11):
    list_all.append(i)
list_all *= 4
list_card4 = random.sample(list_all, 4)
# list_card4=[3,3,7,7]
print(list_card4)
list_op = ['+', '-', '*', '/']
sc1, sc2, sc3, sc4, so1, so2, so3 = None, None, None, None, None, None, None
for i in range(4):
    # print(list_card4)
    sc4 = list_card4[i]
    list_card3 = list_card4.copy()
    list_card3.remove(list_card4[i])
    # print(list_card3)
    for i in range(3):
        sc3 = list_card3[i]
        list_card2 = list_card3.copy()
        list_card2.remove(list_card3[i])
        # print(list_card2)
        for i in range(2):
            sc2 = list_card2[i]
            list_card1 = list_card2.copy()
            list_card1.remove(list_card2[i])
            # print(list_card1)
            sc1 = list_card1[0]

            for i in range(4):
                so1 = list_op[i]
                for i in range(4):
                    so2 = list_op[i]
                    for i in range(4):
                        so3 = list_op[i]

                        ari1 = str('(' + '(' + str(sc1) + so1 + str(sc2) + ')' + so2 + str(sc3) + ')' + so3 + str(sc4))
                        ari2 = str('(' + str(sc1) + so1 + str(sc2) + ')' + so2 + '(' + str(sc3) + so3 + str(sc4) + ')')
                        A, J, Q, K = 1, 11, 12, 13
                        result1 = eval(ari1)
                        if result1 == 24:
                            print(ari1 + ' = 24')
                        try:
                            result2 = eval(ari2)
                            if result2 == 24:
                                print(ari2 + ' = 24')
                        except ZeroDivisionError:
                            pass
