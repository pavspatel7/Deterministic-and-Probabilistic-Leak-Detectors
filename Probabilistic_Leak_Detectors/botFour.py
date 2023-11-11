import random
from helperMethod import *

class bot4():
    def __init__(self, getGrid, botpos, leakpos_1, alpha):

        self.grid = getGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        # temp grid
        self.MOVES = 0
        self.SENSOR = 0
        self.bot_4_grid = [row.copy() for row in self.grid]
        self.task_for_bot4(self.bot_4_grid, botpos, alpha)

    def task_for_bot4(self, grid, botpos, alpha):
        debug = False
        nobeepflag = True
        # probability matrix
        cell_probability_dict = {}
        opent = 0
        leak_in_i = 0

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
                    opent += 1
                    cell_probability_dict[(x, y)] = 1
                if grid[x][y] == "⬛️" or grid[x][y] == "😀":
                    cell_probability_dict[(x, y)] = 0

        # each cell starts with equal probability of containing a leak except where the bot spawns
        for items in cell_probability_dict.keys():
            if cell_probability_dict[items] == 1:
                cell_probability_dict[items] = 1 / opent

        # task is done when leak is found
        while botpos != self.leakpos_1:

            # precalculate distances from botpos to all other locations
            # this is achieved using Dijkstra's algorithm
            distances = all_distances_bfs(2, grid, 1, botpos)
            if debug: print(distances)

            # flag that determines whether to increase sensing or not
            if nobeepflag:
                check = 1
            else:
                check = 5

            # P(leak in j | leak not in i)
            cell_probability_dict = leak_in_j_given_no_leak_in_i(cell_probability_dict, botpos, leak_in_i)

            count = 0
            curr_beep_prob = 0
            rand = 0

            while count < check:
                self.SENSOR += 1
                # P(beep in i | leak in leak location)
                curr_beep_prob = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_1, distances)
                # generate a random number to compare
                rand = random.uniform(0, 1)

                if curr_beep_prob >= rand:
                    # when you hear a beep
                    if nobeepflag:
                        nobeepflag = False
                    break

                count += 1

            if curr_beep_prob >= rand:
                if debug: print("beep")
                # P(leak in j | beep in i)
                cell_probability_dict = prob_leak_given_beep(alpha, grid, cell_probability_dict, botpos, distances)
            else:
                if debug: print("no beep")
                # P(leak in j | beep not in i)
                cell_probability_dict = prob_leak_given_no_beep(alpha, grid, cell_probability_dict, botpos, distances)

            # plan a path towards high probability with short path from botpos in grid
            max_value = max(cell_probability_dict.values())
            max_keys = [k for k, v in cell_probability_dict.items() if v == max_value]
            min_path_len = float('inf')
            for key in max_keys:
                path_len = distances.get(key, float('inf'))
                if min_path_len > path_len:
                    min_path_len = path_len
            max_keys_w_min_len = [k for k in max_keys if distances.get(k, float('inf')) == min_path_len]
            end_a, end_b = max_keys_w_min_len[random.randint(0, len(max_keys_w_min_len) - 1)]
            path = find_shortest_path_bot3(2, grid, 1, botpos, (end_a, end_b))

            # complete exploring the path before sensing again
            while len(path) != 0:
                botpos = path.pop(0)

                if debug:
                    i, j = botpos
                    grid[i][j] = "😀"
                    for x in grid:
                        print(''.join(x))
                    print()

                if botpos == self.leakpos_1:
                    if debug: print("leak found")
                    break
                else:
                    leak_in_i = cell_probability_dict[botpos]
                    # P(leak in j | leak not in i)
                    cell_probability_dict = leak_in_j_given_no_leak_in_i(cell_probability_dict, botpos, leak_in_i)
                self.MOVES += 1

            temp_distance_dict.clear()
