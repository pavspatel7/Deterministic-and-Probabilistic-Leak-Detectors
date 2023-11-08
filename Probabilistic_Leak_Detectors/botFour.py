import random
from helperMethod import *


class bot4():

    def __init__(self, getGrid, botpos, leakpos_1, alpha):

        self.grid = getGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        # temp grid
        self.bot_4_grid = [row.copy() for row in self.grid]
        self.task_for_bot4(self.bot_4_grid, botpos, alpha)

    def task_for_bot4(self, grid, botpos, alpha):
        debug = True
        nobeepflag = True

        cell_probability_dict = {}
        openT = 0
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
                    openT += 1
                    cell_probability_dict[(x, y)] = 1
                if grid[x][y] == "⬛️" or grid[x][y] == "😀":
                    cell_probability_dict[(x, y)] = 0

        # code here
        for items in cell_probability_dict.keys():
            if cell_probability_dict[items] == 1:
                cell_probability_dict[items] = 1 / openT
        timestamp = 0
        while True:
            # detect beep & update probabilities

            if nobeepflag:
                check = 1
            else:
                check = 10

            count = 0
            while count < check:
                curr_beep_prob = beep_in_i_given_leak_in_j(alpha, grid, botpos, self.leakpos_1)
                if debug: print("curr_beep_prob", curr_beep_prob)
                rand = random.uniform(0, 1)
                if debug: print("rand", rand)

                if curr_beep_prob > rand:
                    # beep part
                    if nobeepflag:
                        nobeepflag = False
                    break

                count += 1

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
            timestamp += 1
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
