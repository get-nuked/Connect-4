import board
import game
import player
import randomPlayer
import humanPlayer
from datetime import datetime

wins = 0
winsAndDraws = 0
losses = 0
meanBranchesPruned = 0.0
M2BranchesPruned = 0.0
meanNumberOfNodesExpanded = 0.0
M2NumberOfNodesExpanded = 0.0
meanNumberOfMoves = 0.0
M2NumberOfMoves = 0.0
stdDevBranchesPruned = 0.0
stdDevNumberOfNodesExpanded = 0.0
stdDevNumberOfMoves = 0.0
minBranches = 0
maxBranches = 0
for p in range(100):
    # print(f"Starting game {p+1}")
    p1 = player.Player("X")

    # Player 2 currently picks random moves and so, while player 2 is not very good, it does allow you to
    # start testing your solution. Once you have something sensible, you should change player 2 to be more 
    # intelligent. Note that you can specify a seed for the random player (currently the seed is '42'),
    # which allows for testing in a consistent environment.
    # Note that the following two lines seed the random player differently each run

    seed = datetime.now().timestamp()
    p2 = randomPlayer.RandomPlayer("O", seed)
    # p2 = randomPlayer.RandomPlayer("O", 42)

    # actual connect 4 dimensions
    g = game.Game(p1, p2, 4, 4, 3)

    # g = game.Game(p1, p2, 6, 8, 4)

    # g = game.Game(p1, p2, 5, 6, 4)
    # g = game.Game(p1, p2, 5, 6, 3)
    # g = game.Game(p1, p2, 4, 5, 3)
    # g = game.Game(p1, p2, 4, 4, 4)
    # g = game.Game(p1, p2, 4, 4, 3)
    # g = game.Game(p1, p2, 3, 3, 2)		# for col in range(gameBoard.numColumns):
		# 	coordinatesToCheck = [gameBoard.colFills[col], col]
		# 	if col >= 0 and gameBoard.colFills[col-1] > gameBoard.colFills[col]:
		# 		for row in range(gameBoard.colFills[col], gameBoard.colFills[col-1]):
		# 			coordinatesToCheck.append(row, col)
		# 	elif col <= gameBoard.colFills[col-1] and gameBoard.colFills[col] > gameBoard.colFills[col+1]:
		# 		for row in range(gameBoard.colFills[col], gameBoard.colFills[col+1]):
		# 			coordinatesToCheck.append(row, col)

    # uncomment soon
    result = g.playGame(False)
    if result == 1:
        print(f"Game {p+1} result: Win")
        wins += 1
        winsAndDraws += 1
    elif result == -1:		# for col in range(gameBoard.numColumns):
		# 	coordinatesToCheck = [gameBoard.colFills[col], col]
		# 	if col >= 0 and gameBoard.colFills[col-1] > gameBoard.colFills[col]:
		# 		for row in range(gameBoard.colFills[col], gameBoard.colFills[col-1]):
		# 			coordinatesToCheck.append(row, col)
		# 	elif col <= gameBoard.colFills[col-1] and gameBoard.colFills[col] > gameBoard.colFills[col+1]:
		# 		for row in range(gameBoard.colFills[col], gameBoard.colFills[col+1]):
		# 			coordinatesToCheck.append(row, col)
        print(f"Game {p+1} result: Loss")
        losses += 1
    else:
        print(f"Game {p+1} result: Draw")
        winsAndDraws += 1

    meanBranchesPruned = (meanBranchesPruned * p + p1.numPruned) / (p + 1)
    meanNumberOfNodesExpanded = (meanNumberOfNodesExpanded * p + p1.numExpanded) / (p + 1)
    meanNumberOfMoves = (meanNumberOfMoves * p + g.numberOfMoves) / (p + 1)


    delta = p1.numPruned - meanBranchesPruned
    meanBranchesPruned += delta / (p + 1)
    delta2 = p1.numPruned - meanBranchesPruned
    M2BranchesPruned += delta * delta2
    stdDevBranchesPruned = (M2BranchesPruned / (p + 1)) ** 0.5

    delta = p1.numExpanded - meanNumberOfNodesExpanded
    meanNumberOfNodesExpanded += delta / (p + 1)
    delta2 = p1.numExpanded - meanNumberOfNodesExpanded    
    M2NumberOfNodesExpanded += delta * delta2
    stdDevNumberOfNodesExpanded = (M2NumberOfNodesExpanded / (p + 1)) ** 0.5

    delta = g.numberOfMoves - meanNumberOfMoves
    meanNumberOfMoves += delta / (p + 1)
    delta2 = g.numberOfMoves - meanNumberOfMoves    
    M2NumberOfMoves += delta * delta2   
    stdDevNumberOfMoves = (M2NumberOfMoves / (p + 1)) ** 0.5

    if minBranches > meanBranchesPruned:
        minBranches = meanBranchesPruned
    if maxBranches < meanBranchesPruned:
        maxBranches = meanBranchesPruned



print(f"Win rate: {wins / (p+1) * 100}%")
print(f"Win or Draw rate: {winsAndDraws / (p+1) * 100}%")
print(f"Total wins: {wins}")
print(f"Total losses: {losses}")
print(f"Mean branches pruned: {meanBranchesPruned}")
print(f"Standard deviation of branches pruned: {stdDevBranchesPruned}")
print(f"Min Branches Pruned: {minBranches}")
print(f"Max Branches Pruned: {maxBranches}")
print(f"Mean number of nodes expanded: {meanNumberOfNodesExpanded}")
print(f"Standard deviation of number of nodes expanded: {stdDevNumberOfNodesExpanded}")
print(f"Mean number of moves: {meanNumberOfMoves}")
print(f"Standard deviation of number of moves: {stdDevNumberOfMoves}")  



# range - max and min
        

