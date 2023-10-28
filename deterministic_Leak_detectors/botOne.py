from operator import le
import random
from helperMethod import CreateDetector, find_shortest_path, get_neighbors, is_outer_detection, outer_detection_cells
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
        detection = CreateDetector(self.k, self.sizeOfDetectionGrid, self.grid, xbot, ybot)

        for x,y in detection:
            if (x,y) != self.botpos:
                self.grid[x][y] = "🟩"
        self.task_for_bot1()
        
    def task_for_bot1(self):
        t=0
        outcell_dict = {}
        while True:
            self.detectionGrid = list(set(self.detectionGrid))
            if self.leakpos_1 in self.detectionGrid:
                print("Check for the leak cell")
                break

            print(t)
            # Mark all to no Leak
            print("before loop")
            print(self.botpos)
            print(self.detectionGrid)
            
            for (x,y) in self.detectionGrid:
                if (x,y) != self.botpos:
                    self.grid[x][y] = "✅"
                    
            # find the next position
            x_bot, y_bot = self.botpos
            for item in outer_detection_cells(self.grid, self.detectionGrid):
                l = find_shortest_path(self.grid,1,self.botpos, item)
                if l:
                    try:
                        l = int(l)
                        outcell_dict[item] = l  
                    except:
                        l = len(l)
                        outcell_dict[item] = l  
            
            self.botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
            x_bot,y_bot = self.botpos
            
            self.detectionGrid = CreateDetector(self.k, self.sizeOfDetectionGrid, self.grid, x_bot,y_bot)
            self.grid[x_bot][y_bot] = "😀"
            
            self.botpos = (x_bot,y_bot)
                
                
            for x in self.grid:
                print(''.join(x))

            t += 1
            if t == 5:
                break
            
            
        
        
    
    def get_open(self, grid, bot):
        x,y = bot
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        open_neighor = [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥")]
        return open_neighor
    

'''

        while True:
            
            if t <= 0:
                for (x,y) in self.detectionGrid:
                    if (x,y) != self.botpos:
                        self.grid[x][y] = "✅" # Give marked Signal of SAFE  
                          
            # check for the neighbors:
            x_bot, y_bot = self.botpos
            outpos = random.choice(outer_detection_cells(self.grid, self.detectionGrid))
            while True:
                path = find_shortest_path(self.grid, 1, self.botpos , outpos)
                if path:
                    while len(path) != 0:
                        dx,dy = path.pop(0)
                        self.grid[dx][dy] = "😀"
                        x_bot,y_bot = dx,dy
                    
                    x_bot, y_bot = random.choice(self.get_open(self.grid,x_bot,y_bot))
                    self.grid[x_bot][y_bot] = "😀"
                    break
                else:
                    outpos = random.choice(outer_detection_cells(self.grid, self.detectionGrid))
            self.detectionGrid = CreateDetector(self.k, self.sizeOfDetectionGrid, self.grid, x_bot,y_bot)
            
            for (x,y) in self.detectionGrid:
                self.botpos = x_bot,y_bot
                if (x,y) != self.botpos:
                    self.grid[x][y] = "✅"
        
            self.SENSOR+=1
            if self.leakpos_1 in self.detectionGrid:
                for (x,y) in self.detectionGrid:
                    if (x,y) != self.leakpos_1:
                        self.grid[x][y] = "❎" # Give marked Signal of RISK
                while True:
                    Botneighbors = []
                    x_bot, y_bot = self.botpos
                    Botneighbors = get_neighbors(self.grid,x_bot,y_bot)
                    self.botpos = Botneighbors[random.randint(0, len(Botneighbors)-1)]
                    if self.botpos == self.leakpos_1:
                        print(f"Bot-1 Found leak in {self.MOVES} moves and {self.SENSOR} sense")
                        breakT = 1
                        break     
                if breakT == 1:
                    break
        
            for x in self.grid:
                print(''.join(x))

'''