from itertools import combinations
import random
from helperMethod import *

class bot6():
    def __init__(self,k, getGrid, botpos, leakpos_1, leakpos_2):
    
        self.k = k
        self.leakpos_1 = leakpos_1
        self.leakpos_2 = leakpos_2       
        self.bot_6_grid = [row.copy() for row in getGrid]
        self.SENSOR = 0
        self.MOVES = 0
        self.combinations_dict = {}
        self.task_for_bot6(self.bot_6_grid, botpos)
    
    
    def task_for_bot6(self, grid, botpos):
        self.debug = False
        other_leak_found = False
        leak = 1
        open_cells = []
        
        # Creating Combinations
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "⬜️" or grid[x][y] == "🟥":
                    open_cells.append((x, y))
                    
        combinations_of_tuples = list(combinations(open_cells, 2))
        
        for pair in combinations_of_tuples:
            self.combinations_dict[pair] = 1
        leak_pair = (self.leakpos_1, self.leakpos_2)
        self.leak_found = []
        timeA = 0
        timeB = 0
        
        self.Priority_find = []
        
        while True:
            if self.debug: print("-----------------------------------------------------------------------")
            visited_cell_to_remove = []
            if botpos == self.leakpos_1 and leak == 2:
                break
            if botpos == self.leakpos_2 and leak == 2:
                break
            if botpos == self.leakpos_1 and leak == 1:
                self.Priority_find = []
                leakList = []
                leakList.append(self.leakpos_1)
                self.leak_found.append(self.leakpos_1)
                self.dict_clean_up(1, leakList)
                self.leakpos_1 = (99,99)
                
                leak+=1
                                
            if botpos == self.leakpos_2 and leak == 1:
                self.Priority_find = []
                leakList = []
                leakList.append(self.leakpos_2)
                self.leak_found.append(self.leakpos_2)
                self.dict_clean_up(1, leakList)
                self.leakpos_2 = (99,99)
                leak+=1
            
            # Everytime detection Grid Reset
            detectionGrid = []
            # Get the detction Grid using CreateDetector which takes an input of value k, 
            detectionGrid = CreateDetector(self.k, grid, botpos)
            # Sense the action of the leak in detection grid or not  
            self.SENSOR += 1

            if self.leakpos_1 in detectionGrid and self.leakpos_2 in detectionGrid:   
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and grid[x][y] != "✅":
                        grid[x][y] = "❌"
                    
                for (x,y) in detectionGrid:
                    if grid[x][y] == "❌":
                        self.Priority_find.append((x,y))
                        
                x1,y1 = leak_pair[0]
                grid[x1][y1] = "🟥"
                x2,y2 = leak_pair[1]
                grid[x2][y2] = "🟥"
                other_leak_found = True
            else:
                if self.leakpos_1 in detectionGrid:
                    timeA += 1
                    if timeA == 1:
                        for (x,y) in detectionGrid:
                            if (x,y) != botpos and (x,y) != self.leakpos_1 and grid[x][y] != "✅":
                                grid[x][y] = "❌"
                        
                        for (x,y) in detectionGrid:
                            if grid[x][y] == "❌":
                                self.Priority_find.append((x,y))
                        
                    other_leak_found = True
                    
                    
                if self.leakpos_2 in detectionGrid:
                    timeB += 1
                    if timeB == 1:        
                        for (x,y) in detectionGrid:
                            if (x,y) != botpos and (x,y) != self.leakpos_2 and grid[x][y] != "✅":
                                grid[x][y] = "❌"               
                        for (x,y) in detectionGrid:
                            if grid[x][y] == "❌":
                                self.Priority_find.append((x,y))                
                    other_leak_found = True 
                    
            if other_leak_found:
                i,j = botpos
                neighbors = get_neighbors(0, grid, i,j)
                grid[i][j] = "✅"
                if len(neighbors) != 0:
                    botpos = neighbors[random.randint(0,len(neighbors)-1)]
                    self.MOVES+=1 # UPDATE MOVES BOT POS
                    visited_cell_to_remove.append((botpos))
                else:
                    outcell_dict = {}
                    negative_cells = []
                    for x in range(len(grid)):
                        for y in range(len(grid)):
                            if grid[x][y] == "❌" or grid[x][y] == "🟥":
                                negative_cells.append((x,y))
                                self.Priority_find.append((x,y))
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
                    visited_cell_to_remove.append((botpos))
                    self.MOVES += outcell_dict[botpos]
                other_leak_found = False
            
            else:
                for (x,y) in detectionGrid:
                    if (x,y) != botpos or (x,y) not in leak_pair:
                        grid[x][y] = "✅"
                        visited_cell_to_remove.append((x,y))
                        if (x,y) in self.Priority_find:
                            self.Priority_find.remove((x,y))
                
                self.Priority_find = list(set(self.Priority_find))
                # print("Entered to get next move with botpos", botpos)
                endCell = self.get_next_move(self.combinations_dict, detectionGrid, botpos)
                if endCell:
                    if self.debug: print("EndCell Entered")
                    path = find_shortest_path(2, grid, 1, botpos, endCell)
                    if (self.leakpos_1 in path) or (self.leakpos_2 in path):
                        if self.leakpos_1 in path:
                            self.Priority_find = []
                            index = path.index(self.leakpos_1)
                            botpos = self.leakpos_1
                            # self.MOVES += (index-1)
                            leakList = []
                            leakList.append(self.leakpos_1)
                            self.dict_clean_up(1, leakList)
                            self.leak_found.append(self.leakpos_1)
                            self.leakpos_1 = (99,99)
                            leak += 1

                        if self.leakpos_2 in path:
                            self.Priority_find = []
                            index = path.index(self.leakpos_2)
                            botpos = self.leakpos_2
                            leakList = []
                            leakList.append(self.leakpos_2)
                            self.dict_clean_up(1, leakList)
                            self.leak_found.append(self.leakpos_2)
                            # self.MOVES += (index-1)
                            self.leakpos_2 = (99,99)
                            leak += 1
                        
                        if leak == 3:
                            for x,y in path:
                                grid[x][y] = "✅"
                            if self.debug: 
                                i,j = botpos
                                grid[i][j] = "😀"
                                for x in grid:
                                    print(''.join(x))
                                print()
                            break
                        
                    else:
                        for x,y in path:
                            grid[x][y] = "✅"
                            if (x,y) in self.Priority_find:
                                self.Priority_find.remove((x,y))
                        botpos = path[-1]
                        i,j = botpos
                        if len(self.Priority_find) != 0 :
                            if (i,j) in self.Priority_find:
                                self.Priority_find.remove((i,j))
                        self.MOVES += len(path)
                        visited_cell_to_remove.extend(path)
                else:
                    if self.debug: ("No EndCell Entered")
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
                    x_bot,y_bot = botpos
                    grid[x_bot][y_bot] = "✅"
                    # Get the minimum positive distance from botpos to nearest the outerlayer of the detection grid from the dictionary
                    botpos = min((k for k, v in outcell_dict.items() if v >= 0), key=outcell_dict.get, default=None)
                    # Steps needed to get the Outlayer of the detection Grid
                    # +1 is for to move to open cell form the outer layer of detection grid
                    self.MOVES += (outcell_dict[botpos] + 1)
                    openF = self.get_open(grid, botpos)
                    if len(openF) != 0: 
                        botpos = openF[0]
                    
                    i,j = botpos
                    if len(self.Priority_find) != 0 :
                        if (i,j) in self.Priority_find:
                            self.Priority_find.remove((i,j))
                    
                    
            if self.debug: 
                i,j = botpos
                grid[i][j] = "😀"
                for x in grid:
                    print(''.join(x))
                print()
                print(botpos)

            if visited_cell_to_remove:
                # print("before",len(self.combinations_dict))
                if leak_pair[0] in list(set(visited_cell_to_remove)):
                    visited_cell_to_remove.remove(leak_pair[0])
                if leak_pair[1] in list(set(visited_cell_to_remove)):
                    visited_cell_to_remove.remove(leak_pair[1])
                self.dict_clean_up(0, visited_cell_to_remove)
                # print("after",len(self.combinations_dict))


    # get next move for bot
    def get_next_move(self, combination_dict, detection, bot_pos):
        min_dist = float('inf')
        # print("Prioroty cell",self.Priority_find)
        # print("pos", bot_pos)
        if len(self.Priority_find) != 0:
            if bot_pos in self.Priority_find:
                x,y = bot_pos
                self.Priority_find.remove((x,y))
                
            # print("enteres priority", self.Priority_find)
            for item in list(set(self.Priority_find)):
                distance = self.find_distance(bot_pos,item)
                if min_dist > distance:
                    min_dist = distance
                    cell = item
            if cell:
                # print(cell)
                return cell
            else:
                return None
        
        cell_distance = {}
        for combination in list(combination_dict.keys()):
            if combination[0] not in detection:
                distance = self.find_distance(bot_pos, combination[0])
                if distance > self.k and distance <= 2 * self.k + 1 and (bot_pos[0] == combination[0][0] or bot_pos[1] == combination[0][1]):
                    cell_distance[combination[0]] = distance 
        if cell_distance:
            maxium = max((k for k, v in cell_distance.items() if v >= 0), key=cell_distance.get, default=None)
            if maxium :  
                return maxium
        else:
            return None
            # cellA, cellB = random.choice(list(self.combinations_dict.keys()))
            # if cellA not in self.leak_found:
            #     return cellA
            # else:
            #     return cellB                
            
    # Manhattan Distance
    def find_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1]-end[1])

    # dict clean up
    def dict_clean_up(self, index, remove_list):
        if index == 0:
            remove = []
            for item in remove_list:
                for keys in list(self.combinations_dict.keys()):
                    if item in keys:
                        remove.append(keys)
            for key in remove:
                if key in self.combinations_dict:
                    del self.combinations_dict[key]
        if index == 1:
            remove = []
            for item in remove_list:
                for keys in list(self.combinations_dict.keys()):
                    if item not in keys:
                        remove.append(keys)
            for key in remove:
                if key in self.combinations_dict:
                    del self.combinations_dict[key]
                    
    def get_open(self,  grid, bot):
            x,y = bot
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            # Open Cells
            return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❌")]
