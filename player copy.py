import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	maxDepth = 5

	def __init__(self, name):
		self.name = name
		self.numExpanded = 0  # Use this to track the number of nodes you expand
		self.numPruned = 0    # Use this to track the number of times you prune

	def hasImmediateWin(self, gameBoard, player):
		for col in range(gameBoard.numColumns):
			if gameBoard.colFills[col] < gameBoard.numRows:
				gameBoard.addPiece(col, player)
				if gameBoard.checkWin(): # if the move leeds to a win
					gameBoard.removePiece(col)
					return True
				gameBoard.removePiece(col)
		return False


	def getMove(self, gameBoard):  # minimax
		bestValue = -math.inf
		bestMove = -1

		for col in range(gameBoard.numColumns):
			if gameBoard.colFills[col] < gameBoard.numRows:
				# check if this move is a immediate win
				gameBoard.addPiece(col, "X")
				if gameBoard.checkWin():  # X wins immediately
					gameBoard.removePiece(col)
					return col  # pick it immediately
				gameBoard.removePiece(col)
	
				self.numExpanded += 1
				gameBoard.addPiece(col, "X")
				moveValue = self.minimax(1, gameBoard, False)
				gameBoard.removePiece(col)
				if moveValue > bestValue:
					bestValue = moveValue
					bestMove = col

		if bestMove == -1:
			for col in range(gameBoard.numColumns):
				if gameBoard.colFills[col] < gameBoard.numRows:
					return col

		return bestMove


	def minimax(self, depth, gameBoard, isMaximizing):
		if gameBoard.checkWin():
			if isMaximizing:  # O just played and won
				return -math.inf
			else:
				return math.inf

		if depth == self.maxDepth or gameBoard.checkFull():
			# current player depends on whose turn it is
			currentPlayer = "X" if isMaximizing else "O"
			opponent = "O" if isMaximizing else "X"

			if self.hasImmediateWin(gameBoard, currentPlayer):
				return math.inf if isMaximizing else -math.inf
			if self.hasImmediateWin(gameBoard, opponent):
				return -math.inf if isMaximizing else math.inf
			# if there isnt a move that leeds to a win
			return self.evaluationFunction(gameBoard)

		if isMaximizing:
			best = -math.inf
			for col in range(gameBoard.numColumns):
				if gameBoard.colFills[col] < gameBoard.numRows:
					self.numExpanded += 1
					gameBoard.addPiece(col, "X")
					value = self.minimax(depth + 1, gameBoard, False)
					gameBoard.removePiece(col)
					best = max(best, value)
			return best
		else:
			best = math.inf
			for col in range(gameBoard.numColumns):
				if gameBoard.colFills[col] < gameBoard.numRows:
					self.numExpanded += 1
					gameBoard.addPiece(col, "O")
					value = self.minimax(depth + 1, gameBoard, True)
					gameBoard.removePiece(col)
					best = min(best, value)
			return best


	def getMoveAlphaBeta(self, gameBoard):  # minimax with alpha-beta pruning
		bestValue = -math.inf
		bestMove = -1
			
		center = gameBoard.numColumns // 2
		order = sorted(range(gameBoard.numColumns), key=lambda c: abs(c - center))
		for col in order:
			if gameBoard.colFills[col] < gameBoard.numRows:
				# check if this move is a immediate win
				gameBoard.addPiece(col, "X")
				if gameBoard.checkWin():  # X wins immediately
					gameBoard.removePiece(col)
					return col  # pick it immediately
				gameBoard.removePiece(col)

				self.numExpanded += 1
				gameBoard.addPiece(col, "X")
				moveValue = self.minimaxAlphaBeta(1, gameBoard, False, -math.inf, math.inf, order)
				gameBoard.removePiece(col)
				if moveValue > bestValue:
					bestValue = moveValue
					bestMove = col

		if bestMove == -1:
			for col in range(gameBoard.numColumns):
				if gameBoard.colFills[col] < gameBoard.numRows:
					return col

		return bestMove


	def minimaxAlphaBeta(self, depth, gameBoard, isMaximizing, alpha, beta, order):
		if gameBoard.checkWin():
			if isMaximizing:  # O just played and won
				return -math.inf
			else:
				return math.inf

		if depth == self.maxDepth or gameBoard.checkFull():
			# current player depends on whose turn it is
			currentPlayer = "X" if isMaximizing else "O"
			opponent = "O" if isMaximizing else "X"

			if self.hasImmediateWin(gameBoard, currentPlayer):
				return math.inf if isMaximizing else -math.inf
			if self.hasImmediateWin(gameBoard, opponent):
				return -math.inf if isMaximizing else math.inf
			return self.evaluationFunction(gameBoard)

		if isMaximizing:
			best = -math.inf
			for col in order:
				if gameBoard.colFills[col] < gameBoard.numRows:
					self.numExpanded += 1
					gameBoard.addPiece(col, "X")
					value = self.minimaxAlphaBeta(depth + 1, gameBoard, False, alpha, beta, order)
					gameBoard.removePiece(col)

					best = max(best, value)
					alpha = max(alpha, best)
					if beta <= alpha:
						self.numPruned += 1
						return best
			return best
		else:
			best = math.inf
			for col in order:
				if gameBoard.colFills[col] < gameBoard.numRows:
					self.numExpanded += 1
					gameBoard.addPiece(col, "O")
					value = self.minimaxAlphaBeta(depth + 1, gameBoard, True, alpha, beta, order)
					gameBoard.removePiece(col)

					best = min(best, value)
					beta = min(beta, best)
					if beta <= alpha:
						self.numPruned += 1
						return best
			return best
			

	# def hasAtleastOnePlayableSpace(self, gameBoard, coordinates):  # checks a list of coordinates if atleast one is an empty non floating space
	# 	for coord in coordinates:
	# 		if not (0 <= coord[0] < gameBoard.numRows and 0 <= coord[1] < gameBoard.numColumns):
	# 			continue

	# 		if coord[0] == 0 and gameBoard.checkSpace(coord[0], coord[1]).value == " ": # if bottom row and empty
	# 			return True 
	# 		elif gameBoard.checkSpace(coord[0], coord[1]).value == " " and (coord[0] == 0 or gameBoard.checkSpace(coord[0] - 1, coord[1]).value != " "): # if space is empty and not floating
	# 			return True 
	# 	return False

	def hasAtleastOnePlayableSpace(self, gameBoard, coordinates):
		for row, col in coordinates:
			if not (0 <= row < gameBoard.numRows and 0 <= col < gameBoard.numColumns):
				continue
			# If the next empty row in this column is within our coordinates
			if gameBoard.colFills[col] - 1 == row or (row == 0 and gameBoard.colFills[col] > 0):
				return True
		return False


	# def numberOfFloatingSpaces(self, gameBoard, coordinates):  # counts the number of empty floating spaces in a list of coordinates
	# 	count = 0
	# 	for coord in coordinates:
	# 		if not (0 <= coord[0] < gameBoard.numRows and 0 <= coord[1] < gameBoard.numColumns):
	# 			continue
	# 		if gameBoard.checkSpace(coord[0], coord[1]).value == " " and coord[0] > 0 and gameBoard.checkSpace(coord[0] - 1, coord[1]).value == " ":
	# 			count += 1
	# 	return count
	
	def numberOfFloatingSpaces(self, gameBoard, coordinates):
		count = 0
		for row, col in coordinates:
			if not (0 <= row < gameBoard.numRows and 0 <= col < gameBoard.numColumns):
				continue
			# if the row is above the next empty row, it is floating
			if row < gameBoard.colFills[col] - 1:
				count += 1
		return count



	def evaluationFunction(self, gameBoard):
		minimaxValue = 0
		# checks combinations of length winNum for each direction (horizontal, vertical, diagonal \, diagonal /) for the number X and O pieces

		# checks the horizontal combinations
		for col in range(gameBoard.numColumns - gameBoard.winNum + 1):
			max_row = max(gameBoard.colFills[column] - 1 for column in range(col, min(col + gameBoard.winNum, gameBoard.numColumns)))
			for row in range(max_row + 1):  # row 0 up to highest filled row
				# checks the number of X and O pieces in each combination of length winNum
				window = [gameBoard.checkSpace(row, col + i).value for i in range(gameBoard.winNum)]
				x_count = window.count("X")
				o_count = window.count("O")
	
				if window.count(' ') == gameBoard.winNum:
					continue  # skip empty windows

				openEnds = 0 # counts the number of open ends for the combination
				if (x_count >= gameBoard.winNum-2) ^ (o_count >= gameBoard.winNum-2):
					if window[0]:
						openEnds += 1
					if window[-1]:
						openEnds += 1

				# ensures that the combination is not floating
				if self.hasAtleastOnePlayableSpace(gameBoard, [(row, col + i) for i in range(gameBoard.winNum)]):
					# for each set, checks that only one player's pieces are present and updates minimaxValue accordingly
					if (x_count > 0) ^ (o_count > 0):
						if x_count == gameBoard.winNum:  # x wins
							return math.inf
						elif o_count == gameBoard.winNum:  # O wins
							return -math.inf
						elif x_count > 0:
							weight = (10 ** x_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row, col + i) for i in range(gameBoard.winNum)])  # adds square of number of X pieces to value
						else:
							weight = -1.5 * (10 ** o_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row, col + i) for i in range(gameBoard.winNum)])  # subtracts square of number of O pieces from value

						if openEnds == 2: # higher weight for two open ends as it is more advantageous
							weight *= 2
						elif openEnds == 1:
							weight *= 1.25

						minimaxValue += weight


		# checks the vertical combinations
		for col in range(gameBoard.numColumns):
			# only need to check from bottom row up to the highest possible starting row for a win
			for row in range(max(0, min(gameBoard.colFills[col] - 1, gameBoard.numRows - gameBoard.winNum + 1))):
				# checks the number of X and O pieces in each combination of length winNum
				window = [gameBoard.checkSpace(row + i, col).value for i in range(gameBoard.winNum)]
				x_count = window.count("X")
				o_count = window.count("O")

				if window.count(' ') == gameBoard.winNum:
					continue  # skip empty windows
			
				openEnds = 0 # counts the number of open ends for the combination
				if (x_count >= gameBoard.winNum-2) ^ (o_count >= gameBoard.winNum-2):
					if window[0] == " ":
						openEnds += 1
					if window[-1] == " ":
						openEnds += 1

				# ensures that the combination is not floating
				if self.hasAtleastOnePlayableSpace(gameBoard, [(row + i, col) for i in range(gameBoard.winNum)]):
					# for each set, checks that only one player's pieces are present
					if (x_count > 0) ^ (o_count > 0):
						if x_count == gameBoard.winNum:
							return math.inf
						elif o_count == gameBoard.winNum:
							return -math.inf
						elif x_count > 0:
							weight = (10 ** x_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row + i, col) for i in range(gameBoard.winNum)])
						else:
							weight = -1.5 * (10 ** o_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row + i, col) for i in range(gameBoard.winNum)])

						if openEnds == 2:
							weight *= 2
						elif openEnds == 1:
							weight *= 1.25

						minimaxValue += weight


		# checks the diagonal / combinations
		for col in range(gameBoard.numColumns - gameBoard.winNum + 1):
			for row in range(gameBoard.numRows - gameBoard.winNum + 1):
				# Skip diagonals completely above empty columns or floating cells
				window = [gameBoard.checkSpace(row+i, col+i).value for i in range(gameBoard.winNum)]
				x_count = window.count("X")
				o_count = window.count("O")

				if window.count(' ') == gameBoard.winNum:
					continue

				openEnds = 0 # counts the number of open ends for the combination
				if (x_count >= gameBoard.winNum-2) ^ (o_count >= gameBoard.winNum-2):
					if window[0] == " ":
						openEnds += 1
					if window[-1] == " ":
						openEnds += 1

				# ensures that the combination is not floating
				if self.hasAtleastOnePlayableSpace(gameBoard, [(row + i, col + i) for i in range(gameBoard.winNum)]):
					# for each set, checks that only one player's pieces are present
					if (x_count > 0) ^ (o_count > 0):
						if x_count == gameBoard.winNum:
							return math.inf
						elif o_count == gameBoard.winNum:
							return -math.inf
						elif x_count > 0:
							weight = (10 ** x_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row + i, col + i) for i in range(gameBoard.winNum)])
						else:
							weight = -1.5 * (10 ** o_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row + i, col + i) for i in range(gameBoard.winNum)])

						if openEnds == 2:
							weight *= 2
						elif openEnds == 1:
							weight *= 1.25

						minimaxValue += weight


		# checks the diagonal \ combinations
		for col in range(gameBoard.winNum - 1, gameBoard.numColumns):
			for row in range(gameBoard.numRows - gameBoard.winNum + 1):
				# Skip diagonals completely above empty columns or floating cells
				window = [gameBoard.checkSpace(row+i, col-i).value for i in range(gameBoard.winNum)]
				if window.count(' ') == gameBoard.winNum:
					continue

				# checks the number of X and O pieces in each combination of length winNum
				x_count = window.count("X")
				o_count = window.count("O")
				
				openEnds = 0 # counts the number of open ends for the combination
				if (x_count >= gameBoard.winNum-2) ^ (o_count >= gameBoard.winNum-2):
					if window[0] == " ":
						openEnds += 1
					if window[-1] == " ":
						openEnds += 1

				# ensures that the combination is not floating
				if self.hasAtleastOnePlayableSpace(gameBoard, [(row + i, col - i) for i in range(gameBoard.winNum)]):
					# for each set, checks that only one player's pieces are present
					if (x_count > 0) ^ (o_count > 0):
						if x_count == gameBoard.winNum:
							return math.inf
						elif o_count == gameBoard.winNum:
							return -math.inf
						elif x_count > 0:
							weight = (10 ** x_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row + i, col - i) for i in range(gameBoard.winNum)])
						else:
							weight = -1.5 * (10 ** o_count) * 0.5 ** self.numberOfFloatingSpaces(gameBoard, [(row + i, col - i) for i in range(gameBoard.winNum)])

						if openEnds == 2:
							weight *= 2
						elif openEnds == 1:
							weight *= 1.25

						minimaxValue += weight


		# additional heuristic: center column control
		center = gameBoard.numColumns // 2
		for col in range(gameBoard.numColumns):
			for row in range(gameBoard.colFills[col] - 1):
				if gameBoard.checkSpace(row, col).value == "X":
					minimaxValue += (center - abs(center - col)) * 2
				elif gameBoard.checkSpace(row, col).value == "O":
					minimaxValue -= (center - abs(center - col)) * 2


		return minimaxValue
	


		

	