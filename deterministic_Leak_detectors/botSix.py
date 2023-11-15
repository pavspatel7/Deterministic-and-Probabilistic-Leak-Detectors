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
        
        while True:
            visited_cell_to_remove = []
            if botpos == self.leakpos_1 and leak == 2:
                break
            if botpos == self.leakpos_2 and leak == 2:
                break
            if botpos == self.leakpos_1 and leak == 1:
                leakList = []
                leakList.append(self.leakpos_1)
                self.dict_clean_up(leakList)
                self.leakpos_1 = (99,99)
                leak+=1
                                
            if botpos == self.leakpos_2 and leak == 1:
                leakList = []
                leakList.append(self.leakpos_2)
                self.dict_clean_up(leakList)
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
                        
                x1,y1 = leak_pair[0]
                grid[x1][y1] = "🟥"
                x2,y2 = leak_pair[1]
                grid[x2][y2] = "🟥"
                other_leak_found = True
            
            if self.leakpos_1 in detectionGrid:
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_1 and grid[x][y] != "✅":
                        grid[x][y] = "❌"
                other_leak_found = True
            
            if self.leakpos_2 in detectionGrid:        
                for (x,y) in detectionGrid:
                    if (x,y) != botpos and (x,y) != self.leakpos_2 and grid[x][y] != "✅":
                        grid[x][y] = "❌"                               
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
                
                endCell = self.get_next_move(self.combinations_dict, detectionGrid, botpos)
                path = find_shortest_path(2, grid, 1, botpos, endCell)
                
                if (self.leakpos_1 in path) or (self.leakpos_2 in path):
                    if self.leakpos_1 in path:
                        index = path.index(self.leakpos_1)
                        botpos = self.leakpos_1
                        self.MOVES += (index-1)
                        leakList = []
                        leakList.append(self.leakpos_1)
                        self.dict_clean_up(leakList)
                        self.leakpos_1 = (99,99)
                        leak += 1

                    if self.leakpos_2 in path:
                        index = path.index(self.leakpos_2)
                        botpos = self.leakpos_2
                        leakList = []
                        leakList.append(self.leakpos_2)
                        self.dict_clean_up(leakList)
                        self.MOVES += (index-1)
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
                    botpos = path[-1]
                    self.MOVES += len(path)
                    visited_cell_to_remove.extend(path)

            if self.debug: 
                i,j = botpos
                grid[i][j] = "😀"
                for x in grid:
                    print(''.join(x))
                print()
                print(botpos)

            if visited_cell_to_remove:
                if leak_pair[0] in list(set(visited_cell_to_remove)):
                    visited_cell_to_remove.remove(leak_pair[0])
                if leak_pair[1] in list(set(visited_cell_to_remove)):
                    visited_cell_to_remove.remove(leak_pair[1])
                self.dict_clean_up(visited_cell_to_remove)

    # get next move for bot
    def get_next_move(self, combination_dict, detection, bot_pos):
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
            return random.choice(list(self.combinations_dict.keys()))[1]

    # Manhattan Distance
    def find_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1]-end[1])

    # dict clean up
    def dict_clean_up(self, remove_list):
        remove = []
        for item in remove_list:
            for keys in list(self.combinations_dict.keys()):
                if item in keys:
                    remove.append(keys)
        for key in remove:
            if key in self.combinations_dict:
                del self.combinations_dict[key]
