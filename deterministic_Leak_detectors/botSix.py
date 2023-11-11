import random
from types import NoneType
from helperMethod import *

class bot6():
    def __init__(self,k, getGrid, botpos, leakpos_1, leakpos_2):
        
        self.grid = getGrid
        self.k = k
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        self.leakpos_2 = leakpos_2       
        self.bot_6_grid = [row.copy() for row in self.grid]
        self.SENSOR = 0
        self.MOVES = 0
        self.debug = 0
        self.combination_dict = self.get_dict(self.bot_6_grid)
        self.potential_leak_1 = []
        self.potential_leak_2 = []
        self.leakFound = False
        self.flag = False
        self.yes = False

        self.task_for_bot6(self.bot_6_grid, self.botpos)
        
        
        
    def task_for_bot6(self, grid, bot_pos):
        t=0
        m=0
        leak = 1
        outcell_dict = {}
        botpos = bot_pos
        detectionGrid = []
        type = True
        negative_cells = []
        Alldone = []
        self.checking = False
        while True:
            # print("--------------------------------------------------------------------")


            if botpos == self.leakpos_1 and leak == 2:
                print("both found in 1")
                break
            if botpos == self.leakpos_2 and leak == 2:
                print("both found in 2")
                break
            if botpos == self.leakpos_1 and leak == 1:
                print("leak 1 found")
                keys_to_delete = []
                
                for combination in list(self.combination_dict.keys()):
                    if self.leakpos_1 == combination[0]:
                        self.combination_dict[combination] = 10
                        continue
                    else:
                        keys_to_delete.append(combination)

                for key in keys_to_delete:
                    del self.combination_dict[key]
                
                # for keys, items in self.combination_dict.items():
                #     print(keys, items)
                
                self.checking = True
                self.leakFound = True
                self.leakpos_1 = (99,99)
                leak+=1
                                
            if botpos == self.leakpos_2 and leak == 1:
                print("leak 2 found")
                # self.delete_combinations(self.leakpos_2)
                keys_to_delete = []
                
                for combination in list(self.combination_dict.keys()):
                    if self.leakpos_2 == combination[0]:
                        self.combination_dict[combination] = 10
                        continue
                    else:
                        keys_to_delete.append(combination)

                for key in keys_to_delete:
                    del self.combination_dict[key]
                
                # for keys, items in self.combination_dict.items():
                #     print(keys, items)

                self.leakFound = True
                self.checking = True
                self.leakpos_2 = (99,99)
                leak+=1
            
            # Print Layout
            if self.debug == 1:
                for x in grid:
                    print(''.join(x))
                print()
                # print(self.MOVES, self.SENSOR)
            if leak == 3:
                print("break up")
                break

            # Everytime detection Grid Reset
            detectionGrid = []
            # Get the detction Grid using CreateDetector which takes an input of value k, 
            detectionGrid = CreateDetector(self.k, grid, botpos)

            # Sense the action of the leak in detection grid or not  
            self.SENSOR += 1
            if (self.leakpos_1 in detectionGrid) or (self.leakpos_2 in detectionGrid):
                
                if self.leakpos_1 in detectionGrid:
                    t+=1
                    if t == 1:
                        for (x,y) in detectionGrid:
                            if (x,y) != botpos and (x,y) != self.leakpos_1:
                                if grid[x][y] != "✅" and grid[x][y] != "🟥":
                                    grid[x][y] = "❌"
                                    
                    if self.checking:
                        for x in range(len(grid)):
                            for y in range(len(grid)):
                                if grid[x][y] == "⬜️":
                                    grid[x][y] = "✅" 
                                    Alldone.append((x,y))
                        delete_cell = []    
                        for combination in list(self.combination_dict.keys()):
                            if any (cells in Alldone for cells in combination) and self.combination_dict[combination] != 10:
                                delete_cell.append(combination)
                            else:
                                continue
                        for combinations in delete_cell:
                            del self.combination_dict[combinations]
                        Alldone = []
                
                if self.leakpos_2 in detectionGrid:
                    m+=1
                    if m == 1:
                        for (x,y) in detectionGrid:
                            if (x,y) != botpos and (x,y) != self.leakpos_2:
                                if grid[x][y] != "✅" and grid[x][y] != "🟥":
                                    grid[x][y] = "❌"

                    if self.checking:
                        for x in range(len(grid)):
                            for y in range(len(grid)):
                                if grid[x][y] == "⬜️":
                                    grid[x][y] = "✅" 
                                    Alldone.append((x,y))
                        delete_cell = []    
                        for combination in list(self.combination_dict.keys()):
                            if any (cells in Alldone for cells in combination) and self.combination_dict[combination] != 10:
                                delete_cell.append(combination)
                            else:
                                continue
                        for combinations in delete_cell:
                            del self.combination_dict[combinations]

                i,j = botpos
                neighbors = get_neighbors(0, grid, i,j)
                grid[x_bot][y_bot] = "✅"
                
                if len(neighbors) != 0:
                    botpos = neighbors[random.randint(0,len(neighbors)-1)]
                    x_bot, y_bot = botpos
                    self.MOVES+=1 # UPDATE MOVES BOT POS
                else:
                    # keys_with_value_5 = [key for key, value in self.combination_dict.items() if value == 5]
                    # botpos = random.choice(keys_with_value_5)[0]  
                    # print("botpos", botpos)  
                    # botpos = self.priority_cell(detection = True, bot_pos=botpos)
                    # x_bot, y_bot = botpos
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
                    self.MOVES += outcell_dict[botpos]  # UPDATE MOVE BOT POS
                    
                    
                    
                type = False
            else:
                type = True



            if type:
                
                # If not leak found in detection then mark all safe
                # similarly remove from the combination grid
                for (x,y) in detectionGrid:
                    if (x,y) != self.leakpos_1 or (x,y) != self.leakpos_2:
                        grid[x][y] = "✅"
                x_bot, y_bot = botpos
                
                if self.debug == 1:
                    print("before len of dict", len(self.combination_dict))
                    print("detection grid === ",detectionGrid)
                keys_to_delete = []
                
                for combination in list(self.combination_dict.keys()):
                    if any(cell in detectionGrid for cell in combination) and self.combination_dict[combination] != 10:
                        keys_to_delete.append(combination)

                for key in keys_to_delete:
                    del self.combination_dict[key]
                if self.debug == 1:
                    print("botpos", botpos)
                    print("combination dict ===",self.combination_dict)
                    print("after len of dict", len(self.combination_dict))
                    print()
                
                N_botpos = self.priority_cell(detection= False, bot_pos=botpos)
                if N_botpos:
                    
                    # print("Yes N_bopos")
                    path = find_shortest_path(2, grid, 1, botpos, N_botpos)
                    # print(path)
                else:
                    # print("No N_bopos")
                    self.yes = True
                    N_botpos = self.priority_cell(detection= NoneType, bot_pos=botpos)
                    path = find_shortest_path(2, grid, 1, botpos, N_botpos)
                    # print(path)
                    self.yes = False
                while len(path) != 0:
                    botpos = path.pop(0)
                    x,y = botpos
                        
                    if botpos == self.leakpos_1:
                        leak += 1
                        print("leak 1 found in p")
                        keys_to_delete = []
                        
                        for combination in list(self.combination_dict.keys()):
                            if self.leakpos_1 == combination[0]:
                                self.combination_dict[combination] = 10
                                continue
                            else:
                                keys_to_delete.append(combination)

                        for key in keys_to_delete:
                            del self.combination_dict[key]
                        
                        # for keys, items in self.combination_dict.items():
                        #     print(keys, items)
                            
                        self.leakFound = True
                        # self.delete_combinations(self.leakpos_1)
                        self.leakpos_1 = (99,99)
                        break
                    elif botpos == self.leakpos_2:
                        leak += 1
                        # self.delete_combinations(self.leakpos_2)
                        
                        keys_to_delete = []
            
                        for combination in list(self.combination_dict.keys()):
                            if self.leakpos_2 == combination[0]:
                                self.combination_dict[combination] = 10
                                continue
                            else:
                                keys_to_delete.append(combination)

                        for key in keys_to_delete:
                            del self.combination_dict[key]
                        
                        # for keys, items in self.combination_dict.items():
                        #     print(keys, items)
                            
                        print("leak 2 found in p")
                        self.leakFound = True
                        self.leakpos_2 = (99,99)
                        break
                    
                    if leak == 3:
                        print("break down")
                        break                                            
                    # print('*********************')
                    # print(botpos)
                    # print("------B check----")
                    # for keys, items in self.combination_dict.items():
                    #     print(keys, items)
                    # print("------A check----")
                    
                    keys_to_delete = []
                    for keys in list(self.combination_dict.keys()):
                        if (x,y) in keys and (x,y) != keys[0] :
                            keys_to_delete.append(keys)
                    for key in keys_to_delete:
                            del self.combination_dict[key]
                    

            # Mark the bot location as visited
            x_bot,y_bot = botpos
            grid[x_bot][y_bot] = "😀"
            
            # Print Layout
            if self.debug == 1:
                for x in grid:
                    print(''.join(x))
                print()
                print(botpos)
                # print(self.MOVES, self.SENSOR)
                
                
        
    def get_open(self,  grid, bot):
        x,y = bot
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        # Open Cells
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❌")]

    def priority_cell(self, detection, bot_pos):
        
        if self.yes:
            distance = []
            possible_locations = set()
            for combinations in list(self.combination_dict.keys()):
                if bot_pos != combinations[0] and self.combination_dict[combinations] != 10:
                    distance.append( (combinations[0] , self.find_distance(bot_pos, combinations[0])) )
                if bot_pos != combinations[1] and self.combination_dict[combinations] == 10:
                    distance.append( (combinations[1] , self.find_distance(bot_pos, combinations[1])) )
            go_to_priority_cell = min(distance, key=lambda x: x[1])[0]
            return go_to_priority_cell
        
        if detection:
            print("Entered")
            possible_locations = set()
            # print(self.combination_dict)
            
            min_distance = float('inf')
            for combinations in list(self.combination_dict.keys()):
                if bot_pos != combinations[0] and bot_pos != combinations[0]:
                    # if combinations[0] != combinations[1]:
                    distance = self.find_distance(bot_pos, combinations[0])
                    if min_distance > distance:
                        min_distance = distance
                        go_to_priority_cell = combinations[1]
                    
            return go_to_priority_cell
        
        else:
            if not self.leakFound:
                possible_locations = set()
                for combinations in list(self.combination_dict.keys()):
                    distance = self.find_distance(bot_pos, combinations[0])
                    if 2 * self.k + 1 >= distance > 2 * self.k:
                        possible_locations.add(combinations[0])
                possible_locations = list(possible_locations)
                if possible_locations:
                    go_to_priority_cell = possible_locations[random.randint(0, len(possible_locations) - 1)]
                else:
                    go_to_priority_cell = None
                return go_to_priority_cell
            else:
                possible_locations = set()
                for combinations in list(self.combination_dict.keys()):
                    distance = self.find_distance(bot_pos, combinations[1])
                    if 2 * self.k + 1 >= distance > 2 * self.k:
                        possible_locations.add(combinations[1])
                possible_locations = list(possible_locations)
                if possible_locations:
                    go_to_priority_cell = possible_locations[random.randint(0, len(possible_locations) - 1)]
                else:
                    go_to_priority_cell = None
                return go_to_priority_cell
        
        
        
    def find_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1]-end[1])
    
    
    def get_dict(self, grid):
        my_dict = {}
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] != "⬛️":
                    for i in range(len(grid)):
                        for j in range(len(grid)):
                            if (x,y) != (i,j) and grid[i][j] != "⬛️":
                                my_dict[((x, y), (i, j))] = 1
        return my_dict
    
    def delete_combinations(self, leak_pos):
        
        # print("Entered to detele")
        keys_to_delete = []
        for combination in list(self.combination_dict.keys()):
            if leak_pos == combination[0]:
                self.combination_dict[combination] = 10
            else:
                keys_to_delete.append(combination)

        for key in keys_to_delete:
            del self.combination_dict[key]
        
        # for keys, items in self.combination_dict.items():
        #     print(keys, items)