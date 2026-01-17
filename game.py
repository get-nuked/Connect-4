import board

# The game class stores the board and players and plays the game
class Game:

    # Store the players and create a board with the given specification
    # IMPORTANT: Note that the coursework player is always player 1 (and so always goes first)
	def __init__(self, cwPlayer, player2, rows, columns, winNum):
		self.player1 = cwPlayer
		self.player2 = player2
		self.gameBoard = board.Board(rows, columns, winNum)
		self.listOfPlayers = (cwPlayer, player2)
		self.numberOfMoves = 0

    # Play the game itself, with or without alpha-beta pruning according to whether the pruning 
    # argument is true or false respectively.
	def playGame(self, pruning):
		# Keep track of whether the game is won or the board is full
		won = False
		full = False
		# index is used to keep track of which player's move it is
		index = 0
		# play the game until a player wins or it is a draw (i.e., the board is full)
		while not won and not full:
			# Get the current player, and update the index
			currPlayer = self.listOfPlayers[index]
			print("Moving with player " + str(currPlayer.name))

			if index == 0 and pruning:
				move = currPlayer.getMoveAlphaBeta(self.gameBoard.copy())
			else:
				move = currPlayer.getMove(self.gameBoard.copy())
				
			moveDone = self.gameBoard.addPiece(move, currPlayer.name)
			if moveDone == True:
				won = self.gameBoard.checkWin()
				full = self.gameBoard.checkFull()
				# Uncomment the following line to print each move
				# self.gameBoard.printBoard()
			else:
				print("Player made illegal move. Turn lost.")

			index = (index + 1) % 2
			self.numberOfMoves += 1

		if won and currPlayer == self.player1:
			print("You Win!")
			print("Nodes expanded:", self.player1.numExpanded)
			print("Branches pruned:", self.player1.numPruned)
			self.gameBoard.printBoard()
			return 1

		if won and currPlayer == self.player2:
			print("You Lose!")
			print("Nodes expanded:", self.player1.numExpanded)
			print("Branches pruned:", self.player1.numPruned)
			self.gameBoard.printBoard()
			return -1

		if full and not won:
			print("It's a Draw!")
			print("Nodes expanded:", self.player1.numExpanded)
			print("Branches pruned:", self.player1.numPruned)
			self.gameBoard.printBoard()
			return 0




