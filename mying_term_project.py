#################################################
# Name: Megan Ying
# Andrew ID: mying
# 15-112 Term Project
#################################################

from cmu_112_graphics import *
from math import inf as infinity
import time

# create class for a ball
class Ball(object):
    def __init__(self, row, col, player, color):
        self.row = row
        self.col = col
        self.newRow = None # new row variable for if ball is moving
        self.newCol = None # new column variable for if ball is moving
        self.x0 = -1 # coordinates of ball for if ball is moving
        self.x1 = -1
        self.y0 = -1
        self.y1 = -1
        self.player = player
        self.color = color
        self.isMoving = False
    
#################################################

# set up data
def appStarted(app):
    app.rows = 17
    app.cols = 15
    app.margin = 10
    app.numPlayers = 0
    app.currentPlayer = -1 # whose turn it is
    app.players = [] # set up which players are included in the game
    app.colors = ["red", "purple", "pink", "yellow", "green", "blue"]
    app.board = [([0] * app.cols) for row in range(app.rows)]
    app.boardRows = (1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1)
    app.selection = (-1, -1) # sets up which ball is selected and is equal to
                             # (-1, -1) when no ball is selected
    # possible moves for balls on odd rows
    app.oddMoves = [(-1, 0), (1, 0), (-1, -1), (1, -1), (0, 1), (0, -1)]
    # possible moves for balls on even rows
    app.evenMoves = [(-1, 0), (1, 0), (1, 1), (-1, 1), (0, 1), (0, -1)]
    # starting positions for each ball depending on color
    app.redSpots = {(13, 5), (13, 6), (13, 7), (13, 8), (14, 5), (14, 6), (14, 7),
                    (15, 6), (15, 7), (16, 6)}
    app.purpleSpots = {(12, 9), (11, 10), (10, 10), (9, 11), (12, 10), (11, 11),
                       (10, 11), (11, 12), (12, 11), (12, 12)}
    app.pinkSpots = {(7, 11), (6, 10), (5, 10), (4, 9), (4, 10), (5, 11), (6, 11),
                     (5, 12), (4, 11), (4, 12)}
    app.yellowSpots = {(0, 6), (1, 6), (1, 7), (2, 5), (2, 6), (2, 7), (3, 5),
                       (3, 6), (3, 7), (3, 8)}
    app.greenSpots = {(4, 3), (5, 3), (6, 2), (7, 2), (6, 1), (5, 2), (4, 2),
                      (4, 1), (5, 1), (4, 0)}
    app.blueSpots = {(9, 2), (10, 2), (11, 3), (12, 3), (12, 2), (11, 2), (10, 1),
                     (11, 1), (12, 1), (12, 0)}
    app.isJumping = False # whether the current ball is jumping
    app.gameOver = False
    app.gameStarted = False
    app.givingHint = False
    app.hintBall = (-1, -1) # location of ball that the hint says to move
    app.hintLocation = (-1, -1) # location that the hint says to move to
    app.timeRemaining = 30
    app.currentTime = time.time()
    app.winner = None
    app.balls = set()
    app.AIBalls = []
    app.timerDelay = 15
    setUpPlayers(app)

# set up starting position of pieces on board and the starting player
def setUpPlayers(app):
    isNotValid = True
    while isNotValid:
        app.numPlayers = app.getUserInput("""
Enter the number of players:""")
        # ask user for number of players
        if app.numPlayers in ["1", "2", "4", "6"]: # determine if the number of
                                                   # players is valid
            app.numPlayers = int(app.numPlayers)
            isNotValid = False
        else:
            app.showMessage("""
The answer you entered is not valid. Please enter 1, 2, 4, or 6 players.""")
    if app.numPlayers == 1 or app.numPlayers == 2:
        setUpYellow(app)
        setUpRed(app)
        app.players = [1, 4]
    elif app.numPlayers == 4:
        setUpGreen(app)
        setUpPink(app)
        setUpBlue(app)
        setUpPurple(app)
        app.players = [2, 3, 5, 6]
    else:
        setUpYellow(app)
        setUpRed(app)
        setUpGreen(app)
        setUpPink(app)
        setUpBlue(app)
        setUpPurple(app)
        app.players = [1, 2, 3, 4, 5, 6]
    app.currentPlayer = app.players[0] # set current player to first player in
                                       # list of players
    app.currentTime = time.time() # restart timer
    app.gameStarted = True
                                       
# create new ball at specified row and column with color
def createBall(app, row, col, player, color):
    ball = Ball(row, col, player, color)
    app.balls.add(ball)
    if player == 4 and app.numPlayers == 1:
        app.AIBalls.append(ball) 
    (ball.x0, ball.y0, ball.x1, ball.y1) = getCellBounds(app, row, col)
    app.board[row][col] = ball.player # set cell on board as occupied by player
    
# set up all red balls as player 1
def setUpRed(app):
    for (row, col) in app.redSpots:
        createBall(app, row, col, 1, "red")

# set up all purple balls as player 2  
def setUpPurple(app):
    for (row, col) in app.purpleSpots:
        createBall(app, row, col, 2, "purple2")
    
# set up all pink balls as player 3
def setUpPink(app):
    for (row, col) in app.pinkSpots:
        createBall(app, row, col, 3, "hot pink")

# set up all yellow balls as player 4
def setUpYellow(app):
    for (row, col) in app.yellowSpots:
        createBall(app, row, col, 4, "yellow")

# set up all green balls as player 5
def setUpGreen(app):
    for (row, col) in app.greenSpots:
        createBall(app, row, col, 5, "lime green")

# set up all blue balls as player 6
def setUpBlue(app):
    for (row, col) in app.blueSpots:
        createBall(app, row, col, 6, "deep sky blue")

#################################################

# determine if player 1 won
def redWins(app):
    redSet = set()
    for ball in app.balls:
        if ball.color == "red":
            redSet.add((ball.row, ball.col))
    if redSet == app.yellowSpots:
        app.winner = 1
        return True
    return False

# determine if player 2 won
def purpleWins(app):
    purpleSet = set()
    for ball in app.balls:
        if ball.color == "purple2":
            purpleSet.add((ball.row, ball.col))
    if purpleSet == app.greenSpots:
        app.winner = 2
        return True
    return False

# determine if player 3 won
def pinkWins(app):
    pinkSet = set()
    for ball in app.balls:
        if ball.color == "hot pink":
            pinkSet.add((ball.row, ball.col))
    if pinkSet == app.blueSpots:
        app.winner = 3
        return True
    return False

#determine if player 4 won
def yellowWins(app):
    yellowSet = set()
    for ball in app.balls:
        if ball.color == "yellow":
            yellowSet.add((ball.row, ball.col))
    if yellowSet == app.redSpots:
        app.winner = 4
        return True
    return False

# determine if player 5 won
def greenWins(app):
    greenSet = set()
    for ball in app.balls:
        if ball.color == "lime green":
            greenSet.add((ball.row, ball.col))
    if greenSet == app.purpleSpots:
        app.winner = 5
        return True
    return False

# determine if player 6 won
def blueWins(app):
    blueSet = set()
    for ball in app.balls:
        if ball.color == "deep sky blue":
            blueSet.add((ball.row, ball.col))
    if blueSet == app.pinkSpots:
        app.winner = 6
        return True
    return False

# determine if game ended/if any player won
def gameIsOver(app):
    if (redWins(app) or purpleWins(app) or pinkWins(app) or yellowWins(app) or
        greenWins(app) or blueWins(app)):
        app.currentPlayer = -1
        return True
    return False
    
#################################################

# get the bounding coordinates of a cell in a grid
def getCellBounds(app, row, col):
    gridWidth = app.width - (2 * app.margin)
    gridHeight = app.height - (2 * app.margin)
    cellWidth = min(gridWidth, gridHeight) / app.rows
    offset = cellWidth / 2
    startPoint = ((gridWidth - (cellWidth * app.cols)) / 2) + offset
    if row % 2 == 1:
        x0 = startPoint + (col * cellWidth)
        x1 = startPoint + ((col + 1) * cellWidth)
    else:
        x0 = startPoint + offset + (col * cellWidth)
        x1 = startPoint + offset + ((col + 1) * cellWidth)
    y0 = app.margin + (row * cellWidth)
    y1 = app.margin + ((row + 1) * cellWidth)
    return (x0, y0, x1, y1)

# get the row and column from coordinates
def getCell(app, x, y):
    gridWidth = app.width - (2 * app.margin)
    gridHeight = app.height - (2 * app.margin)
    cellWidth = min(gridWidth, gridHeight) / app.rows
    offset = cellWidth / 2
    startPoint = ((gridWidth - (cellWidth * app.cols)) / 2) + offset
    row = int((y - app.margin) / cellWidth)
    if row % 2 == 1:
        col = int((x - startPoint) / cellWidth)
    else: # offset all even rows
        col = int((x - startPoint - offset) / cellWidth)
    if spotOnBoard(app, row, col): # only send coordinates for cells on board
        return (row, col)
    else:
        return (-1, -1)

# determine if the cell is on the board
def spotOnBoard(app, row, col):
    if row < 0 or row >= app.rows or col < 0 or col >= app.cols:
        return False
    mid = app.cols // 2
    numCols = app.boardRows[row]
    dcol = numCols // 2
    if row % 2 == 1:
        for legalDcol in range(-dcol, dcol):
            if col == (mid + legalDcol):
                return True
    else:
        for legalDcol in range(-dcol - 1, dcol):
            if col == (mid + legalDcol):
                return True
    return False

# determine whether there are balls moving
def ballsMoving(app):
    for ball in app.balls:
        if ball.isMoving:
            return True
    return False

# set ball as moving, set new row and column, mark its previous location as
# unoccupied, and mark its new location as occupied
def moveBall(app, ball, row, col):
    ball.newRow = row
    ball.newCol = col
    ball.isMoving = True
    app.board[ball.row][ball.col] = 0
    app.board[ball.newRow][ball.newCol] = ball.player
    if abs(ball.row - row) > 1 and abs(ball.col - col) > 1:
        app.isJumping = True

# determine if a move is allowed
def isLegalMove(app, ballRow, ballCol, row, col, board):
    if not spotOnBoard(app, row, col):
        return False
    if board[row][col] != 0 or app.gameOver: # check if cell is occupied
                                                 # or game over
        return False
    if ballRow % 2 == 1:
        possibleMoves = app.oddMoves
    else:
        possibleMoves = app.evenMoves
    for (drow, dcol) in possibleMoves: # check if cell is adjacent to selected
                                       # ball's current cell
        newRow = ballRow + drow
        newCol = ballCol + dcol
        if not app.isJumping: # ball can only move one step if not jumping
            if (row, col) == (newRow, newCol):
                return True
        if spotOnBoard(app, newRow, newCol) and board[newRow][newCol] != 0:
            # check if the selected ball can be moved to the new cell by jumping
            # over another ball
                newRow += drow
                newCol += dcol
                if drow != 0: # account for shift in columns
                    if newRow % 2 == 0:
                        newCol -= 1
                    elif newRow % 2 == 1:
                        newCol += 1
                if ((row, col) == (newRow, newCol) and
                    board[newRow][newCol] == 0):
                    return True
    return False

# update all moving balls' coordinates
def timerFired(app):
    if gameIsOver(app): # check if game is over
        app.gameOver = True
    # only start AI turn once current player's ball stops moving
    if app.currentPlayer == 4 and app.numPlayers == 1 and (not ballsMoving(app)):
        moveAI(app)
    if time.time() - app.currentTime >= 30: # change player if timed turn has
                                            # ended
        app.selection = (-1, -1)
        changePlayer(app)
    for ball in app.balls:
        if ball.isMoving:
            (currX0, currY0, currX1, currY1) = getCellBounds(app,
                                                             ball.row, ball.col)
            (newX0, newY0, newX1, newY1) = getCellBounds(app,
                                                         ball.newRow, ball.newCol)
            dx = newX0 - currX0
            dy = newY0 - currY0
            # calculate steps needed to move ball in direction of new location
            stepX = dx / 10
            stepY = dy / 10
            # add step to current coordinates of ball
            ball.x0 += stepX
            ball.y0 += stepY
            ball.x1 += stepX
            ball.y1 += stepY
            if (abs(ball.x0 - newX0) <= 0.1 and abs(ball.y0 - newY0) <= 0.1 and
                abs(ball.x1 - newX1) <= 0.1 and abs(ball.y1 - newY1) <= 0.1):
                # if difference in current location and new location is small,
                # fix its location as the new location and set it to not moving
                ball.isMoving = False
                ball.row = ball.newRow
                ball.col = ball.newCol
    
# move ball when ball is pressed
def mousePressed(app, event):
    if app.givingHint:
        app.givingHint = False
    (row, col) = getCell(app, event.x, event.y)
    checkButtons(app, event.x, event.y)
    if app.selection == (-1, -1):
        for ball in app.balls:
            if ((ball.row, ball.col) == (row, col) and
                ball.player == app.currentPlayer):
                app.selection = (row, col) # select the ball only if it
                                           # corresponds to the current player
    else:
        if ((row, col) == app.selection or app.board[row][col] != 0 or
            not isLegalMove(app, app.selection[0], app.selection[1], row, col,
                            app.board)):
            if app.isJumping:
                changePlayer(app)
                app.isJumping = False # end jumping turn
            app.selection = (-1, -1) # deselect the ball
        elif spotOnBoard(app, row, col):
            for ball in app.balls:
                if ((ball.row, ball.col) == app.selection and
                    isLegalMove(app, app.selection[0], app.selection[1],
                                row, col, app.board)):
                    # if single step move was taken, change player and deselect
                    # ball
                    if abs(ball.row - row) <= 1 and abs(ball.col - col) <= 1:
                        changePlayer(app)
                        app.selection = (-1, -1) # deselect the ball
                        moveBall(app, ball, row, col)
                    # if jump was taken, set selection to new location and set
                    # ball as jumping
                    else:
                        moveBall(app, ball, row, col)
                        app.isJumping = True
                        app.selection = (row, col)

# check if any buttons were clicked
def checkButtons(app, x, y):
    cx, cy = app.width / 2, app.height - (app.height / 15)
    # begin new game if new game button is clicked
    if ((x < cx + 90) and (x > cx - 90) and (y < cy + 20) and (y > cy - 20)):
        appStarted(app)
    cx, cy = app.width - (app.width / 6), app.height / 12
    # give the player a hint if hint button is clicked
    if ((x < cx + 30) and (x > cx - 30) and (y < cy + 20) and (y > cy - 20) and
        app.numPlayers == 1 and app.currentPlayer == 1):
        givePlayerHint(app)
    
# change the player to the next player in list of players
def changePlayer(app):
    currentIndex = app.players.index(app.currentPlayer)
    if app.numPlayers == 1: # account for AI opponent if number of players
                            # entered is equal to 1
        app.currentPlayer = (app.players[(currentIndex + 1) %
                                         (app.numPlayers + 1)])
    else:
        app.currentPlayer = (app.players[(currentIndex + 1) % app.numPlayers])
    app.currentTime = time.time()

#################################################

# move an AI ball based on minimax
def moveAI(app):
    (ballRow, ballCol, newRow, newCol, value) = minimax(app, app.board, 3,
                                                        app.currentPlayer)
    for ball in app.AIBalls:
        if (ball.row, ball.col) == (ballRow, ballCol):
            selectedBall = ball
    moveBall(app, selectedBall, newRow, newCol)
    changePlayer(app)
 
# get all changes in row and column of a ball to make a move
def getAllMoves(app, row, col, state):
    if row % 2 == 1:
        possibleMoves = app.oddMoves
    else:
        possibleMoves = app.evenMoves
    possibleJumps = getAllJumps(app, row, col, state, possibleMoves)
    allPossibleMoves = possibleMoves + possibleJumps
    return allPossibleMoves

# get all changes in row and column of a ball to make a jump
def getAllJumps(app, row, col, state, possibleMoves):
    possibleJumps = []
    for (drow, dcol) in possibleMoves:
        midRow = row + drow
        midCol = col + dcol
        if spotOnBoard(app, midRow, midCol) and state[midRow][midCol] != 0:
        # check to make sure there is an intermmediate ball to jump over
            newDRow = 2 * drow
            newDCol = 2 * dcol
            if drow != 0: # account for shift in columns
                if row % 2 == 0:
                    newDCol -= 1
                else:
                    newDCol += 1
            possibleJumps.append((newDRow, newDCol))
    return possibleJumps

# get all legal changes in row and column of a ball to make a jump
def getAllLegalJumps(app, row, col, state, possibleMoves):
    allLegalJumps = []
    possibleJumps = getAllJumps(app, row, col, state, possibleMoves)
    for (drow, dcol) in possibleJumps:
        newRow = row + drow
        newCol = col + dcol
        if isLegalMove(app, row, col, newRow, newCol, state):
            allLegalJumps.append((drow, dcol)) # check if all possible jumps are
                                               # legal
    return allLegalJumps

# get all changes in row and column of a ball that result in a legal move
def getAllLegalMoves(app, row, col, state):
    allLegalMoves = []
    allPossibleMoves = getAllMoves(app, row, col, state)
    for (drow, dcol) in allPossibleMoves:
        newRow = row + drow
        newCol = col + dcol
        if isLegalMove(app, row, col, newRow, newCol, state):
            allLegalMoves.append((newRow, newCol)) # check if all possible single
                                                   # step moves are legal
    return allLegalMoves

# determine from a state if the human player won
def humanPlayerWins(app, state):
    for (row, col) in app.yellowSpots:
        if state[row][col] != 1:
            return False
    return True

# determine from a state if the AI opponent won
def AIOpponentWins(app, state):
    for (row, col) in app.redSpots:
        if state[row][col] != 4:
            return False
    return True

# determine if a game with an AI has ended
def AIGameOver(app, state):
    return humanPlayerWins(app, state) or AIOpponentWins(app, state)

# determine the value of a state
def getValue(app, state):
    value = 0
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] == 4:
                value += row
            elif state[row][col] == 1:
                value -= (16 - row)
    return value

# decide on best possible move for AI
# https://github.com/Cledersonbc/tic-tac-toe-minimax
# /blob/master/py_version/minimax.py
def minimax(app, state, depth, player):
    if player == 4:
        best = [-1, -1, -1, -1, -infinity] # higher values are more beneficial for
                                           # AI 
        nextPlayer = 1
    else:
        best = [-1, -1, -1, -1, infinity] # lower values are more beneficial for
                                          # player
        nextPlayer = 4
    if depth == 0 or AIGameOver(app, state): 
        score = getValue(app, state)
        return [-1, -1, -1, -1, score]
    currentState = copy.deepcopy(state)
    if not app.isJumping:
        for row in range(app.rows):
            for col in range(app.cols):
                if state[row][col] == player:
                    moves = getAllLegalMoves(app, row, col, state)
                    for (newRow, newCol) in moves:
                        # adjust state to account for changes in ball positions
                        currentState[row][col] = 0
                        currentState[newRow][newCol] = player
                        score = minimax(app, currentState, depth - 1, nextPlayer)
                        # backtrack the state
                        currentState[row][col] = player
                        currentState[newRow][newCol] = 0
                        # adjust score to return best ball to move and best location
                        # to move it to
                        score[0] = row
                        score[1] = col
                        score[2] = newRow
                        score[3] = newCol
                        if player == 4:
                            if score[-1] > best[-1]:
                                best = score
                        else:
                            if score[-1] < best[-1]:
                                best = score
        return best

# use minimax to give the player a hint
def givePlayerHint(app):
    (ballRow, ballCol, newRow, newCol, value) = minimax(app, app.board, 3, 1)
    app.hintBall = (ballRow, ballCol)
    app.hintLocation = (newRow, newCol)
    app.givingHint = True

#################################################

# highlight the selected ball
def highlightSelection(app, canvas):
    if app.selection != (-1, -1) and (not ballsMoving(app)):
        (x0, y0, x1, y1) = getCellBounds(app, app.selection[0], app.selection[1])
        canvas.create_oval(x0, y0, x1, y1, outline = "blue", width = 5)

# highlight possible moves for the selected ball
def highlightPossibleMoves(app, canvas):
    if app.selection != (-1, -1) and (not ballsMoving(app)):
        for row in range(app.rows):
            for col in range(app.cols):
                if isLegalMove(app, app.selection[0], app.selection[1], row, col,
                               app.board):
                    (x0, y0, x1, y1) = getCellBounds(app, row, col)
                    canvas.create_oval(x0, y0, x1, y1, outline = "blue",
                                       width = 5)

# highlight hint for player
def highlightHint(app, canvas):
    if app.givingHint:
        (row, col) = app.hintBall
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, outline = "blue", width = 5)
        (row, col) = app.hintLocation
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, outline = "blue", width = 5)

# draw the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            if spotOnBoard(app, row, col):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_oval(x0, y0, x1, y1)

# draw all balls on the board
def drawBalls(app, canvas):
    for ball in app.balls: # draw stationary balls first to make it appear as if
                           # jumping balls are jumping over stationary balls
        if not ball.isMoving:
            (x0, y0, x1, y1) = getCellBounds(app, ball.row, ball.col)
            canvas.create_oval(x0, y0, x1, y1, fill = ball.color)
    for ball in app.balls:
        if ball.isMoving:
            # if the ball is moving, draw it based on coordinates rather than
            # based on row and column
            canvas.create_oval(ball.x0, ball.y0, ball.x1, ball.y1,
                               fill = ball.color)

# draw texts
def drawMessage(app, canvas):
    cx, cy = app.width / 2, app.height - (app.height / 15)
    message = "Start a new game"
    canvas.create_rectangle(cx - 90, cy - 20, cx + 90, cy + 20,
                            fill = "light gray")
    canvas.create_text(cx, cy, text = message, font = "futura 20")
    if not app.gameOver:
        # display current player
        cy = app.height - (app.height / 6)
        message = "It's " + app.colors[app.currentPlayer - 1] + " player's turn!"
        canvas.create_text(cx, cy, text = message, font = "futura 26")
        if app.isJumping:
            # give instructions about ending turn
            cy = app.height - (app.height / 8)
            message = "Click anywhere on the board to end your turn"
            canvas.create_text(cx, cy, text = message, font = "futura 20")
        # display the remaining time left in a turn
        cx, cy = app.width / 6, app.height / 12
        message = """Time
remaining: """ + str(int(31 - (time.time() - app.currentTime)))
        canvas.create_text(cx, cy, text = message, font = "futura 24")
        if app.numPlayers == 1:
            cx, cy = app.width - (app.width / 6), app.height / 12
            message = "Hint"
            canvas.create_rectangle(cx - 30, cy - 20, cx + 30, cy + 20,
                                    fill = "light gray")
            canvas.create_text(cx, cy, text = message, font = "futura 20")
    else:
        cy = app.height - app.height / 6 # announce winner when game is over
        message = "Congrats " + app.colors[app.winner - 1] + " player! You won!"
        canvas.create_text(cx, cy, text = message, font = "futura 26")
        
def redrawAll(app, canvas):
    if app.gameStarted:
        drawBoard(app, canvas)
        drawBalls(app, canvas)
        drawMessage(app, canvas)
        highlightSelection(app, canvas)
        highlightPossibleMoves(app, canvas)
        highlightHint(app, canvas)

runApp(width = 600, height = 800)
