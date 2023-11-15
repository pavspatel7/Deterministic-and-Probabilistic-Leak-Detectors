# imports
# Deterministic Leak Detectors
from deterministic_Leak_detectors.botOne import bot1
from deterministic_Leak_detectors.botTwo import bot2
from deterministic_Leak_detectors.botFive import bot5
from deterministic_Leak_detectors.botSix import bot6

# Probability Leak Detectors
from Probabilistic_Leak_Detectors.botThree import bot3
from Probabilistic_Leak_Detectors.botFour import bot4
from Probabilistic_Leak_Detectors.botSeven import bot7
from Probabilistic_Leak_Detectors.botEight import bot8
from Probabilistic_Leak_Detectors.botNine import bot9

# Layout
from layout import runMain

# Initialize variables
k = 3                    # size of detector for bot 1, bot 2, bot 5, bot 6
alpha = 0.08                # value of alpha for bot 3, bot 4, bot 7, bot 8, bot 9
sizeOfGrid = 30          # Grid Size
observations = 10         # number of observations

# for loop 
for i in range(observations):
    print()
    # print("*****************************************************************************************************************")
    # print(f"K = {k} and alpha = {alpha}")
    # print("*****************************************************************************************************************")
    
    grid_with_one_leak, botpos, leakpos_1 = runMain(k, sizeOfGrid, 1)
    # Bot 1 vs Bot 2
    # bot_1 = bot1(k, grid_with_one_leak, botpos, leakpos_1)
    # print("BOT1 =>   sensor: ", bot_1.SENSOR, "  moves: ", bot_1.MOVES, "  action_sum: ", bot_1.SENSOR + bot_1.MOVES)
    # bot_2 = bot2(k, grid_with_one_leak, botpos, leakpos_1)
    # print("BOT2 =>   sensor: ", bot_2.SENSOR, "  moves: ", bot_2.MOVES, "  action_sum: ", bot_2.SENSOR + bot_2.MOVES)
    # print("*****************************************************************************************************************")
    # Bot 3 vs Bot 4
    bot_3 = bot3(grid_with_one_leak, botpos, leakpos_1, alpha)
    print("BOT3 =>   sensor: ", bot_3.SENSOR, "  moves: ", bot_3.MOVES, "  action_sum: ", bot_3.SENSOR + bot_3.MOVES)
    bot_4 = bot4(grid_with_one_leak, botpos, leakpos_1, alpha)
    print("BOT4 =>   sensor: ", bot_4.SENSOR, "  moves: ", bot_4.MOVES, "  action_sum: ", bot_4.SENSOR + bot_4.MOVES)
    # print("*****************************************************************************************************************")
    # grid_with_two_leak, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)
    # # bot 5 vs bot 6
    # bot_5 = bot5(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("BOT5 =>   sensor: ", bot_5.SENSOR, "  moves: ", bot_5.MOVES, "  action_sum: ", bot_5.SENSOR + bot_5.MOVES)
    # bot_6 = bot6(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("BOT6 =>   sensor: ", bot_6.SENSOR, "  moves: ", bot_6.MOVES, "  action_sum: ", bot_6.SENSOR + bot_6.MOVES)
    # print("*****************************************************************************************************************")
    # # bot 7 vs bot 8
    # bot_7 = bot7(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    # print("BOT7 =>   sensor: ", bot_7.SENSOR, "  moves: ", bot_7.MOVES, "  action_sum: ", bot_7.SENSOR + bot_7.MOVES)
    # bot_8 = bot8(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    # print("BOT8 =>   sensor: ", bot_8.SENSOR, "  moves: ", bot_8.MOVES, "  action_sum: ", bot_8.SENSOR + bot_8.MOVES)
    # bot_9 = bot9(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    # print("BOT9 =>   sensor: ", bot_9.SENSOR, "  moves: ", bot_9.MOVES, "  action_sum: ", bot_9.SENSOR + bot_9.MOVES)
    # print("*****************************************************************************************************************")
