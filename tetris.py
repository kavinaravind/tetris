#kavinaravind
#------------------------------------------------------------------------------------------------------------------

from Tkinter import *
import random

def run(rows, cols):
    global canvas
    root = Tk()
    canvas = Canvas(root, height=34*rows, width=35*cols, background="orange")
    canvas.pack()
    root.resizable(width=0, height=0)
    root.canvas = canvas.canvas = canvas
    class Struct:pass
    canvas.data=Struct()
    canvas.data.rows=rows
    canvas.data.cols=cols
    init()
    root.bind("<Key>", keyPressed)
    timerFired()
    root.mainloop()

def init():
    loadBoard()
    tetrisPieces = standardPieces()
    tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors
    canvas.data.isGameOver = False
    canvas.data.score = 0
    newFallingPiece()
    redrawAll()
    
def loadBoard():
    rows=canvas.data.rows
    cols=canvas.data.cols
    board=[]
    for row in xrange(rows):
        newRow = []
        for col in xrange(cols):
            newRow.append("blue")
        board.append(newRow)
    canvas.data.board = board
    
def redrawAll():
    canvas.delete(ALL)
    drawGame()
    
def drawGame():
    drawBoard()
    drawFallingPiece()
    canvas.create_text(300,500,text="Score:" + str(canvas.data.score))
    if canvas.data.isGameOver == True:
        canvas.create_text(110,18,text="Game Over Press r to Restart!!! :)")

def drawBoard():
    board=canvas.data.board
    for row in range(len(board)):
        for col in range (len(board[0])):
            cellColor=board[row][col]
            drawCell(board,row,col,cellColor)

def standardPieces():
    iPiece = [
        [ True,  True,  True,  True]
    ]

    jPiece = [
        [ True, False, False ],
        [ True, True,  True]
    ]
  
    lPiece = [
        [ False, False, True],
        [ True,  True,  True]
    ]
  
    oPiece = [
        [ True, True],
        [ True, True]
    ]

    sPiece = [
        [ False, True, True],
        [ True,  True, False ]
    ]

    tPiece = [
        [ False, True, False ],
        [ True,  True, True]
    ]

    zPiece = [
        [ True,  True, False ],
        [ False, True, True]
    ]
    return [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]

def newFallingPiece():
    pieces=canvas.data.tetrisPieces
    pieceIndex=random.randint(0,6)
    canvas.data.fallingPiece =  pieces[pieceIndex]
    colors=canvas.data.tetrisPieceColors
    canvas.data.fallingPieceColor =  colors[pieceIndex]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 - len(canvas.data.fallingPiece[0])/2

def drawFallingPiece():
    board=canvas.data.board
    fallingPiece=canvas.data.fallingPiece
    for row in xrange(len(fallingPiece)):
        for col in xrange(len(fallingPiece[0])):
            if fallingPiece[row][col]==True:
                drawCell(board, canvas.data.fallingPieceRow + row, canvas.data.fallingPieceCol + col, canvas.data.fallingPieceColor)

def moveFallingPiece(drow, dcol):
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if fallingPieceIsLegal()==False:
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    else:
        return True
    
def fallingPieceIsLegal():
    board=canvas.data.board
    rows=canvas.data.rows
    cols=canvas.data.cols
    fallingPiece=canvas.data.fallingPiece
    for row in xrange(len(fallingPiece)):
        for col in xrange(len(fallingPiece[0])):
            if fallingPiece[row][col]==True:
                pieceRow= canvas.data.fallingPieceRow + row
                pieceCol= canvas.data.fallingPieceCol + col
                if pieceRow >= rows or pieceRow < 0:
                    return False
                if pieceCol >= cols or pieceCol < 0:
                    return False
                if canvas.data.board[pieceRow][pieceCol] != "blue":
                    return False
    return True

def rotateFallingPiece():
    fallingPiece = canvas.data.fallingPiece
    locationRow = canvas.data.fallingPieceRow
    locationCol = canvas.data.fallingPieceCol
    rotatedPiece =[]
    for col in xrange(len(fallingPiece[0])-1, -1, -1):
        newRowList=[]
        for row in xrange(len(fallingPiece)):
            newRowList.append(fallingPiece[row][col])
        rotatedPiece.append(newRowList)
    canvas.data.fallingPiece = rotatedPiece
    if fallingPieceIsLegal()==False:
        canvas.data.fallingPiece = fallingPiece

def timerFired():
    if moveFallingPiece(1,0)==False:
        placeFallingPiece()
        if canvas.data.isGameOver != True:
            newFallingPiece()
        if fallingPieceIsLegal()==False:
            canvas.data.isGameOver = True
    removeFullRows()
    redrawAll()
    delay = 500
    canvas.after(delay, timerFired)
      
def placeFallingPiece():
    board=canvas.data.board
    fallingPiece=canvas.data.fallingPiece
    for row in xrange(len(fallingPiece)):
        for col in xrange(len(fallingPiece[0])):
            if fallingPiece[row][col]==True:
                board[canvas.data.fallingPieceRow + row][canvas.data.fallingPieceCol + col]=canvas.data.fallingPieceColor
    
def keyPressed(event):
    if event.keysym == "Up":
        rotateFallingPiece()
    elif event.keysym == "Down":
        moveFallingPiece(1,0)
    elif event.keysym == "Left":
        moveFallingPiece(0,-1)
    elif event.keysym == "Right":
        moveFallingPiece(0,1)
    elif event.keysym == "n":
        newFallingPiece()
    elif event.keysym == "r":
        init()
    redrawAll()    

def removeFullRows():
    board=canvas.data.board
    availableIndex=len(board)-1
    score = 0
    for row in xrange(len(board) -1, -1, -1):
        notFull=0
        newRow=[]
        for col in xrange(len(board[0])):
            if board[row][col] == "blue":
                notFull+=1
        if notFull>0:
            for color in board[row]:
                newRow.append(color)
            board[availableIndex]=newRow
            availableIndex -= 1
        else:
            score += 1
    canvas.data.score += score**2
                
def drawCell(board,row,col,cellColor):
    board=canvas.data.board
    margin = 30
    cellSize=30
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill=cellColor, width=4)
  
run(15,10)
