import random
from helperMethod_bot8 import *

class bot9():
    
    def __init__(self, getGrid, botpos, leakpos_1, leakpos_2, alpha):
        
        self.bot_9_grid = [row.copy() for row in getGrid]
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        self.leakpos_2 = leakpos_2
        
        # temp grid
        self.MOVES = 0
        self.SENSOR = 0
        
        self.task_for_bot9(self.bot_9_grid, botpos, leakpos_1, leakpos_2, alpha)

    def task_for_bot9(self, grid, botpos, leakpos_1, leakpos_2, alpha):
        debug = False
        leaks_to_find = [leakpos_1, leakpos_2]
        # probability matrix
        cell_pair_probability_dict = {}
        opent = 0
        nobeepflag = True
        leak_time = 0
        leaks_found = []

        if debug:
            for x in grid:
                print(''.join(x))
            print()

        # Create a list of open_cell pairs
        open_cells = []
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "⬜️" or grid[x][y] == "🟥":
                    opent += 1
                    open_cells.append((x, y))
        keys = []
        keys.extend(open_cells)
        num_open_cells_pair = opent*(opent-1)/2
        cell_pairs = [(keys[i], keys[j]) for i in range(len(keys)) for j in range(i+1, len(keys))]
        
        # In dictionary storing the cell pair as ((x1,y1), (x2,y2)) as key and probabilities as value:
        # -> For Each pair of open cells by default probability is 1 / total pairs of open cells
        for pair in cell_pairs:
            cell_pair_probability_dict[pair] = 1/num_open_cells_pair
        if debug: print( "Num Pairs initial: {}".format(len(cell_pair_probability_dict)))
        
        cell_pair_probability_dict = leak_in_i_j_given_no_leak_in_k(cell_pair_probability_dict, botpos)

        while True:

            if nobeepflag:
                check = 1
            else:
                check = alpha*30
            
            if check < 1:
                check = 1

            # precalculate distances from botpos to all other locations
            # this is achieved using Dijkstra's algorithm
            distances = all_distances_bfs(2, grid, 1, botpos)
            
            # Delete unwanted items from dict to improve efficiency
            clean_up(cell_pair_probability_dict)
            
            count = 0
            nobeepTimes = 0
            while count < check:
                # P(beep in k | leaks in actual leaks location)
                curr_beep_prob = beep_in_k_given_leak_in_i_and_j(alpha, grid, botpos, self.leakpos_1, self.leakpos_2, distances)
                # generate a random number to compare
                rand = random.uniform(0, 1)
                self.SENSOR += 1
                # determine beep or no beep
                curr_beep = rand <= curr_beep_prob
                if curr_beep:
                    if debug: print("beep")
                    # P(leak in i, j | beep in k)
                    cell_pair_probability_dict = prob_leak_given_beep(alpha, grid, cell_pair_probability_dict, botpos, distances)
                    if nobeepflag:
                        nobeepflag = False
                    break
                else:
                    if debug: print("no beep")
                    nobeepTimes += 1
                    # P(leak in i, j | no beep in k)
                    cell_pair_probability_dict = prob_leak_given_no_beep(alpha, grid, cell_pair_probability_dict, botpos, distances)
                    if(count >= check-1 and count == nobeepTimes):
                        nobeepflag = True
                count += 1

            # plan a path towards high probability cell with short path from botpos in grid
            max_value = max(cell_pair_probability_dict.values())
            if debug: print("Max prob is:", max_value)
            max_prob_pairs = [k for k, v in cell_pair_probability_dict.items() if v == max_value]
            # Create dict to store individual cell probabilities for possible choice cells
            cell_probability_dict = {}
            if debug: print("Max prob pairs {}".format(len(max_prob_pairs)))
            for pair in max_prob_pairs:
                if pair[0] not in leaks_found and pair[0] not in cell_probability_dict.keys():
                    cell_probability_dict[pair[0]] = get_cell_probability(cell_pair_probability_dict, pair[0])
                if pair[1] not in leaks_found and pair[1] not in cell_probability_dict.keys():
                    cell_probability_dict[pair[1]] = get_cell_probability(cell_pair_probability_dict, pair[1])    
            max_value = max(cell_probability_dict.values())
            max_keys = [k for k, v in cell_probability_dict.items() if v == max_value]
            min_path_len = float('inf')
            for key in max_keys:  
                path_len = distances.get(key, float('inf'))
                if min_path_len > path_len:
                    min_path_len = path_len
            max_keys_w_min_len = [k for k in max_keys if distances.get(k, float('inf')) == min_path_len]
            if debug: print(max_keys_w_min_len)
            end_a, end_b = max_keys_w_min_len[random.randint(0, len(max_keys_w_min_len) - 1)]
            path = find_shortest_path_bot3(2, grid, 1, botpos, (end_a, end_b))

            # complete exploring the path before sensing again
            while len(path) != 0:
                botpos = path.pop(0)

                i,j = botpos
                grid[i][j] = "😀"

                if debug:
                    for x in grid:
                        print(''.join(x))
                    print()
                    i, j = botpos
                    grid[i][j] = "✅"

                if botpos in leaks_to_find:
                    leak_time += 1
                    leaks_found.append(botpos)
                    leaks_to_find.remove(botpos)
                    if debug and leak_time == 1: print("leak 1 found")
                    nobeepflag = True
                    if leak_time == 2:
                        break
                    # P(leak in i,j | leak in k)
                    cell_pair_probability_dict = leak_in_i_j_given_leak_in_k(cell_pair_probability_dict, botpos)
                else:
                    # P(leak in i,j | leak not in k)
                    if(botpos not in leaks_found):
                        cell_pair_probability_dict = leak_in_i_j_given_no_leak_in_k(cell_pair_probability_dict, botpos)
                self.MOVES += 1
            
            if len(leaks_to_find) == 0:
                if debug: print("Leak Found")
                break
            
            temp_distance_dict.clear()