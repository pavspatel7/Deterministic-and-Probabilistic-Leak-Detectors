import random
from helperMethod import CreateDetector, find_shortest_path, get_neighbors, create_mini_grid, outer_detection_cells

class bot1():
    
    def __init__(self, k,  getGrid, bot_pos, leakpos_1):
        
        self.grid = getGrid
        self.leakpos_1 = leakpos_1
        self.SENSOR = 0 # sensing counter
        self.MOVES = 0 # MOVES counter
        self.innerGridCells = []
        self.k = k
        self.debug = 0
        
        self.task_for_bot1(self.grid, bot_pos)
        
    def task_for_bot1(self, grid, bot_pos):
        t=0
        leak = 1
        outcell_dict = {}
        botpos = bot_pos
        detectionGrid = []
        type = True
        positive_cells = []
        negative_cells = []

        while True:
            # Everytime detection Grid Reset
            detectionGrid = []
            # Get the detction Grid using CreateDetector which takes an input of value k, 
            detectionGrid = CreateDetector(self.k, grid, botpos)
            if type:
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_1:
                        grid[x][y] = "✅"
                        positive_cells.append((x,y))

            # Print Layout
            if self.debug == 0:
                for x in grid:
                    print(' '.join(x))
                print()
          
            # Sense the action of the leak in detection grid or not  
            self.SENSOR += 1
            if self.leakpos_1 in detectionGrid:
                for x in range(len(grid)):
                    for y in range(len(grid)):
                        if grid[x][y] == "⬜️":
                            grid[x][y] = "🟧" 
                t+=1
                if t == 1:
                    for (x,y) in detectionGrid:
                        if (x,y) != botpos and (x,y) != self.leakpos_1:
                            grid[x][y] = "❎"
                for x in grid:
                    print(' '.join(x))
                print()  
                i,j = botpos
                neighbors = get_neighbors(0, grid, i,j)
                print(neighbors)
                grid[x_bot][y_bot] = "✅"
                if len(neighbors) != 0:
                    botpos = neighbors[random.randint(0,len(neighbors)-1)]
                else:
                    outcell_dict = {}
                    for x in range(len(grid)):
                        for y in range(len(grid)):
                            if grid[x][y] == "❎":
                                negative_cells.append((x,y))
                    for item in negative_cells:
                        l = find_shortest_path(2, grid ,1 ,botpos, item)
                        if l:
                            try:
                                l = int(l)
                                outcell_dict[item] = l  
                            except:
                                l = len(l)
                                outcell_dict[item] = l 
                    botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                    print("botpos",botpos)
                    print("outcell_dict",outcell_dict)
                    #botpos = self.get_open(1, grid, botpos)[0]
                    
                print("botpos", botpos)
                type = False
            else:
                type = True

            if type:
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_1:
                        grid[x][y] = "✅"
                        positive_cells.append((x,y))
                # If not then find the next position for the bot
                x_bot, y_bot = botpos
                outcell_dict = {}
                for item in outer_detection_cells(grid):
                    # From the botpos to all marked outer cell which has atleast one open cell - Running BFS and storng data
                    # into the dictionary with key = co-ordinates and values = length of the path
                    l = find_shortest_path(1, grid ,1 ,botpos, item)
                    if l:
                        # Try if the return value if -1 which means no path found from botpos to that item
                        try:
                            l = int(l)
                            outcell_dict[item] = l  
                        # Now, store the length of the BFS and increament the MOVES needed to reach teh cell
                        except:
                            l = len(l)
                            outcell_dict[item] = l 
                
                # Marked the visited cell - No Leak
                grid[x_bot][y_bot] = "✅"
                # Get the minimum positive distance from botpos to nearest the outerlayer of the detection grid from the dictionary
                botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                # Steps needed to get the Outlayer of the detection Grid
                # +1 is for to move to open cell form the outer layer of detection grid
                #print("outcells",outcell_dict)
                self.MOVES += (outcell_dict[botpos] + 1)
                botpos = self.get_open(grid, botpos)[0]
            
            if botpos == self.leakpos_1:
                print(botpos, self.leakpos_1)
                print("jehgbjekgv")
                print(f"Bot Found Leak in {self.SENSOR} sense actions and {self.MOVES} moves..")
                break
            else:
                # Distance changed from the current botpos, so assign dictionary value empty
                # outcell_dict = {}
                # Mark Last bot postion
                x_bot,y_bot = botpos
                grid[x_bot][y_bot] = "😀"

            # t += 1



    def get_open(self,  grid, bot):
        x,y = bot
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        # Open Cells
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❎")]

'''  
    # Helpers of Methods
    def get__neighbors(self, grid, bot):
        x,y = bot
        neighbors = []
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != "⬛️"]

    def confirm_leak(self, grid):
        botpos = None
        for x in grid:
            print(''.join(x))
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] == "😀":
                    botpos = (x,y)
        # print(botpos)
        # print(len(grid[0]), len(grid))
        while True:
            neighbors = self.get__neighbors(grid, botpos)
            print(neighbors)
            botpos = neighbors[random.randint(0,len(neighbors)-1)]
            if botpos == self.leakpos_1:
                break
            x_bot,y_bot = botpos
            grid[x_bot][y_bot] = "😀"
            Ngrid = CreateDetector(self.k, grid, botpos)
            if self.leakpos_1 not in Ngrid:
                for (x,y) in Ngrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_1:
                        grid[x][y] = "✅"
                
                # grid[x_bot][y_bot] = "✅"
                
            
        for x in grid:
            print(''.join(x))
'''