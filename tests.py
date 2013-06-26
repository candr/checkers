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

def testSimpleMoveEnumerator():
	b = MV.enumerateSimpleMovesRed(19)
	print b

def testJumpMoveEnumerator():
	b = MV.enumerateJumpMovesRed(16)
	print b

if __name__ == "__main__":
	testValidMoveGeneratorI()
	testValidMoveGeneratorII()
	testValidMoveGeneratorIII()
	testValidMoveGeneratorIV()
	testValidMoveGeneratorV()
	testValidMoveGeneratorVI()
	testSimpleMoveEnumerator()
	testJumpMoveEnumerator()
