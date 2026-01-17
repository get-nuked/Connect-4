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
    # g = game.Game(p1, p2, 6, 7, 4)

    # g = game.Game(p1, p2, 5, 6, 4)
    # g = game.Game(p1, p2, 5, 6, 3)
    # g = game.Game(p1, p2, 4, 5, 3)
    # g = game.Game(p1, p2, 4, 4, 4)
    # g = game.Game(p1, p2, 4, 4, 3)
    # g = game.Game(p1, p2, 3, 3, 2)

    g = game.Game(p1, p2, 4, 4, 3)

    result = g.playGame(False)
    