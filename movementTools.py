'''A collection of functions all functions related to moving a peice that don't actually affect the board in any way'''

nullToken = -1
redToken = 1
redKingToken = 11
blackToken = 2
blackKingToken = 22
staleToken = 0

global boardSize
boardSize = 8 

def red(board, pos):
    if board[pos] == redToken or board[pos] == redKingToken:
        return True
    return False

def black(board, pos):
    if board[pos] == blackToken or board[pos] == blackKingToken:
        return True
    return False

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
