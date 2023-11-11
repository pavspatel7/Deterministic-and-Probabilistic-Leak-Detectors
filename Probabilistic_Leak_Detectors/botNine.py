import random

class bot9():
    
    def __init__(self, getGrid, botpos, leakpos_1, leakpos_2, alpha):
        
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        self.leakpos_2 = leakpos_2
        self.alpha = alpha
        self.bot_9_grid = [row.copy() for row in getGrid]
        self.SENSOR = 0
        self.MOVES = 0
        for x in self.bot_9_grid:
            print(''.join(x))
        print()
        self.task_for_bot9(self.bot_9_grid, botpos, leakpos_1, leakpos_2, alpha)

    def task_for_bot9(self, grid, botpos, leakpos_1, leakpos_2, alpha):
        pass