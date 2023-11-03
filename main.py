import random

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

# Layout
from layout import runMain


k = 5              # sixe of detector ((2*k) +1)
sizeOfGrid = 50
leaks = 1

# grid_with_one_leak, detectionGrid, botpos, leakpos_1  = runMain(k,sizeOfGrid,1)
# grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)

for i in range(1):
    grid_with_one_leak, botpos, leakpos_1  = runMain(k,sizeOfGrid,leaks)
    

    # Bot 1 vs Bot 2
    bot_1 = bot1(k, grid_with_one_leak, botpos, leakpos_1)
    print("BOT-1 == sensor", bot_1.SENSOR ,"moves", bot_1.MOVES, "average:-", (bot_1.SENSOR + bot_1.MOVES) / 2)
    # print("bot2")
    # bot2(grid_with_one_leak, detectionGrid, botpos, leakpos_1)
    # # bot 5 vs bot 6
    # print("bot5")
    #grid_with_two_leak, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)
    #bot_5 = bot5(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    #print("BOT-5 == sensor", bot_5.SENSOR ,"moves", bot_5.MOVES, "average:-", (bot_5.SENSOR + bot_5.MOVES) / 2)
    # print("bot6")
    # bot6(grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2)
    
    # # Bot 3 vs Bot 4
    # print("bot3")
    # bot3(grid_with_one_leak, botpos, leakpos_1)
    # print("bot4")
    # bot4(grid_with_one_leak, detectionGrid, botpos, leakpos_1)
    # # bot 7 vs bot 8
    # print("bot7")
    # bot7(grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2)
    # print("bot8")
    # bot8(grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2)


