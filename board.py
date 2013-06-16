from collections import deque

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

nullToken = -1
redToken = 1
redKingToken = 11
blackToken = 2
blackKingToken = 22
staleToken = 0

boardSize = 8 

def red(board, pos):
    if board[pos] == redToken or board[pos] == redKingToken:
        return True
    return False

def black(board, pos):
    if board[pos] == blackToken or board[pos] == blackKingToken:
        return True
    return False

def newBoard():
    board =  [blackToken,blackToken,blackToken,blackToken,\
              blackToken,blackToken,blackToken,blackToken,\
              blackToken,blackToken,blackToken,blackToken,\
              nullToken,nullToken,nullToken,nullToken,\
              nullToken,nullToken,nullToken,nullToken,\
              redToken,redToken,redToken,redToken,\
              redToken,redToken,redToken,redToken,\
              redToken,redToken,redToken,redToken]
    return board

def showBoard(board):
    line = ""
    for i in range(boardSize*boardSize):
        line = line + '|'
        if ((i%2 != 0) if ((i/boardSize)%2 == 0) else (i%2 == 0)) :
            if board[i/2] == nullToken:
                line = line + '-'
            elif board[i/2] == redToken:
                line = line + 'r'
            elif board[i/2] == redKingToken:
                line = line + 'R'
            elif board[i/2] == blackToken:
                line = line + 'b'
            elif board[i/2] == blackKingToken:
                line = line + 'B'
        else:
            line = line + '~'

        if i%boardSize == boardSize - 1:
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
    isKing = True if piece == redKingToken else False

    if not red(board, move[0]):
        raise Exception, 'Moving a red piece in the black move function'
    if board[move[1]] != nullToken:
        raise Exception, 'Moving to an occupied space'
    if move[1] > 31:
        raise Exception, 'Moving off the board'
    if move[1] < 0:
        raise Exception, 'Moving off the board'

    simpleDests = enumerateSimpleMovesRed(move[0])
    if isKing:
        simpleDests = simpleDests | enumerateSimpleMovesBlack(move[0])

    if move[1] in simpleDests:
        if jumpPossibleRed(board, move[0]) or (isKing and jumpPossibleBlack(board, move[0], True)):
            raise Exception, 'must jump if able'
        board[move[1]] = piece
        board[move[0]] = nullToken
    else:
        while len(move) > 1:
            jumpDests = enumerateJumpMovesRed(move[0])
            if isKing:
                jumpDests = jumpDests | enumerateJumpMovesBlack(move[0])

            if move[1] not in jumpDests:
                raise Exception, 'Invalid:  move is not on the list of valid moves' 
            if move[1] > 31:
                raise Exception, 'Moving off the board'
            if move[1] < 0:
                raise Exception, 'Moving off the board'

            #going left
            if move[1] + 8 == move[0]-1:
                blackPos = move[0] - (3 + ((move[0]/4)%2) + 1)

            #going right
            if move[1] + 8 == move[0]+1:
                blackPos = move[0] - (3 + ((move[0]/4)%2))

            if isKing:
                #Going left
                if move[1] - 8 == move[0]-1:
                   blackPos = move[0] + (4 - ((move[0]/4)%2))

                #Going Right
                if move[1] - 8 == move[0]+1:
                   blackPos = move[0] + (4 - ((move[0]/4)%2) + 1)


            if not black(board, blackPos):
                raise Exception, 'Attempting to jump over a black nor empty square'
            else:
                board[blackPos] = nullToken
            board[move[1]] = piece
            board[move[0]] = nullToken
            move.popleft()


        if jumpPossibleRed(board, move[0]) or (isKing and jumpPossibleBlack(board, move[0], True)):
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
    isKing = True if piece == blackKingToken else False

    if not black(board, move[0]):
        raise Exception, 'Moving a red piece in the black move function'
    if board[move[1]] != nullToken:
        raise Exception, 'Moving to an occupied space'
    if move[1] > 31:
        raise Exception, 'Moving off the board'
    if move[1] < 0:
        raise Exception, 'Moving off the board'

    simpleDests = enumerateSimpleMovesBlack(move[0])
    if isKing:
        simpleDests = simpleDests | enumerateSimpleMovesRed(move[0])

    if move[1] in simpleDests:
        if jumpPossibleBlack(board, move[0]) or (isKing and jumpPossibleRed(board, move[0], True)):
            raise Exception, 'must jump if able'
        board[move[1]] = piece
        board[move[0]] = nullToken
    else:
        while len(move) > 1:
            jumpDests = enumerateJumpMovesBlack(move[0])
            if isKing:
                jumpDests = jumpDests | enumerateJumpMovesRed(move[0])

            if move[1] not in jumpDests:
                raise Exception, 'Invalid:  move is not on the list of valid moves' 
            if move[1] > 31:
                raise Exception, 'Moving off the board'
            if move[1] < 0:
                raise Exception, 'Moving off the board'

            #Going left
            if move[1] - 8 == move[0]-1:
               redPos = move[0] + (4 - ((move[0]/4)%2))

            #Going Right
            if move[1] - 8 == move[0]+1:
               redPos = move[0] + (4 - ((move[0]/4)%2) + 1)

            if isKing:
                #going left
                if move[1] + 8 == move[0]-1:
                    redPos = move[0] - (3 + ((move[0]/4)%2) + 1)

                #going right
                if move[1] + 8 == move[0]+1:
                    redPos = move[0] - (3 + ((move[0]/4)%2))


            if not red(board, redPos):
                raise Exception, 'Attempting to jump over a black nor empty square'
            else:
                board[redPos] = nullToken
            board[move[1]] = piece
            board[move[0]] = nullToken
            move.popleft()


        if jumpPossibleBlack(board, move[0]) or (isKing and jumpPossibleRed(board, move[0], True)):
            raise Exception, 'must jump complete chain, jumps are still possible'

def enumerateSimpleMovesBlack(start):
    '''returns all the valid simple movements from position start as a set'''
    '''assumes travel towards the red side of the board'''
    #These are the possible moves if we aren't jumping
    nonjumpPlaces = [] 
    #To the left
    if (start/4)%2 == 0 or start%4 != 0:
        simpLeft = start + (4 - ((start/4)%2))
        if simpLeft < 32:
            nonjumpPlaces.append(simpLeft)

    #To the right
    if (start/4)%2 != 0 or start%4 != 3:
        simpRight = start + (4 - ((start/4)%2)) + 1
        if simpRight < 32:
            nonjumpPlaces.append(simpRight)

    return set(nonjumpPlaces)

def enumerateSimpleMovesRed(start):
    '''returns all the valid simple movements from position start as a set'''
    '''assumes travel towards the black side of the board'''
    #These are the possible moves if we aren't jumping
    nonjumpPlaces = [] 
    #To the left
    if (start/4)%2 == 0 or start%4 != 0:
        simpLeft = start - (3 + ((start/4)%2) + 1)
        if simpLeft >= 0:
            nonjumpPlaces.append(simpLeft)

    #To the right
    if (start/4)%2 != 0 or start%4 != 3:
        simpRight = start - (3 + ((start/4)%2))
        if simpRight >= 0:
            nonjumpPlaces.append(simpRight)

    return set(nonjumpPlaces)

def enumerateJumpMovesBlack(start):
    '''returns all jumps possible from a position, without considering if a red peice is in place to be jumped over'''
    '''assumes travel towards the red side of the board'''
    jumpPlaces = []

    #To the left
    if start%4 != 0 and start + 7 < 32:
        jumpPlaces.append(start + 7)
    #To the right
    if start%4 != 3 and start + 9 < 32:
        jumpPlaces.append(start + 9)

    return set(jumpPlaces)

def enumerateJumpMovesRed(start):
    '''returns all jumps possible from a position, without considering if a red peice is in place to be jumped over'''
    '''assumes travel towards the black side of the board'''
    jumpPlaces = []

    #To the left
    if start%4 != 0 and start - 9 >= 0:
        jumpPlaces.append(start - 9)
    #To the right
    if start%4 != 3 and start - 7 >= 0:
        jumpPlaces.append(start - 7)

    return set(jumpPlaces)

def jumpPossibleBlack(board, start, isRedKing = False):
    '''Given the current situation on the board, returns whether a jump is possible from position start. It assumes that there is a black tile on start'''
    '''isRedKing will be True if this fcn is being called for a red king'''
    simpLeft = -1
    simpRight = -1
    #To the left
    if (start/4)%2 == 0 or start%4 != 0:
        simpLeft = start + (4 - ((start/4)%2))
        if simpLeft > 31:
            simpLeft = -1

    #To the right
    if (start/4)%2 != 0 or start%4 != 3:
        simpRight = start + (4 - ((start/4)%2)) + 1
        if simpRight > 31:
            simpRight = -1
    

    jumpLeft = -1 
    jumpRight = -1
    #To the left
    if start%4 != 0 and start + 7 < 32:
        jumpLeft = (start + 7)
    #To the right
    if start%4 != 3 and start + 9 < 32:
        jumpRight = (start + 9)

    if (simpLeft != -1 and jumpLeft != -1 and board[jumpLeft] == nullToken and (black(board, simpLeft) if isRedKing else red(board, simpLeft))) \
       or (simpRight != -1 and jumpRight != -1 and board[jumpRight] == nullToken and (black(board, simpRight) if isRedKing else red(board, simpRight))):
        return True

    return False

def jumpPossibleRed(board, start, isBlackKing = False):
    '''Given the current situation on the board, returns whether a jump is possible from position start. It assumes that there is a red tile on start'''
    '''isRedKing will be True if this fcn is being called for a red king'''
    simpLeft = -1
    simpRight = -1
    #To the left
    if (start/4)%2 == 0 or start%4 != 0:
        simpLeft = start - (3 + ((start/4)%2) + 1)
        if simpLeft < 0:
            simpLeft = -1

    #To the right
    if (start/4)%2 != 0 or start%4 != 3:
        simpRight = start - (3 + ((start/4)%2))
        if simpRight < 0:
            simpRight = -1
    

    jumpLeft = -1 
    jumpRight = -1
    #To the left
    if start%4 != 0 and start - 9 >= 0:
        jumpLeft = (start - 9)
    #To the right
    if start%4 != 3 and start - 7 >= 0:
        jumpRight = (start - 7)

    if (simpLeft != -1 and jumpLeft != -1 and board[jumpLeft] == nullToken and (red(board, simpLeft) if isBlackKing else black(board, simpLeft))) \
       or (simpRight != -1 and jumpRight != -1 and board[jumpRight] == nullToken and (red(board, simpRight) if isBlackKing else black(board, simpRight))):
        return True

    return False


if __name__ == "__main__":
    board = newBoard()
    board[17] = blackKingToken
    board[6] = nullToken
    board[22] = redKingToken
    moveRedPiece(board,[22,13,6,15])
    '''
    for i in range(32):
        s = 'moves from ' + repr(i + 1) + ' are '
        #m = enumerateSimpleMovesBlack(i)
        #m = enumerateJumpMovesBlack(i)
        #m = enumerateSimpleMovesRed(i)
        #m = enumerateJumpMovesRed(i)
        while(len(m) > 0):
            s = s + repr(m.pop()+ 1) + ', '
        print s
    '''
    showBoard(board)


