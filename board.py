from collections import deque
import movementTools as MV
import pygame, sys
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
HGREEN = (105, 205, 50)
BROWN = (205, 170, 125)

CELLSIZE = 50
PEICERAD = 20

boardOffset = {'x':10, 'y':10}

'''
A game of checkers
board is stored in shorthand
The eventual goal is to be able to swap out AIs

--00--01--02--03
04--05--06--07--
--08--09--10--11
12--13--14--15--
--16--17--18--19
20--21--22--23--
--24--25--26--27
28--29--30--31--

'''


def newBoard():
    board =  [MV.blackToken,MV.blackToken,MV.blackToken,MV.blackToken,\
              MV.blackToken,MV.blackToken,MV.blackToken,MV.blackToken,\
              MV.blackToken,MV.blackToken,MV.blackToken,MV.blackToken,\
              MV.nullToken,MV.nullToken,MV.nullToken,MV.nullToken,\
              MV.nullToken,MV.nullToken,MV.nullToken,MV.nullToken,\
              MV.redToken,MV.redToken,MV.redToken,MV.redToken,\
              MV.redToken,MV.redToken,MV.redToken,MV.redToken,\
              MV.redToken,MV.redToken,MV.redToken,MV.redToken]
    return board

def showBoard(board):
    line = ""
    for i in range(64):
        line = line + '|'
        if ((i%2 != 0) if ((i/8)%2 == 0) else (i%2 == 0)) :
            if board[i/2] == MV.nullToken:
                line = line + '-'
            elif board[i/2] == MV.redToken:
                line = line + 'r'
            elif board[i/2] == MV.redKingToken:
                line = line + 'R'
            elif board[i/2] == MV.blackToken:
                line = line + 'b'
            elif board[i/2] == MV.blackKingToken:
                line = line + 'B'
        else:
            line = line + '~'

        if i%8 == 7:
            print line
            line = ""


def moveRedPiece(board, move):
    '''move is denoted in shorthand as list, with the first position being the current position of the peice and the rest prospective destinations
    Movement in red & black is different enough to need 2 functions
    Otherwise this function would be a mess of if red .. if black ..
    Noone wants that
    Except for Mussolini, which is another good reason to do it this way
    Mostly this function validates a move, and throws an exception if the move is illegal
    '''
    move = deque(move)
    piece = board[move[0]]
    isKing = True if piece == MV.redKingToken else False

    if not MV.red(board, move[0]):
        raise Exception, 'Moving a red piece in the black move function'
    if board[move[1]] != MV.nullToken:
        raise Exception, 'Moving to an occupied space'
    if move[1] > 31:
        raise Exception, 'Moving off the board'
    if move[1] < 0:
        raise Exception, 'Moving off the board'

    simpleDests = MV.enumerateSimpleMovesRed(move[0])
    if isKing:
        simpleDests = simpleDests | MV.enumerateSimpleMovesBlack(move[0])

    if move[1] in simpleDests:
        if MV.jumpPossibleRed(board, move[0]) or (isKing and MV.jumpPossibleBlack(board, move[0], True)):
            raise Exception, 'must jump if able'
	#if it gets to the last row
	if move[1] in range(4):
	    piece = MV.redKingToken
        board[move[1]] = piece
        board[move[0]] = MV.nullToken
    else:
        while len(move) > 1:
            jumpDests = MV.enumerateJumpMovesRed(move[0])
            if isKing:
                jumpDests = jumpDests | MV.enumerateJumpMovesBlack(move[0])

            if move[1] not in jumpDests:
                raise Exception, 'Invalid:  move is not on the list of valid moves' 
            if move[1] > 31:
                raise Exception, 'Moving off the board'
            if move[1] < 0:
                raise Exception, 'Moving off the board'
	
            blackPos = MV.jumpIsValidRed(move[0], move[1], board, isKing)

	    if blackPos is not False:
                board[blackPos] = MV.nullToken
            else:
                raise Exception, 'Attempting to jump over a red or empty square'
	    #if it gets to the last row
	    if move[1] in range(4):
	        piece = MV.redKingToken
                isKing = True
            board[move[1]] = piece
            board[move[0]] = MV.nullToken
            move.popleft()


        if MV.jumpPossibleRed(board, move[0]) or (isKing and MV.jumpPossibleBlack(board, move[0], True)):
            raise Exception, 'must jump complete chain, jumps are still possible'
    	


def moveBlackPiece(board, move):
    '''move is denoted in shorthand as list, with the first position being the current position of the peice and the rest prospective destinations
    Movement in red & black is different enough to need 2 functions
    Otherwise this function would be a mess of if red .. if black ..
    Noone wants that
    Except for Mussolini, which is another good reason to do it this way
    Mostly this function validates a move, and throws an exception if the move is illegal
    '''
    move = deque(move)
    piece = board[move[0]]
    isKing = True if piece == MV.blackKingToken else False

    if not MV.black(board, move[0]):
        raise Exception, 'Moving a red piece in the black move function'
    if board[move[1]] != MV.nullToken:
        raise Exception, 'Moving to an occupied space'
    if move[1] > 31:
        raise Exception, 'Moving off the board'
    if move[1] < 0:
        raise Exception, 'Moving off the board'

    simpleDests = MV.enumerateSimpleMovesBlack(move[0])
    if isKing:
        simpleDests = simpleDests | MV.enumerateSimpleMovesRed(move[0])

    if move[1] in simpleDests:
        if MV.jumpPossibleBlack(board, move[0]) or (isKing and MV.jumpPossibleRed(board, move[0], True)):
            raise Exception, 'must jump if able'
	#if it gets to the last row
	if move[1] in range(28,32):
	    piece = MV.blackKingToken
        board[move[1]] = piece
        board[move[0]] = MV.nullToken
    else:
        while len(move) > 1:
            jumpDests = MV.enumerateJumpMovesBlack(move[0])
            if isKing:
                jumpDests = jumpDests | MV.enumerateJumpMovesRed(move[0])

            if move[1] not in jumpDests:
                raise Exception, 'Invalid:  move is not on the list of valid moves' 
            if move[1] > 31:
                raise Exception, 'Moving off the board'
            if move[1] < 0:
                raise Exception, 'Moving off the board'

            redPos = MV.jumpIsValidBlack(move[0], move[1], board, isKing)

	    if redPos is not False:
                board[redPos] = MV.nullToken
            else:
                raise Exception, 'Attempting to jump over a black or empty square'
	    #if it gets to the last row
	    if move[1] in range(28,32):
	        piece = MV.blackKingToken
                isKing = True
            board[move[1]] = piece
            board[move[0]] = MV.nullToken
            move.popleft()


        if MV.jumpPossibleBlack(board, move[0]) or (isKing and MV.jumpPossibleRed(board, move[0], True)):
            raise Exception, 'must jump complete chain, jumps are still possible'


def initGUI():
    pygame.init()
    pygame.display.set_caption('Checkers')
    return pygame.display.set_mode((500, 500), 0, 32)

def drawBoardGUI(DISPLAYSURF, board):
    DISPLAYSURF.fill(WHITE)
    pygame.draw.rect(DISPLAYSURF, BROWN, (boardOffset['x'],  boardOffset['y'], CELLSIZE * 8, CELLSIZE * 8))
    for i in range(8):
        for j in range(4):
            x = 2*j*CELLSIZE + ((i+1)%2)*CELLSIZE + boardOffset['x']
            y = i * CELLSIZE + boardOffset['y']
            pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
            if board[i*4 + j] != MV.nullToken:
                x += CELLSIZE/2
                y += CELLSIZE/2
                if board[i*4 + j] == MV.blackToken:
                    pygame.draw.circle(DISPLAYSURF, BLACK, (x, y), PEICERAD)
                if board[i*4 + j] == MV.redToken:
                    pygame.draw.circle(DISPLAYSURF, RED, (x, y), PEICERAD)
    
    

def convertPosToCell(pos, offset):
    gridNum = (((pos[1]-offset['y'])/CELLSIZE)*8) + (pos[0]-offset['x'])/CELLSIZE
    oddRow = (gridNum/8)%2

    if gridNum%2 != oddRow:
        return gridNum/2
    else:
        return None

def convertCellToPos(cell, offset):
    x = cell%4 * 2
    y = (cell*2)/8

    evenRow = (y+1)%2

    x = (x + evenRow) * CELLSIZE + offset['x']
    y = y * CELLSIZE + offset['y']

    return {'x':x, 'y':y}

def selectingBoard(pos, offset):
    if pos[1] > offset['y'] and \
       pos[0] > offset['x'] and \
       pos[1] < 8 * CELLSIZE + offset['y'] and \
       pos[0] < 8 * CELLSIZE + offset['x']:
           return True

    return False

class human:
    def __init__(self, isRed):
        self.isRed = isRed
        self.move = []

    def selectCell(self):
        for event in pygame.event.get(MOUSEBUTTONDOWN):
            if selectingBoard(event.pos, boardOffset):
                cell = convertPosToCell(event.pos, boardOffset)
                if cell != None:
                    self.move.append(cell)

    def getMove(self):
        return self.move


def highlightMove(DISPLAYSURF, board, move):
    for cell in move:
        pos = convertCellToPos(cell, boardOffset)
        pygame.draw.rect(DISPLAYSURF, HGREEN, (pos['x'], pos['y'], CELLSIZE, CELLSIZE))
        if board[cell] != MV.nullToken:
            x = pos['x'] + CELLSIZE/2
            y = pos['y'] + CELLSIZE/2
            if board[cell] == MV.blackToken:
                pygame.draw.circle(DISPLAYSURF, BLACK, (x, y), PEICERAD)
            if board[cell] == MV.redToken:
                pygame.draw.circle(DISPLAYSURF, RED, (x, y), PEICERAD)




if __name__ == "__main__":
    DIS = initGUI()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN])
    board = newBoard()
    redTurn = False 
    red = human(True)
    black = human(False)
    while(True):
        drawBoardGUI(DIS, board)
        red.selectCell()
        move = red.getMove()
        highlightMove(DIS, board, move)
        pygame.display.update()
        for event in pygame.event.get(QUIT):
			pygame.quit()
			sys.exit()


        '''
        if redTurn:
            moveList = MV.allPossibleMovesRed(board)
            if len(moveList) == 0:
                print "Black wins"
                break
            move = humanMoveRed(board)
            if move != None: 
                moveRedPiece(board, moves[moveSelected])
        else:
            moveList = MV.allPossibleMovesBlack(board)
            if len(moveList) == 0:
                print "Red wins"
                break
            moves = {x: moveList[x] for x in range(len(moveList))} 
            print moves
            moveSelected = input("Select a move\n")
            moveBlackPiece(board, moves[moveSelected])
        redTurn = not redTurn
        '''
