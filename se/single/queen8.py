# -*- coding: utf-8 -*-
# date: 2024-5-22
def queen(n=8):
    state = []

    def conflict(nextpos):
        for index, pos in enumerate(state):
            if nextpos == pos or abs(index - len(state)) == abs(pos - nextpos):
                return True
        return False

    def backtract():
        if len(state) == n:
            print(state)
            return
        for nextpos in range(n):
            if not conflict(nextpos):
                state.append(nextpos)
                backtract()
                state.remove(nextpos)

    backtract()


queen()
