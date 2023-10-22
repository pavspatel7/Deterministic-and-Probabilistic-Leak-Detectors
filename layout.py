import random

class creatingLayout():
    def __init__(self):
        # Initializing Variables 
        self.openGrid = []
        self.grid = []
        self.innerGridCells = []
        
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
    def getOpenGridCell(self, sizeOfGrid):
        for x in range(sizeOfGrid):
            for y in range(sizeOfGrid):
                if self.grid[x][y] == "⬜️":
                    self.openGrid.append((x, y))
        return self.openGrid

    # Creating an dection layout based on the current position of the Grid..
    def CreateDetector(self,k, sizeOfGrid, x_bot,y_bot):
        detectorGridSize = (2*k + 1)
        halfSize = (detectorGridSize - 1) // 2
        x1 = x_bot - halfSize
        y1 = y_bot - halfSize
        for i in range(detectorGridSize):
            for j in range(detectorGridSize):
                # Calculate the coordinates of each cell in the inner grid
                inner_x = x1 + i
                inner_y = y1 + j
                # Check if the inner_x and inner_y are within the bounds of the size of the grid and not block cells
                if 0 <= inner_x < sizeOfGrid and 0 <= inner_y < sizeOfGrid and self.grid[inner_x][inner_y] != "⬛️":
                    self.innerGridCells.append((inner_x, inner_y))
        return self.innerGridCells
   
    
def runMain(k, sizeOfGrid, leaks):
    #from main import k, sizeOfGrid
    Isleak = True
    layout = creatingLayout()
    
    # Generate Layout
    OriginalGrid = layout.Inititate_Grid(sizeOfGrid)
    OpenCells = layout.getOpenGridCell(sizeOfGrid)
    
    # Pick Random Bot Position (x_bot,y_bot)
    pickRandomInt = random.randint(0,len(OpenCells)-1)
    x_bot, y_bot = OpenCells[pickRandomInt]
    OriginalGrid[x_bot][y_bot] = "🤖"
    OpenCells.remove((x_bot,y_bot))
    
    # Create detection Layout with the being the bot position in the center
    detectionGrid = layout.CreateDetector(k, sizeOfGrid, x_bot, y_bot)
    # when there will leak 1 then it will only get the one leak cell
    for (x,y) in detectionGrid:
        if (x,y) in OpenCells:
            OpenCells.remove((x,y))
    # Now checks if k = 1 (Means Leak is only 1) 
    # if Leaks is 2 then if statement will run for the first leak cell
    if len(OpenCells) != 0 and leaks >= 1:
        pickRandomInt = random.randint(0,len(OpenCells)-1)
        x_leak, y_leak = OpenCells[pickRandomInt]
        OriginalGrid[x_leak][y_leak] = "🟥"
    else: 
        # if the given k is higher than says leak is false outside of the detection grid
        Isleak = False
    
    # For testing purpose to check the grid on main grid
    # for (x,y) in detectionGrid:
    #     OriginalGrid[x][y] = "😂"
        
    # Now checks if k = 2 which satisfies here so it will open the second leak cell
    if len(OpenCells) != 0 and leaks > 1:
        # just that second detection is not in the same cell with first leak cell
        OpenCells.remove((x_leak,y_leak)) 
        # appending to detection to add to open grid cell
        pickRandomInt = random.randint(0,len(OpenCells)-1)
        x_leak_1, y_leak_1 = OpenCells[pickRandomInt]
        OriginalGrid[x_leak_1][y_leak_1] = "🟥"
        
    
    # Put Back All the Values of OpenCells
    for (x,y) in detectionGrid:
        if (x,y) not in OpenCells:
            OpenCells.append((x,y))
            
    # These condition only satisfies when the given value of k is much higher
    # so, we will randomly pick leaks cells inside the detection grid
    if Isleak == False:
        pickRandomInt = random.randint(0,len(OpenCells)-1)
        x_leak, y_leak = OpenCells[pickRandomInt]
        OriginalGrid[x_leak][y_leak] = "🟥"
        OpenCells.remove((x_leak,y_leak))
        pickRandomInt = random.randint(0,len(OpenCells)-1)
        x_leak_1, y_leak_1 = OpenCells[pickRandomInt]
        OriginalGrid[x_leak_1][y_leak_1] = "🟥"
    
    # return the Original Grid, detection Grid for bot, and thier co-ordinates
    if leaks == 1:
        return OriginalGrid, detectionGrid, (x_bot,y_bot), (x_leak,y_leak)
    if leaks == 2:
        return OriginalGrid, detectionGrid, (x_bot,y_bot), (x_leak,y_leak), (x_leak_1,y_leak_1)


