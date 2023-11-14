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
        # cell_probability_dict = {}
        opent = 0
        leak_in_k = 0
        leak_time = 0
        leaks_found = []

        if debug:
            for x in grid:
                print(''.join(x))
            print()

        # In dictionary storing the cell as (x,y) as key and probabilities as value:
        # 1) open and leak cell to by default probability is 1 / total open cells
        # 2) block and bot cell to by default probability is 0

        open_cells = []
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "⬜️" or grid[x][y] == "🟥":
                    opent += 1
                    open_cells.append((x, y))
                # if grid[x][y] == "⬛️" or grid[x][y] == "😀":
                #       blocked_cells.append((x, y))
        
        keys = []
        keys.extend(open_cells)
        # keys.extend(blocked_cells)
        num_open_cells_pair = opent*(opent-1)/2
        cell_pairs = [(keys[i], keys[j]) for i in range(len(keys)) for j in range(i+1, len(keys))]
        # print("Cell Pairs: ",cell_pairs)
        for pair in cell_pairs:
            # if pair[0] in blocked_cells or pair[1] in blocked_cells:
            #     cell_pair_probability_dict[pair] = 0
            # else:
            cell_pair_probability_dict[pair] = 1/num_open_cells_pair


        # for keys, items in cell_pair_probability_dict.items():
        #     print(keys, items)
        if debug: print( "Num Pairs initial: {}".format(len(cell_pair_probability_dict)))
        # if debug:
        #     for x in grid:
        #         print(''.join(x))
        #     print()
        # P(leak in i,j | leak not in k)
        cell_pair_probability_dict = leak_in_i_j_given_no_leak_in_k(cell_pair_probability_dict, botpos)

        while True:

            # precalculate distances from botpos to all other locations
            distances = all_distances_bfs(2, grid, 1, botpos)
            # if debug: print(distances)
            clean_up(cell_pair_probability_dict)
            
            # P(beep in k | leaks in actual leaks location)
            curr_beep_prob = beep_in_k_given_leak_in_i_and_j(alpha, grid, botpos, self.leakpos_1, self.leakpos_2, distances)
            # generate a random number to compare
            rand = random.uniform(0, 1)
            curr_beep_prob1_leak1 = curr_beep_prob1_leak2 = 0
            curr_beep_prob1_leak1 = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_1, distances)
            curr_beep_prob1_leak2 = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_2, distances)
            beep_1 = (rand <= curr_beep_prob1_leak1)
            beep_2 = (rand <= curr_beep_prob1_leak2)
            curr_beep = beep_1 or beep_2
            #curr_beep_prob = beep_in_k_given_leak_in_i_and_j(alpha, grid, botpos, self.leakpos_1, self.leakpos_2, distances)
            # generate a random number to compare
            self.SENSOR += 1
            if curr_beep:
                if debug: print("beep")
                cell_pair_probability_dict = prob_leak_given_beep(alpha, grid, cell_pair_probability_dict, botpos, distances)
            else:
                if debug: print("no beep")
                if(botpos not in leaks_found):
                    cell_pair_probability_dict = prob_leak_given_no_beep(alpha, grid, cell_pair_probability_dict, botpos, distances)

            # plan a path towards high probability pair with short path from botpos in grid
            max_value = max(cell_pair_probability_dict.values())
            if debug: print("Max prob is:", max_value)
            max_prob_pairs = [k for k, v in cell_pair_probability_dict.items() if v == max_value]
            cell_probability_dict = {}
            if debug: print("Max prob pairs {}".format(len(max_prob_pairs)))
            min_pair_dist = float('inf')
            for pair in max_prob_pairs:
                pair_dist = distances.get(pair[0], float('inf')) + distances.get(pair[1], float('inf'))
                if min_pair_dist > pair_dist:
                    min_pair_dist = pair_dist
            
            max_prob_pairs = [k for k in max_prob_pairs if distances.get(k[0], float('inf')) + distances.get(k[1], float('inf')) == min_pair_dist]
            cell_a, cell_b = max_prob_pairs[random.randint(0, len(max_prob_pairs) - 1)]
            if len(leaks_to_find) == 2:
                if distances.get(cell_a, float('inf')) < distances.get(cell_b, float('inf')):
                    path = find_shortest_path_bot3(2, grid, 1, botpos, cell_a) + find_shortest_path_bot3(2, grid, 1, cell_a, cell_b)
                else:
                    path = find_shortest_path_bot3(2, grid, 1, botpos, cell_b) + find_shortest_path_bot3(2, grid, 1, cell_b, cell_a)
            else:
                if cell_a in leaks_found:
                    path =  find_shortest_path_bot3(2, grid, 1, botpos, cell_b)
                else:
                    path = find_shortest_path_bot3(2, grid, 1, botpos, cell_a)

            while len(path) != 0:
                botpos = path.pop(0)
                distances = all_distances_bfs(2, grid, 1, botpos)
                self.MOVES += 1

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
                    if leak_time == 2:
                        break
                    cell_pair_probability_dict = leak_in_i_j_given_leak_in_k(cell_pair_probability_dict, botpos)
                    break
                else:
                    #leak_in_i = cell_probability_dict[botpos]
                    # P(leak in j | leak not in i)
                    if(botpos not in leaks_found):
                        cell_pair_probability_dict = leak_in_i_j_given_no_leak_in_k(cell_pair_probability_dict, botpos)
                        if botpos == cell_a or botpos == cell_b:
                            path = []
                    #leak_in_j_given_no_leak_in_i(cell_probability_dict, botpos, leak_in_i)
                
                # generate a random number to compare
                wrong_leak_1 = wrong_leak_2 = True
                if leakpos_1 not in leaks_found:
                    curr_beep_prob2_leak1 = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_1, distances)
                    wrong_leak_1 = curr_beep_prob2_leak1 < curr_beep_prob1_leak1
                if leakpos_2 not in leaks_found:
                    curr_beep_prob2_leak2 = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_2, distances)
                    wrong_leak_2 = curr_beep_prob2_leak2 < curr_beep_prob1_leak2
                self.SENSOR += 1
                if wrong_leak_1 and wrong_leak_2:
                    if debug: print("Wrong Path detected")
                    while len(path) != 0:
                        cell = path.pop()
                        if(cell == cell_a or cell == cell_b):
                            path = []
                        #cell_pair_probability_dict = no_beep_in_k_given_leak_in_i_and_j(alpha, grid, cell, self.leakpos_1, self.leakpos_2, distances)
                        if cell not in leaks_found:
                            cell_pair_probability_dict = leak_in_i_j_given_no_leak_in_k(cell_pair_probability_dict, cell)
                            distances = all_distances_bfs(2, grid, 1, cell)
                else:
                    curr_beep_prob1_leak1 = curr_beep_prob2_leak1
                    curr_beep_prob1_leak2 = curr_beep_prob2_leak2

            if len(leaks_to_find) == 0:
                if debug: print("Leak Found")
                break
            temp_distance_dict.clear()