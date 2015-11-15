from board import Board
from player import Player

class Monopoly(object):
    """
    Monopoly class, represents entirety of game
    """
    def __init__(self, num_players=4):
        self.board = Board()
        self.players = [Player("player" + i) for i in xrange(num_players)]
