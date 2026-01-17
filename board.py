import copy

# The Space class is a simple wrapper around a string representing the content of a space.
# If a space is unused it has the value ' ', otherwise it has the name of the player whose piece occupies that space. 
# To fill a space, simply set its value to the name of the player whose piece occupies the space. 
class Space:

	def __init__(self):
		self.value = " "

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return str(self)


# This class represents the Connect board, and tracks various useful pieces of information and provides utility 
# methods, e.g., for checking whether the board is full or the last move is a winning moves. 
class Board:

	# When defining the board, you should provide the number of rows and columns, and the number of
	# pieces in a line required to win (winNum). 
	def __init__(self, rows, columns, winNum):
		# The game board is represented as a list of lists of Space objects.
		self.gameBoard = list()

		# We store the number of rows, columns, and pieces in a line needed to win,
		# and initialise the board to contain empty Space objects
		self.numRows = rows
		self.numColumns = columns
		self.winNum = winNum
		for i in range(self.numRows):
			currRow = list()
			for i in range(self.numColumns):
				currRow.append(Space())
			self.gameBoard.append(currRow)

		# We use colFills to track the lowest numbered row that is empty for each column.
		# When a piece is placed in a column, the corresponding number in this list will be incremented.
		self.colFills = list()
		for i in range(self.numColumns):
			self.colFills.append(0)

		# We store the location of the last piece added to the game, and the player who made the move. 
		# The first element is the row, the second is the column and the last element is the name of the player.
		self.lastPlay = [-1,-1, ""]


	# This method adds a piece for the specified player to the specified column
	def addPiece(self, column, player):
		if column >= self.numColumns or column < 0:
			print("Column does not exist")
			return False

		if self.colFills[column] >= self.numRows:
			print("Column is full, pick another column")
			return False

		# get the row to fill from the fill tracker
		row = self.colFills[column]
		# assign the space to the player and record the last move
		self.gameBoard[row][column].value = player
		self.lastPlay = [row, column, player]
		# increment the fill tracker to account for this move
		self.colFills[column] = self.colFills[column] + 1
		return True


	# This method removes a piece from the specified column
	# Note this can be used in your search, and not as a move in the game.
	def removePiece(self, column):
		if column >= self.numColumns or column < 0:
			print("Column does not exist")
			return False

		if self.colFills[column] == 0:
			print("Column is empty, pick another column")
			return False

		# get the row containing the highest piece
		row = self.colFills[column] - 1
		# set the space to empty
		self.gameBoard[row][column].value = ' '
		self.lastPlay = [row, column, ' ']
		# decrement the fill tracker to account for this move
		self.colFills[column] = self.colFills[column] - 1
		return True


	# This method returns True if the last play resulted in a win for that player, and returns False.
	# Note that this only checks whether the last move was a winning move, and not whether there is already
	# a winning number of pieces in a line.
	def checkWin(self):
		if self.lastPlay[2] == ' ':
			return False

		# get the details of the last move
		lastRow = self.lastPlay[0]
		lastColumn = self.lastPlay[1]
		lastPlayer = self.lastPlay[2]

		# Check whether there is a winning number of pieces in a column. 
		# Track how many pieces in a line have been found so far (initially 1 from the last move)
		rowCounter = 1
		foundRow = 1
		# Record whether should check upwards and downwards in the current column
		uCount = True
		dCount = True
		# Check upwards and downwards to see if there is a winning number of pieces in a line
		while foundRow < self.winNum:

			if not uCount and not dCount:
				break

			if lastRow - rowCounter < 0:
				dCount = False

			if lastRow + rowCounter >= self.numRows:
				uCount = False

			change = False
			if dCount:
				if self.gameBoard[lastRow - rowCounter][lastColumn].value == lastPlayer:
					change = True
					foundRow = foundRow + 1
				else:
					dCount = False

			if uCount:
				if self.gameBoard[lastRow + rowCounter][lastColumn].value == lastPlayer:
					change = True
					foundRow = foundRow + 1
				else:
					uCount = False

			if change:
				rowCounter = rowCounter + 1

		if foundRow >= self.winNum:
			return True

		# Check whether there is a winning number of pieces in a row. 
		# Track how many pieces in a line have been found so far (initially 1 from the last move)
		colCounter = 1
		foundCol = 1
		# Record whether should check forwards and backwards in the current column
		bCount = True
		fCount = True

		# Check forwards and backwards to see if there is a winning number of pieces in a line
		while foundCol < self.winNum:

			if not bCount and not fCount:
				break

			if lastColumn - colCounter < 0:
				bCount = False

			if lastColumn + colCounter >= self.numColumns:
				fCount = False

			change = False
			if bCount:
				if self.gameBoard[lastRow][lastColumn - colCounter].value == lastPlayer:
					change = True
					foundCol = foundCol + 1
				else:
					bCount = False

			if fCount:
				if self.gameBoard[lastRow][lastColumn + colCounter].value == lastPlayer:
					change = True
					foundCol = foundCol + 1
				else:
					fCount = False

			if change:
				colCounter = colCounter + 1	

		if foundCol >= self.winNum:
			return True

		# Check whether there is a winning number of pieces in a upper left to lower right diagonal. 
		# Track how many pieces in a line have been found so far (initially 1 from the last move)
		diagCounter = 1
		foundDiag = 1
		# Record whether should check upwards left and downwards right from the last move
		ulCount = True
		drCount = True

		# Check each diagonal to see if there is a winning number of pieces in a line
		while foundDiag < self.winNum:
			if not ulCount and not drCount:
				# return False
				break

			if lastRow + diagCounter >= self.numRows or lastColumn - diagCounter < 0:
				ulCount = False

			if lastRow - diagCounter < 0 or lastColumn + diagCounter >= self.numColumns:
				drCount = False

			change = False

			if ulCount:
				if self.gameBoard[lastRow + diagCounter][lastColumn - diagCounter].value == lastPlayer:
					change = True
					foundDiag = foundDiag + 1
				else:
					ulCount = False

			if drCount:
				if self.gameBoard[lastRow - diagCounter][lastColumn + diagCounter].value == lastPlayer:
					change = True
					foundDiag = foundDiag + 1
				else:
					drCount = False

			if change:
				diagCounter = diagCounter + 1

		if foundDiag >= self.winNum:
			return True

		# Check whether there is a winning number of pieces in a upper right to lower left diagonal. 
		# Track how many pieces in a line have been found so far (initially 1 from the last move)
		diagCounter = 1
		foundDiag = 1
		# Record whether should check upwards right and downwards left from the last move
		urCount = True
		dlCount = True
		# Check each diagonal to see if there is a winning number of pieces in a line
		while foundDiag < self.winNum:
			if not urCount and not dlCount:
				return False

			if lastRow + diagCounter >= self.numRows or lastColumn + diagCounter >= self.numColumns:
				urCount = False

			if lastRow - diagCounter < 0 or lastColumn - diagCounter < 0:
				dlCount = False

			change = False

			if urCount:
				if self.gameBoard[lastRow + diagCounter][lastColumn + diagCounter].value == lastPlayer:
					change = True
					foundDiag = foundDiag + 1
				else:
					urCount = False

			if dlCount:
				if self.gameBoard[lastRow - diagCounter][lastColumn - diagCounter].value == lastPlayer:
					change = True
					foundDiag = foundDiag + 1
				else:
					dlCount = False

			if change:
				diagCounter = diagCounter + 1

		if foundDiag >= self.winNum:
			return True

		return False
	

	# Check whether the board is full, i.e., if it is possible to make a move 
	def checkFull(self):
		for i in range(self.numColumns):
			if self.colFills[i] < self.numRows:
				return False
		return True


	# Check what is in the specified location (i.e., return the player name or ' ')
	def checkSpace(self, row, column):
		return self.gameBoard[row][column]


	# Print a simple visualisation of the current board (where 0,0 is bottom left)
	def printBoard(self):
		for row in reversed(self.gameBoard):
			print("| ", end='')
			for col in row:
				print(col, " ", end='')
			print("|")
		for i in range(self.numColumns):
			print("--" + str(i + 1), end='')
		print("---")


	# Copy the current board
	def copy(self):
		b = Board(self.numRows, self.numColumns, self.winNum)
		b.gameBoard = copy.deepcopy(self.gameBoard)
		b.lastPlay = copy.deepcopy(self.lastPlay)
		b.colFills = copy.deepcopy(self.colFills)
		return b
