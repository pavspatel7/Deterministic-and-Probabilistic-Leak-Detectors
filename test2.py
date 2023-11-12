import random
import openpyxl

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'] = 'Sensor bot7'
sheet['B1'] = 'Moves bot7'
sheet['C1'] = 'Sensor bot8'
sheet['D1'] = 'Moves bot8'
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
from Probabilistic_Leak_Detectors.botNine import bot9

# Layout
from layout import runMain

k = 3               # size of detector ((2*k) +1)
alpha = 0.5          # value of alpha for bot 3, bot 4
sizeOfGrid = 30
avg_1 = 0
avg_2 = 0
avg_3 = 0
timer = 0
print("alpha 0.5 to 1, 50 obs")

count = 0
while count < 50:

    # grid_with_one_leak, botpos, leakpos_1 = runMain(k, sizeOfGrid, 1)

    # Bot 1 vs Bot 2
    # bot_1 = bot1(k, grid_with_one_leak, botpos, leakpos_1)
    # print("BOT-1 == sensor", bot_1.SENSOR ,"moves", bot_1.MOVES, "average:-", (bot_1.SENSOR + bot_1.MOVES) / 2)
    # bot_2 = bot2(k, grid_with_one_leak, botpos, leakpos_1)
    # print("BOT-2 == sensor", bot_2.SENSOR ,"moves", bot_2.MOVES, "average:-", (bot_2.SENSOR + bot_2.MOVES) / 2)

    # Bot 3 vs Bot 4
    # bot_3 = bot3(grid_with_one_leak, botpos, leakpos_1, alpha)
    # print("BOT3 =>   sensor: ", bot_3.SENSOR, "  moves: ", bot_3.MOVES, "  action_sum: ", bot_3.SENSOR + bot_3.MOVES)
    # bot_4 = bot4(grid_with_one_leak, botpos, leakpos_1, alpha)
    # print("BOT4 =>   sensor: ", bot_4.SENSOR, "  moves: ", bot_4.MOVES, "  action_sum: ", bot_4.SENSOR + bot_4.MOVES)

    

    grid_with_two_leak, botpos, leakpos_1, leakpos_2 = runMain(k,sizeOfGrid,2)

    # # bot 5 vs bot 6
    # bot_5 = bot5(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("BOT-5 == sensor", bot_5.SENSOR ,"moves", bot_5.MOVES, "average:-", (bot_5.SENSOR + bot_5.MOVES) / 2)

    # bot_6 = bot6(k, grid_with_two_leak, botpos, leakpos_1, leakpos_2)
    # print("BOT-6 == sensor", bot_6.SENSOR ,"moves", bot_6.MOVES, "average:-", (bot_6.SENSOR + bot_6.MOVES) / 2)

    # # bot 7 vs bot 8
    bot_7 = bot7(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    print("BOT7 =>   sensor: ", bot_7.SENSOR, "  moves: ", bot_7.MOVES, "  action_sum: ", bot_7.SENSOR + bot_7.MOVES)
    bot_8 = bot8(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    print("BOT8 =>   sensor: ", bot_8.SENSOR, "  moves: ", bot_8.MOVES, "  action_sum: ", bot_8.SENSOR + bot_8.MOVES)
    bot_9 = bot9(grid_with_two_leak, botpos, leakpos_1, leakpos_2, alpha)
    print("BOT9 =>   sensor: ", bot_9.SENSOR, "  moves: ", bot_9.MOVES, "  action_sum: ", bot_9.SENSOR + bot_9.MOVES)

    # Write data into the Excel file
    sheet[f'A{row}'] = bot_7.SENSOR
    sheet[f'B{row}'] = bot_7.MOVES
    sheet[f'C{row}'] = bot_8.SENSOR
    sheet[f'D{row}'] = bot_8.MOVES
    sheet[f'A{row}'] = bot_9.SENSOR
    sheet[f'B{row}'] = bot_9.MOVES
    row += 1

    # Calculate avg
    avg_1 += bot_7.SENSOR + bot_7.MOVES
    avg_2 += bot_8.SENSOR + bot_8.MOVES
    avg_3 += bot_9.SENSOR + bot_9.MOVES
    
    count += 1
    if count == 49:
        avg_1 = avg_1 / 50
        avg_2 = avg_2 / 50
        avg_3 = avg_3 / 50
        print("Bot7 final avg -", avg_1)
        print("Bot8 final avg -", avg_2)
        print("Bot8 final avg -", avg_3)

        row += 1
        sheet[f'A{row}'] = avg_1
        row += 1
        sheet[f'A{row}'] = avg_2
        row += 1
        sheet[f'A{row}'] = avg_3

        print()
        print()
        print()
        print()
        print()
        print()
        avg_1 = 0
        avg_2 = 0
        avg_3 = 0
        row += 5
        alpha += 0.05
        print("alpha", alpha)
        print()
        sheet[f'A{row}'] = alpha
        print("alpha 0.5 to 1")
        if alpha >= 1.02:
            print()
            print("data collected")
            break
        else:
            count = 0

workbook.save('bot_7_8_9_report2_50.xlsx')
workbook.close()
