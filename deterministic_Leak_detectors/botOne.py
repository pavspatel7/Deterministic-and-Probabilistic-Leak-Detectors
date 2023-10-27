import random
from helperMethod import help
class bot1():
    
    def __init__(self, k, sizeOfDetectionGrid,  getGrid, detectionGrid, botpos, leakpos_1):
        
        self.grid = getGrid
        self.detectionGrid = detectionGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        self.SENSOR = 0 # sensing counter
        self.MOVES = 0 # MOVES counter
        self.innerGridCells = []
        self.k = k
        self.sizeOfDetectionGrid = sizeOfDetectionGrid
        xbot, ybot = botpos
        detection = help.CreateDetector(self.k, self.sizeOfDetectionGrid, self.grid, xbot, ybot)

        for x,y in detection:
            if (x,y) != self.botpos:
                self.grid[x][y] = "🟩"
        self.task_for_bot1()
        
    def task_for_bot1(self):
        t=0
        while True:
            self.SENSOR+=1
            if self.leakpos_1 in self.detectionGrid:
                for (x,y) in self.detectionGrid:
                    if (x,y) != self.leakpos_1:
                        self.grid[x][y] = "❎" # Give marked Signal of RISK
                while True:
                    Botneighbors = []
                    x_bot, y_bot = self.botpos
                    Botneighbors = help.get_neighbors(self.grid,x_bot,y_bot)
                    self.botpos = Botneighbors[random.randint(0, len(Botneighbors)-1)]
                    if self.botpos == self.leakpos_1:
                        print(f"Bot-1 Found leak in {self.MOVES} moves and {self.SENSOR} sense")
                        breakT = 1
                        break     
                if breakT == 1:
                    break
            else:
                for (x,y) in self.detectionGrid:
                    if (x,y) != self.botpos:
                        self.grid[x][y] = "✅" # Give marked Signal of SAFE                    
                # check for the neighbors:
                x_bot, y_bot = self.botpos
                while True:
                    Botneighbors = help.get_neighbors(self.grid,x_bot,y_bot)
                    self.botpos = Botneighbors[random.randint(0, len(Botneighbors)-1)]
                    self.MOVES += 1
                    x_bot,y_bot = self.botpos
                    if self.grid[x_bot][y_bot] == "⬜️": 
                        break
                self.detectionGrid = help.CreateDetector(self.k, self.sizeOfDetectionGrid, self.grid, x_bot,y_bot)
            for x in self.grid:
                print(''.join(x))
            t+=1
            if t == 3:
                break
            print()
    