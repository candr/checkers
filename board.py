from collections import deque
import movementTools as MV


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

    if not black(board, move[0]):
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
            board[move[1]] = piece
            board[move[0]] = MV.nullToken
            move.popleft()


        if MV.jumpPossibleBlack(board, move[0]) or (isKing and MV.jumpPossibleRed(board, move[0], True)):
            raise Exception, 'must jump complete chain, jumps are still possible'



if __name__ == "__main__":
    board = newBoard()
    board[17] = MV.blackKingToken
    board[6] = MV.nullToken
    board[22] = MV.redKingToken
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


