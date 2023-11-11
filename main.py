import random
import openpyxl

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = 'Sensor bot3'
sheet['B1'] = 'Moves bot3'
sheet['C1'] = 'Sensor bot4'
sheet['D1'] = 'Moves bot4'
row = 2

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

k = 3  # size of detector ((2*k) +1)
alpha = 0  # value of alpha for bot 3, bot 4
sizeOfGrid = 50
leaks = 1
avg_1 = 0
avg_2 = 0
timer = 0
# grid_with_one_leak, detectionGrid, botpos, leakpos_1  = runMain(k,sizeOfGrid,1)
# grid_with_two_leak, detectionGrid, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)

print("alpha 0 to 1, bot 4 repeat 3 times each step after beep found, 200 obs")
count = 0
while count < 200:
    grid_with_one_leak, botpos, leakpos_1 = runMain(k, sizeOfGrid, leaks)
    # Bot 1 vs Bot 2
    # bot_1 = bot1(k, grid_with_one_leak, botpos, leakpos_1)
    # print("BOT-1 == sensor", bot_1.SENSOR ,"moves", bot_1.MOVES, "average:-", (bot_1.SENSOR + bot_1.MOVES) / 2)
    # bot_2 = bot2(k, grid_with_one_leak, botpos, leakpos_1)
    # print("BOT-2 == sensor", bot_2.SENSOR ,"moves", bot_2.MOVES, "average:-", (bot_2.SENSOR + bot_2.MOVES) / 2)

    # Bot 3 vs Bot 4
    # print("bot3")
    bot_3 = bot3(grid_with_one_leak, botpos, leakpos_1, alpha)
    print("BOT3 =>   sensor: ", bot_3.SENSOR, "  moves: ", bot_3.MOVES, "  action_sum: ", bot_3.SENSOR + bot_3.MOVES)
    # print("bot4")
    bot_4 = bot4(grid_with_one_leak, botpos, leakpos_1, alpha)
    print("BOT4 =>   sensor: ", bot_4.SENSOR, "  moves: ", bot_4.MOVES, "  action_sum: ", bot_4.SENSOR + bot_4.MOVES)

    # Write data into the Excel file
    # sheet[f'A{row}'] = bot_3.SENSOR
    # sheet[f'B{row}'] = bot_3.MOVES
    # sheet[f'C{row}'] = bot_4.SENSOR
    # sheet[f'D{row}'] = bot_4.MOVES
    # row += 1

    # grid_with_two_leak, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)
    # # bot 5 vs bot 6
    # bot_5 = bot5(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("BOT-5 == sensor", bot_5.SENSOR ,"moves", bot_5.MOVES, "average:-", (bot_5.SENSOR + bot_5.MOVES) / 2)

    # bot_6 = bot6(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("BOT-6 == sensor", bot_6.SENSOR ,"moves", bot_6.MOVES, "average:-", (bot_6.SENSOR + bot_6.MOVES) / 2)

    # # bot 7 vs bot 8
    # print("bot7")
    # bot7(grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("bot8")
    # bot8(grid_with_two_leak, botpos, leakpos_1, leakpos_2)

    avg_1 += bot_3.SENSOR + bot_3.MOVES
    avg_2 += bot_4.SENSOR + bot_4.MOVES

    count += 1
    if count == 199:
        avg_1 = avg_1 / 200
        avg_2 = avg_2 / 200
        print("Bot3 final avg -", avg_1)
        print("Bot4 final avg -", avg_2)

        row += 1
        sheet[f'A{row}'] = avg_1
        row += 1
        sheet[f'A{row}'] = avg_2

        print()
        print()
        print()
        print()
        print()
        print()
        avg_1 = 0
        avg_2 = 0
        row += 5
        alpha += 0.05
        print("alpha", alpha)
        print()
        if alpha >= 1.02:
            print()
            print("data collected")
            break
        else:
            count = 0

workbook.save('dijkstras2003.xlsx')
workbook.close()
