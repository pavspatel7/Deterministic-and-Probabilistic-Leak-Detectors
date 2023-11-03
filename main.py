from pydoc import Helper
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


k = 4              # sixe of detector ((2*k) +1)
sizeOfGrid = 25
leaks = 1

# grid_with_one_leak, detectionGrid, botpos, leakpos_1  = runMain(k,sizeOfGrid,1)
# grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)

for i in range(1):
    grid_with_one_leak, botpos, leakpos_1  = runMain(k,sizeOfGrid,leaks)
    # grid_with_two_leak, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,leaks)


    # Bot 1 vs Bot 2
    # print("bot 1 Result" )
    # bot1(k, grid_with_one_leak, botpos, leakpos_1)
    
    # print("bot2")
    # bot2(grid_with_one_leak, detectionGrid, botpos, leakpos_1)
    # # bot 5 vs bot 6
    # print("bot5")
    # bot5(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("bot6")
    # bot6(grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2)
    
    # # Bot 3 vs Bot 4
    print("bot3")
    bot3(grid_with_one_leak, botpos, leakpos_1)
    # print("bot4")
    # bot4(grid_with_one_leak, detectionGrid, botpos, leakpos_1)
    # # bot 7 vs bot 8
    # print("bot7")
    # bot7(grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2)
    # print("bot8")
    # bot8(grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2)


