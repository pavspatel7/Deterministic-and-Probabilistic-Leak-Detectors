import random
sizeOfGrid = 5
class creatingLayout():
    def __init__(self):
        self.openGrid = []
        self.grid = []
    def Inititate_Grid(self, D):
        self.grid = [["⬛️" for _ in range(D)] for _ in range(D)]
        openBlockPosArr = []
        deadEndCells = []

        randIntX = random.randint(1, D - 2)
        randIntY = random.randint(1, D - 2)
        self.grid[randIntX][randIntY] = "⬜️"
        openBlockPosArr.append((randIntX, randIntY))

        effX1 = randIntX - 1
        effX2 = randIntX + 1
        effY1 = randIntY - 1
        effY2 = randIntY + 1

        while openBlockPosArr:
            openBlockPosArr = []
            for x in range(effX1, effX2 + 1):
                for y in range(effY1, effY2 + 1):
                    openBlockPos = 0
                    if self.grid[x][y] == "⬛️":
                        a = x + 1
                        b = x - 1
                        c = y + 1
                        d = y - 1
                        if a <= effX2 and self.grid[a][y] == "⬜️":
                            openBlockPos += 1
                        if b >= effX1 and self.grid[b][y] == "⬜️":
                            openBlockPos += 1
                        if c <= effY2 and self.grid[x][c] == "⬜️":
                            openBlockPos += 1
                        if d >= effY1 and self.grid[x][d] == "⬜️":
                            openBlockPos += 1
                        if openBlockPos == 1:
                            openBlockPosArr.append((x, y))
            if openBlockPosArr:

                randIndex = random.randint(0, len(openBlockPosArr) - 1)
                randIntX, randIntY = openBlockPosArr[randIndex]
                self.grid[randIntX][randIntY] = "⬜️"

                if 0 < effX1 == randIntX:
                    effX1 = randIntX - 1
                if D - 1 > effX2 == randIntX:
                    effX2 = randIntX + 1
                if 0 < effY1 == randIntY:
                    effY1 = randIntY - 1
                if D - 1 > effY2 == randIntY:
                    effY2 = randIntY + 1

        for x in range(D):
            for y in range(D):
                deadEndBlock = 0
                deadEndBlockArr = []
                if self.grid[x][y] == "⬜️":
                    a = x + 1
                    b = x - 1
                    c = y + 1
                    d = y - 1
                    if 0 <= a <= D - 1 and self.grid[a][y] == "⬛️":
                        deadEndBlock += 1
                        deadEndBlockArr.append((a, y))
                    if 0 <= b <= D - 1 and self.grid[b][y] == "⬛️":
                        deadEndBlock += 1
                        deadEndBlockArr.append((b, y))
                    if 0 <= c <= D - 1 and self.grid[x][c] == "⬛️":
                        deadEndBlock += 1
                        deadEndBlockArr.append((x, c))
                    if 0 <= d <= D - 1 and self.grid[x][d] == "⬛️":
                        deadEndBlock += 1
                        deadEndBlockArr.append((x, d))
                    if deadEndBlock >= 3:
                        randIndex = random.randint(0, len(deadEndBlockArr) - 1)
                        randIntX, randIntY = deadEndBlockArr[randIndex]
                        deadEndCells.append(
                            (randIntX, randIntY))  # for each dead end pick a coordinate to open at random and store in list

        # shuffle the list and open 50% of the dead end cells
        random.shuffle(deadEndCells)
        for i in range(int(len(deadEndCells) / 2)):
            x, y = deadEndCells[i]
            self.grid[x][y] = "⬜️"
        
        return self.grid

    # Appending Open Cell to OpenGrid List
    def getOpenGridCell(self, D):
        for x in range(D):
            for y in range(D):
                if self.grid[x][y] == "⬜️":
                    self.openGrid.append((x, y))
        
        return self.openGrid


def runMain():
    layout = creatingLayout()
    # Generate Layout
    OriginalGrid = layout.Inititate_Grid(sizeOfGrid)
    OpenCells = layout.getOpenGridCell(sizeOfGrid)
    # Generate random Leak Cell
    pickRandomInt = random.randint(0,len(OpenCells)-1)
    x_leak, y_leak = OpenCells[pickRandomInt]
    OriginalGrid[x_leak][y_leak] = "🟥"
    OpenCells.remove((x_leak,y_leak))
    # Generate random Bot Position
    pickRandomInt = random.randint(0,len(OpenCells)-1)
    x_bot, y_bot = OpenCells[pickRandomInt]
    OriginalGrid[x_bot][y_bot] = "🤖"
    return OriginalGrid, (x_bot,y_bot), (x_leak,y_leak)





# layout = creatingLayout()
# result = layout.Inititate_Grid(D=5)
# for x in result:
#     print(' '.join(x))
# print()
# opencell = layout.getOpenGridCell(5)
# print(opencell)