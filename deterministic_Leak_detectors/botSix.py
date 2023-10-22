import random

class bot6():
    
    def __init__(self, getGrid, detectionGrid, botpos, leakpos_1, leakpos_2):
        
        self.grid = getGrid
        self.detectionGrid = detectionGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        self.leakpos_2 = leakpos_2       
        self.bot_6_grid = [row.copy() for row in self.grid]
        
        for x in self.grid:
            print(''.join(x))
        print()
        
    
