import board
import random

class humanPlayer:
    def __init__(self, name):
        self.name = name

    def getMove(self, gameBoard):
        choice = int(input("Enter the column number (1 to " + str(gameBoard.numColumns) + "): "))
        choice -= 1
        return choice
