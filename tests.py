'''This is the start of my unit test framework. Soon, I should use an actual unit testing lib'''
import movementTools as MV
import board as BD

#testing only one valid jump
#-~b
#~r~
def testValidMoveGeneratorI():
	b = [MV.nullToken for i in range(32)]
	b[18] = MV.blackToken
	b[10] = MV.blackToken
	b[11] = MV.blackToken
	b[22] = MV.redToken
	BD.showBoard(b)
	
	jumpsValid = MV.buildJumpTreeRed(22, b, [], False)
	print jumpsValid
#Test we can't jump over our own
#r~b
#~r~
def testValidMoveGeneratorII():
	b = [MV.nullToken for i in range(32)]
	b[18] = MV.blackToken
	b[10] = MV.blackToken
	b[11] = MV.blackToken
	b[17] = MV.redToken
	b[22] = MV.redToken
	BD.showBoard(b)
	jumpsValid = MV.buildJumpTreeRed(22, b, [], False)
	print jumpsValid

#Test we can jump over all of them
#b~b
#~r~
def testValidMoveGeneratorIII():
	b = [MV.nullToken for i in range(32)]
	b[18] = MV.blackToken
	b[10] = MV.blackToken
	b[11] = MV.blackToken
	b[17] = MV.blackToken
	b[22] = MV.redToken
	BD.showBoard(b)
	jumpsValid = MV.buildJumpTreeRed(22, b, [], False)
	print jumpsValid
	

#Test empty jump list 
#-~-
#~r~
def testValidMoveGeneratorIV():
	b = [MV.nullToken for i in range(32)]
	b[22] = MV.redToken
	BD.showBoard(b)
	jumpsValid = MV.buildJumpTreeRed(22, b, [], False)
	print jumpsValid

#Test extended jump sequence
#b~b~b
#~b~b~
#-~r~-
def testValidMoveGeneratorV():
	b = [MV.nullToken for i in range(32)]
	b[16] = MV.blackToken
	b[17] = MV.blackToken
	b[19] = MV.blackToken
	b[26] = MV.blackToken
	b[25] = MV.blackToken
	b[30] = MV.redToken
	BD.showBoard(b)
	jumpsValid = MV.buildJumpTreeRed(30, b, [], False)
	print jumpsValid

#Test we get all king moves
#b~b
#~R~
#b~b
def testValidMoveGeneratorVI():
	b = [MV.nullToken for i in range(32)]
	b[21] = MV.blackToken
	b[14] = MV.blackToken
	b[13] = MV.blackToken
	b[17] = MV.redKingToken
	b[22] = MV.blackToken
	BD.showBoard(b)
	jumpsValid = MV.buildJumpTreeRed(17, b, [], True)
	print jumpsValid

#test loops with king jumps
#~R~
#b~b
#~-~
#b~b
def loopTestI():
	b = [MV.nullToken for i in range(32)]
	b[9] = MV.redKingToken
	b[13] = MV.blackToken
	b[21] = MV.blackToken
	b[22] = MV.blackToken
	b[14] = MV.blackToken
	BD.showBoard(b)
	jumpsValid = MV.jumpTreeRed(9, b, True)
	print jumpsValid

#test loops with king jumps
#b~-
#~R~
#b~b
#~-~
#b~b
def loopTestII():
	b = [MV.nullToken for i in range(32)]
	b[9] = MV.redKingToken
	b[13] = MV.blackToken
	b[21] = MV.blackToken
	b[22] = MV.blackToken
	b[14] = MV.blackToken
	b[5] = MV.blackToken
	BD.showBoard(b)
	jumpsValid = MV.jumpTreeRed(9, b, True)
	print jumpsValid

def testSimpleMoveEnumerator():
	b = MV.enumerateSimpleMovesRed(19)
	print b

def testJumpMoveEnumerator():
	b = MV.enumerateJumpMovesRed(16)
	print b

def testAllMovesRed():
	b = [MV.nullToken for i in range(32)]
	b[17] = MV.redToken
	b[9] = MV.redKingToken
	b[13] = MV.blackToken
	b[14] = MV.blackKingToken
	b[0] = MV.redToken
	b[15] = MV.redToken
	b[11] = MV.blackToken
	b[19] = MV.redToken
	b[27] = MV.redKingToken
	b[21] = MV.blackToken
	b[22] = MV.blackToken
	BD.showBoard(b)

	print MV.allPossibleMovesRed(b)

def testAllMovesBlack():
	b = [MV.nullToken for i in range(32)]
	b[17] = MV.blackToken
	b[9] = MV.blackKingToken
	b[13] = MV.redToken
	b[14] = MV.redKingToken
	b[29] = MV.blackToken
	b[15] = MV.blackToken
	b[11] = MV.blackToken
	b[19] = MV.redToken
	b[21] = MV.redToken
	b[22] = MV.redToken
	BD.showBoard(b)

	print MV.allPossibleMovesBlack(b)

def testKingSimpleBlack():
	b = [MV.nullToken for i in range(32)]
	b[8] = MV.blackKingToken
	b[10] = MV.blackKingToken
	b[6] = MV.blackToken
	b[2] = MV.blackKingToken
	b[31] = MV.blackKingToken
	b[11] = MV.blackKingToken
	b[20] = MV.blackKingToken
	BD.showBoard(b)

	print MV.allPossibleMovesBlack(b)

def testEndConditionI():
	b = [MV.nullToken for i in range(32)]
	print MV.allPossibleMovesBlack(b)

def testEndConditionII():
	b = [MV.nullToken for i in range(32)]
	print MV.allPossibleMovesRed(b)

def testEndConditionIII():
	b = [MV.nullToken for i in range(32)]
	b[0] = MV.redToken
	b[4] = MV.blackToken
	b[5] = MV.blackToken
	b[9] = MV.blackToken
	print MV.allPossibleMovesRed(b)

if __name__ == "__main__":
	testGenerator = False
	if testGenerator:
		testValidMoveGeneratorI()
		testValidMoveGeneratorII()
		testValidMoveGeneratorIII()
		testValidMoveGeneratorIV()
		testValidMoveGeneratorV()
		testValidMoveGeneratorVI()
	
	testEnumerator = False
	if testEnumerator:
		testSimpleMoveEnumerator()
		testJumpMoveEnumerator()

	testAllMove = False
	if testAllMove:
		testAllMovesRed()
		testKingSimpleBlack()
		testAllMovesBlack()

	testLoop = False
	if testLoop:
		loopTestI()
		loopTestII()

	testEndCondition = True
	if testEndCondition:
		testEndConditionI()
		testEndConditionII()
		testEndConditionIII()
