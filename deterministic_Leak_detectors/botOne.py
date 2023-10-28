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
        self.task_for_bot1(bot_pos)
        
    def task_for_bot1(self, bot_pos):
        t=0
        leak = 1
        outcell_dict = {}
        botpos = bot_pos
        detectionGrid = []
        while True:
            # Everytime detection Grid Reset
            detectionGrid = []
            # Get the detction Grid using CreateDetector which takes an input of value k, 
            detectionGrid = CreateDetector(self.k, self.grid, botpos)
            for (x,y) in detectionGrid:
                if (x,y) != botpos and (x,y) != self.leakpos_1:
                    self.grid[x][y] = "✅"

            # Print Layout
            if self.debug == 1:
                for x in self.grid:
                    print(' '.join(x))
                print()

            # Now check if the leak is in detectionGrid ?  
            # REMANING TO FIND THE EXACT LOCATION INSIDE THE DETECTION            
            # Sense the action of the leak in detection grid or not  
            self.SENSOR += 1
            if self.leakpos_1 in detectionGrid:
                
                if self.debug == 0:
                    for (x,y) in detectionGrid:
                        if (x,y) != botpos and (x,y) != self.leakpos_1:
                            self.grid[x][y] = "❎"
                    for x in self.grid:
                        print(' '.join(x))
                    print()  
                
                # Confirm the exact location
                # self.confirm_leak(self.SENSOR, self.MOVES, grid, botpos)

                miniGrid = create_mini_grid(self.k, self.grid, botpos)
                for x in miniGrid:
                    print(''.join(x))

                if leak == 1:
                    print(f"Bot Found Leak in {self.SENSOR} sense actions and {self.MOVES} moves..")
                    break

            # If not then find the next position for the bot
            x_bot, y_bot = botpos
            for item in outer_detection_cells(self.grid):
                # From the botpos to all marked outer cell which has atleast one open cell - Running BFS and storng data
                # into the dictionary with key = co-ordinates and values = length of the path
                l = find_shortest_path(self.grid,1,botpos, item)
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
            self.grid[x_bot][y_bot] = "✅"
            # Get the minimum positive distance from botpos to nearest the outerlayer of the detection grid from the dictionary
            botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
            # Steps needed to get the Outlayer of the detection Grid
            # +1 is for to move to open cell form the outer layer of detection grid
            self.MOVES += (outcell_dict[botpos] + 1)
            botpos = self.get_open(self.grid, botpos)[0]
            # Distance changed from the current botpos, so assign dictionary value empty
            outcell_dict = {}
            # Mark Last bot postion
            x_bot,y_bot = botpos
            self.grid[x_bot][y_bot] = "😀"

            t += 1

    def get_open(self, grid, bot):
        x,y = bot
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥")]


    def confirm_leak(self, grid, botpos):
        neighbors = get_neighbors(grid, botpos)
        u_detectiongrid = []
        while True:
            if len(neighbors) != 0:
                u_botpos = neighbors[random.randint(0, len(neighbors)-1)]
            u_detectiongrid = CreateDetector(self.k, self.grid, u_botpos)
            if self.leakpos_1 in u_detectiongrid:
                break
            
            if (u_botpos == self.leakpos_1) :
                print("Found")  
    
