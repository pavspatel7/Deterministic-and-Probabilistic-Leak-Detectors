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
k = 8                    # size of detector for bot 1, bot 2, bot 5, bot 6
alpha = 0.08             # value of alpha for bot 3, bot 4, bot 7, bot 8, bot 9
sizeOfGrid = 30          # Grid Size
observations = 5         # number of observations
sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0
sum5 = 0
sum6 = 0
sum7 = 0
sum8 = 0
sum9 = 0

print("*****************************************************************************************************************")
print(f"K = {k} and alpha = {alpha}")

# for loop 
for i in range(observations):
    print("*****************************************************************************************************************")
    grid_with_one_leak, botpos, leakpos_1 = runMain(k, sizeOfGrid, 1)
    # Bot 1 vs Bot 2
    bot_1 = bot1(k, grid_with_one_leak, botpos, leakpos_1)
    print("BOT1 =>   sensor: ", bot_1.SENSOR, "  moves: ", bot_1.MOVES, "  action_sum: ", bot_1.SENSOR + bot_1.MOVES)
    bot_2 = bot2(k, grid_with_one_leak, botpos, leakpos_1)
    print("BOT2 =>   sensor: ", bot_2.SENSOR, "  moves: ", bot_2.MOVES, "  action_sum: ", bot_2.SENSOR + bot_2.MOVES)
    
    
    # Bot 3 vs Bot 4
    bot_3 = bot3(grid_with_one_leak, botpos, leakpos_1, alpha)
    print("BOT3 =>   sensor: ", bot_3.SENSOR, "  moves: ", bot_3.MOVES, "  action_sum: ", bot_3.SENSOR + bot_3.MOVES)
    bot_4 = bot4(grid_with_one_leak, botpos, leakpos_1, alpha)
    print("BOT4 =>   sensor: ", bot_4.SENSOR, "  moves: ", bot_4.MOVES, "  action_sum: ", bot_4.SENSOR + bot_4.MOVES)
    
    
    grid_with_two_leak, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)
    # bot 5 vs bot 6
    bot_5 = bot5(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    print("BOT5 =>   sensor: ", bot_5.SENSOR, "  moves: ", bot_5.MOVES, "  action_sum: ", bot_5.SENSOR + bot_5.MOVES)
    bot_6 = bot6(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    print("BOT6 =>   sensor: ", bot_6.SENSOR, "  moves: ", bot_6.MOVES, "  action_sum: ", bot_6.SENSOR + bot_6.MOVES)
    
    
    # # bot 7 vs bot 8
    bot_7 = bot7(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    print("BOT7 =>   sensor: ", bot_7.SENSOR, "  moves: ", bot_7.MOVES, "  action_sum: ", bot_7.SENSOR + bot_7.MOVES)
    bot_8 = bot8(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    print("BOT8 =>   sensor: ", bot_8.SENSOR, "  moves: ", bot_8.MOVES, "  action_sum: ", bot_8.SENSOR + bot_8.MOVES)
    bot_9 = bot9(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    print("BOT9 =>   sensor: ", bot_9.SENSOR, "  moves: ", bot_9.MOVES, "  action_sum: ", bot_9.SENSOR + bot_9.MOVES)
    
    
    
    sum1 += (bot_1.SENSOR + bot_1.MOVES)
    sum2 += (bot_2.SENSOR + bot_2.MOVES)
    sum3 += (bot_3.SENSOR + bot_3.MOVES)
    sum4 += (bot_4.SENSOR + bot_4.MOVES)
    sum5 += (bot_5.SENSOR + bot_5.MOVES)
    sum6 += (bot_6.SENSOR + bot_6.MOVES)
    sum7 += (bot_7.SENSOR + bot_7.MOVES)
    sum8 += (bot_8.SENSOR + bot_8.MOVES)
    sum9 += (bot_9.SENSOR + bot_9.MOVES)

print("*********************************************** RESULT **********************************************************")
print(f"Bot 1 average Total Number of actions (senses + moves): {sum1/observations}")
print(f"Bot 2 average Total Number of actions (senses + moves): {sum2/observations}")
print(f"Bot 3 average Total Number of actions (senses + moves): {sum3/observations}")
print(f"Bot 4 average Total Number of actions (senses + moves): {sum4/observations}")
print(f"Bot 5 average Total Number of actions (senses + moves): {sum5/observations}")
print(f"Bot 6 average Total Number of actions (senses + moves): {sum6/observations}")
print(f"Bot 7 average Total Number of actions (senses + moves): {sum7/observations}")
print(f"Bot 8 average Total Number of actions (senses + moves): {sum8/observations}")
print(f"Bot 9 average Total Number of actions (senses + moves): {sum9/observations}")


# sample output - 5 observations for each bot
'''
*****************************************************************************************************************
K = 8 and alpha = 0.08
*****************************************************************************************************************
BOT1 =>   sensor:  44   moves:  172   action_sum:  216
BOT2 =>   sensor:  19   moves:  84   action_sum:  103
BOT3 =>   sensor:  2   moves:  91   action_sum:  93
BOT4 =>   sensor:  53   moves:  533   action_sum:  586
BOT5 =>   sensor:  89   moves:  231   action_sum:  320
BOT6 =>   sensor:  46   moves:  121   action_sum:  167
BOT7 =>   sensor:  32   moves:  413   action_sum:  445
BOT8 =>   sensor:  17   moves:  413   action_sum:  430
BOT9 =>   sensor:  87   moves:  489   action_sum:  576
*****************************************************************************************************************
BOT1 =>   sensor:  1   moves:  12   action_sum:  13
BOT2 =>   sensor:  16   moves:  78   action_sum:  94
BOT3 =>   sensor:  25   moves:  603   action_sum:  628
BOT4 =>   sensor:  56   moves:  147   action_sum:  203
BOT5 =>   sensor:  55   moves:  205   action_sum:  260
BOT6 =>   sensor:  72   moves:  281   action_sum:  353
BOT7 =>   sensor:  22   moves:  500   action_sum:  522
BOT8 =>   sensor:  50   moves:  662   action_sum:  712
BOT9 =>   sensor:  30   moves:  322   action_sum:  352
*****************************************************************************************************************
BOT1 =>   sensor:  8   moves:  38   action_sum:  46
BOT2 =>   sensor:  5   moves:  102   action_sum:  107
BOT3 =>   sensor:  18   moves:  477   action_sum:  495
BOT4 =>   sensor:  15   moves:  123   action_sum:  138
BOT5 =>   sensor:  117   moves:  243   action_sum:  360
BOT6 =>   sensor:  29   moves:  148   action_sum:  177
BOT7 =>   sensor:  29   moves:  766   action_sum:  795
BOT8 =>   sensor:  30   moves:  276   action_sum:  306
BOT9 =>   sensor:  55   moves:  253   action_sum:  308
*****************************************************************************************************************
BOT1 =>   sensor:  64   moves:  130   action_sum:  194
BOT2 =>   sensor:  10   moves:  30   action_sum:  40
BOT3 =>   sensor:  9   moves:  97   action_sum:  106
BOT4 =>   sensor:  28   moves:  157   action_sum:  185
BOT5 =>   sensor:  50   moves:  176   action_sum:  226
BOT6 =>   sensor:  30   moves:  122   action_sum:  152
BOT7 =>   sensor:  31   moves:  327   action_sum:  358
BOT8 =>   sensor:  45   moves:  431   action_sum:  476
BOT9 =>   sensor:  21   moves:  291   action_sum:  312
*****************************************************************************************************************
BOT1 =>   sensor:  20   moves:  103   action_sum:  123
BOT2 =>   sensor:  21   moves:  79   action_sum:  100
BOT3 =>   sensor:  1   moves:  44   action_sum:  45
BOT4 =>   sensor:  1   moves:  44   action_sum:  45
BOT5 =>   sensor:  26   moves:  105   action_sum:  131
BOT6 =>   sensor:  37   moves:  190   action_sum:  227
BOT7 =>   sensor:  48   moves:  1138   action_sum:  1186
BOT8 =>   sensor:  55   moves:  769   action_sum:  824
BOT9 =>   sensor:  68   moves:  333   action_sum:  401
*********************************************** RESULT **********************************************************
Bot 1 average Total Number of actions (senses + moves): 118.4
Bot 2 average Total Number of actions (senses + moves): 88.8
Bot 3 average Total Number of actions (senses + moves): 273.4
Bot 4 average Total Number of actions (senses + moves): 231.4
Bot 5 average Total Number of actions (senses + moves): 259.4
Bot 6 average Total Number of actions (senses + moves): 215.2
Bot 7 average Total Number of actions (senses + moves): 661.2
Bot 8 average Total Number of actions (senses + moves): 549.6
Bot 9 average Total Number of actions (senses + moves): 389.8
'''
