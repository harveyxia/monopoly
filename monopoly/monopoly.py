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
        self.player_turn = 0    # which Player has next move, default first player

        self.is_over = False    # true if game is over
        self.winner = None

    # game consists of N moves until all but one player is bankrupt
    def make_move(self):
        player = self.players[self.player_turn]
        dice = self.roll_dice()
        player.do_strategy()
        if dice[0] == dice[1]:              # doubles, roll again
            dice = self.roll_dice()
            player.do_strategy()
            if dice[0] == dice[1]:          # third double, go to jail
                player.go_to_jail()

    def roll_dice(self):
        return randint(1, 6), randint(1, 6)

    def do_square_action(self):
        # if pass GO, get $200
        # if go to jail, go to fail
        # if land on owned property, pay rent
        # if land on tax, pay tax
        # if land on chance or community, pick card and do card
        pass

    def run(self):
        while not self.is_over:
            pass
