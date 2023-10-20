import random
from tkinter import Grid
from layout import runMain

class bot1():
    def __init__(self):
        self.grid , self.bot_pos , self.leak_pos = runMain()    
        self.bot_1_grid = [row.copy() for row in self.grid]
        self.getBot_1()
        self.VisitedNeighbors = []
        
    def getBot_1(self):
        time = 1
        while True:
            for x in self.bot_1_grid:
                print(''.join(x))
            print()
            if (self.bot_pos) == (self.leak_pos):
                print(self.bot_pos , self.leak_pos)
                print("Leak Found")
                break
            x,y = self.bot_pos
            Bot_neighbors = self.get_neighbors(x,y)
            self.bot_pos = Bot_neighbors[random.randint(0,len(Bot_neighbors)-1)]
            x,y = self.bot_pos
            self.bot_1_grid[x][y] = "🟩"
            self.VisitedNeighbors.append((x,y))
            time+=1
        
        print(F"Leak Found Bot-1 in {time} time stamp")
    
    def get_neighbors(self, x, y):
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(self.bot_1_grid) and 0 <= ny < len(self.bot_1_grid) and self.bot_1_grid[nx][ny] != "⬛️" and self.bot_1_grid[nx][ny] != "🟩"]

# bot1()