from board import Board
from player import Player
from random import randint


class Monopoly(object):
    """
    Monopoly class, represents entirety of game
    """

    def __init__(self, num_players=4):
        self.board = Board()
        self.players = [Player("player" + i) for i in xrange(num_players)]
        self.player_turn = 0  # which Player has next move, default first player

    def make_move(self):
        player = self.players[self.player_turn]
        # roll dice, if doubles go again
        dice = self.roll_dice()
        # do square action
        if dice[0] == dice[1]:
            dice = self.roll_dice()
            # do square action
            if dice[0] == dice[1]:
                player.go_to_jail()

    def roll_dice(self):
        return randint(1, 6), randint(1, 6)

    def do_square_action(self):
        pass
