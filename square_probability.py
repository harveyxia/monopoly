from monopoly.monopoly import Monopoly

"""
Using Monte Carlo simulation calculate the probability of landing on each square of the board.
"""

def run(turns, num_players):
    monopoly = Monopoly(num_players=num_players)
    squares = [0 for i in xrange(40)]
    for i in xrange(num_players*turns):
        player = monopoly.make_move()
        squares[player.position] += 1
    return squares
