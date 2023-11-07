import random
from helperMethod import *


class bot3():
    
    def __init__(self, getGrid, botpos, leakpos_1):
        
        self.grid = getGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        # temp grid
        self.bot_3_grid = [row.copy() for row in self.grid]
        self.task_for_bot3(self.bot_3_grid, botpos)
        
        
    def task_for_bot3(self, grid, botpos):
        debug = True
        alpha = 0.9

        cell_probability_dict = {}
        open=0
        if debug:
            for x in grid:
                print(''.join(x))
            print()

        # In dictionary storing the cell as (x,y) as key and probabilities as value:
        # 1) open and leak cell to by default probability is 1 / total open cells
        # 2) block and bot cell to by default probability is 0
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "⬜️" or grid[x][y] == "🟥":
                    open+=1
                    cell_probability_dict[(x,y)] = 1
                if grid[x][y] == "⬛️" or grid[x][y] == "😀":
                    cell_probability_dict[(x,y)] = 0



        # code here
        for items in cell_probability_dict.keys():
            if cell_probability_dict[items] == 1:
                cell_probability_dict[items] = 1 / open
        timestamp = 0
        while True:
            timestamp+=1
            # detect beep & update probabilities
            curr_beep_prob = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_1)
            if debug: print("curr_beep_prob", curr_beep_prob)
            rand = random.uniform(0, 1)
            if debug: print("rand", rand)

            if curr_beep_prob > rand:
                if debug: print("beep")
                cell_probability_dict = prob_leak_given_beep(alpha, grid, cell_probability_dict, botpos)
            else:
                if debug: print("no beep")
                cell_probability_dict = prob_leak_given_no_beep(alpha, grid, cell_probability_dict, botpos)

            # find a cell in grid where probability is highest
            max_key = max(cell_probability_dict, key=lambda k: cell_probability_dict[k])
            max_value = max(cell_probability_dict.values())
            max_keys = [k for k, v in cell_probability_dict.items() if v == max_value]
            min_path_len = float('inf')
            for key in max_keys:
                # if cell_probability_dict[key] == max_value:
                #     end_a, end_b = key
                #     min_path_len = get_bfs_len(2, grid, 1, botpos, key)
                #    break
                path_len = get_bfs_len(2, grid, 1, botpos, key)
                if min_path_len > path_len:
                    end_a, end_b = key
                    min_path_len = path_len
            if debug:
                print("Highest prob at {} = {}".format((end_a, end_b), cell_probability_dict[(end_a, end_b)]))
            # find the shortest path towards the highest prob and move to next/first cell in path and update stats
            path = find_shortest_path_bot3(2, grid, 1, botpos, (end_a, end_b))
            botpos = path[0]
            temp_distance_dict.clear()
            if debug:
                i, j = botpos
                grid[i][j] = "😀"
                for x in grid:
                    print(''.join(x))
                print()
            # if leak found: break
            # else update P(leak in j | no leak in i)
            if botpos == self.leakpos_1:
                if debug: print("leak found")
                break
            else:
                if debug:
                    print("moved to", botpos)
                    print("leak at", self.leakpos_1)
                cell_probability_dict[botpos] = 0
                cell_probability_dict = leak_in_j_given_no_leak_in_i(cell_probability_dict)


        print(timestamp)










        '''
                probability of current cell containing a leak = 0
                probability of all other cells divide equally out of 1

                *************************************************************
                i is location of bot, j is evey other cell that might contain a leak

                detect beep & update
                xb = e^(-alpha(d-1)) -> d is BFS from i to leak
                select random number rn from 0 to 1, -> random.uniform(0, 1)
                if xb > rn: then beep
                else no beep

                if no beep:                 P(leak in j | no beep in i)
                else if beep:               P(leak in j | beep in i)

                find a cell in grid where probability is highest
                move towards highest prob one step at a time
                if leak found:              break
                else                        P(leak in j | no leak in i)

                repeat
                *************************************************************
        '''
