import random
from helperMethod import * 

class bot2():
    
    def __init__(self, k,  getGrid, bot_pos, leakpos_1):
        
        bot_2_grid = [row.copy() for row in getGrid]       # Grid
        self.leakpos_1 = leakpos_1                         # Leak Position 
        self.SENSOR = 0                                    # sensing counter
        self.MOVES = 0                                     # MOVES counter
        self.innerGridCells = []                           # Inner Grid cells 
        self.k = k                                         # K value
        self.debug = False                                 # debug default set to False
        self.task_for_bot2(bot_2_grid, bot_pos)            # Call Task for Bot 2
        
        
    def task_for_bot2(self, grid, bot_pos):
        time=0
        outcell_dict = {}              # Initialize Outer cell dictionary
        botpos = bot_pos               # Created a local bot postion
        detectionGrid = []             # Initialized Detection grid
        type = True                    # Type condition checker to run or not
        negative_cells = []            # Store all the potential leak cells

        # While will break when the botpos and leak position will be equal
        while botpos != self.leakpos_1:
            
            # Print Layout
            if self.debug:
                for x in grid:
                    print(''.join(x))
                print()
                print(self.MOVES, self.SENSOR)

            # Everytime detection Grid Reset
            detectionGrid = []
            # Get the detction Grid using CreateDetector which takes an input of value k, 
            detectionGrid = CreateDetector(self.k, grid, botpos)
          
            # Sense the action of the leak in detection grid or not  
            self.SENSOR += 1
            if self.leakpos_1 in detectionGrid:
                # Only Marking once if the leak is found
                time+=1
                if time == 1:
                    for (x,y) in detectionGrid:
                        if (x,y) != botpos and (x,y) != self.leakpos_1:
                            if grid[x][y] != "✅":
                                grid[x][y] = "❌"
                    # If we found the leak in the detection grid, then the other outer remaning 
                    # un-exlpore will automatically by marked as no leak
                    for x in range(len(grid)):
                        for y in range(len(grid)):
                            if grid[x][y] == "⬜️":
                                grid[x][y] = "✅" 
                # Mark visited bot postion as no leak
                i,j = botpos
                neighbors = get_neighbors(0, grid, i,j)
                grid[i][j] = "✅"
                # check if the length of the bot neighbor is not null
                # iF it is not null then get the random any neighbor and move towards it by increamenting moves
                if len(neighbors) != 0:
                    botpos = neighbors[random.randint(0,len(neighbors)-1)]
                    self.MOVES+=1 # UPDATE MOVES BOT POS
                else:
                    # If there are no neighbors found then, We will run BFS to the POTENTIAL CONTAINS LEAK cells
                    # those might have the leak, so sotred into the negative_cells finding the BFS to each items in negative cells
                    # from the current bot positon.  
                    outcell_dict = {}
                    negative_cells = []
                    for x in range(len(grid)):
                        for y in range(len(grid)):
                            if grid[x][y] == "❌" or grid[x][y] == "🟥":
                                negative_cells.append((x,y))
                    # Stored the values of the cells and thier distances into the otucell_dict dictionary
                    for item in negative_cells:
                        l = find_shortest_path(2, grid ,1 ,botpos, item)
                        if l:
                            try:
                                l = int(l)
                                outcell_dict[item] = l  
                            except:
                                l = len(l)
                                outcell_dict[item] = l 
                    # Picking an min distance cells from the bot pos from the dictionary and getting its key
                    botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                    # Increment its length od distance of move needed to reach the location
                    self.MOVES += outcell_dict[botpos]  # UPDATE MOVE BOT POS
                # Type is False means that there is still leak present inside the detection leak, 
                # until the bot move far from the leak and no leak present in detection grid the Type will be True
                type = False
            else:
                # Type = True (Means no leak found in detection grid)
                type = True

            # If No leak found in detection grid then this if statement will be execute
            if type:
                # Since there is no leak found then Mark all the cells in the detection grid to NO LEAK CONTAIN
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_1:
                        grid[x][y] = "✅"

                # If not then find the next position for the bot
                outcell_dict = {}
                # Find the next available position which is atleast at some distance from the current detection grid, it will allow to check more cells faster
                check = out_cells_bot_2(self.k, grid)
                # if there are no cell possible then it will run as bot-1 which means finding the nearest possible cell to explore
                if check:
                    for item in check:
                        l = find_shortest_path(2, grid, 1, botpos, item)
                        if l:       
                            # Try if the return value if -1 which means no path found from botpos to that item
                            try:
                                outcell_dict[item] = (len(l), l)
                            # Now, store the length of the BFS and increament the MOVES needed to reach teh cell
                            except:
                                l = len(l)
                                outcell_dict[item] = (len(l), l)
                    # Find the minimum distance and the path (p)
                    d,p = find_min_distance_and_path(outcell_dict)
                    # Check if the leak positon is in the path p
                    if self.leakpos_1 in p:
                        for (x,y) in p:
                            cell = (x,y)
                            if cell != self.leakpos_1:
                                # Find the exact location in the path and increament the moves needed to reach
                                grid[x][y] = "😀"
                                self.MOVES+=1
                            else:
                                # breka for loop
                                break
                        # break Main while loop
                        break
                    else:
                        x_bot,y_bot = bot_pos
                        grid[x_bot][y_bot] = "✅"
                        botpos = p[-1]
                        self.MOVES += len(p)
                # Continue as bot-1 if there no cell possible to minimize the Overlapping of the detection grid       
                else:
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
                    x_bot,y_bot = bot_pos
                    grid[x_bot][y_bot] = "✅"
                    # Get the minimum positive distance from botpos to nearest the outerlayer of the detection grid from the dictionary
                    botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                    # Steps needed to get the Outlayer of the detection Grid
                    # +1 is for to move to open cell form the outer layer of detection grid
                    self.MOVES += (outcell_dict[botpos] + 1)
                    botpos = self.get_open(grid, botpos)[0]
                    

            # Mark the bot location as visited
            x_bot,y_bot = botpos
            grid[x_bot][y_bot] = "😀"
            
            # Print Layout
            if self.debug:
                for x in grid:
                    print(''.join(x))
                print()
                print(self.MOVES, self.SENSOR)
        
        
        
    def get_open(self,  grid, bot):
        x,y = bot
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        # Open Cells
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❌")]
