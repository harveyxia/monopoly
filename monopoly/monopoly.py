from board import Board
from player import Player
from random import randint


class Monopoly(object):
    """
    Monopoly class, represents entirety of game
    """

    def __init__(self, num_players=4):
        self.board = Board()
        self.players = [Player("player" + str(i)) for i in xrange(num_players)]
        self.player_turn = 0    # which Player has next move, default first player

        self.is_over = False    # true if game is over
        self.winner = None

    # game consists of N moves until all but one player is bankrupt
    def make_move(self):
        player = self.players[self.player_turn]
        if player.in_jail:
            self.attempt_get_out_of_jail(player)
        else:
            self.roll_and_move(player)
        return player                           # return the player that just moved

    def attempt_get_out_of_jail(self, player):
        # if in jail for 3 turns, get out automatically and roll to move
        if player.jail_duration >= 2:
            player.in_jail = False
            player.jail_duration = 0
            self.roll_and_move(player)
            print "served time"
        else:
            # if roll doubles, get out of jail but don't move forward
            d = self.roll_dice()
            if d[0] == d[1]:
                print "escape jail"
                player.in_jail = False
                player.jail_duration = 0
            else:
                player.jail_duration += 1

    def roll_and_move(self, player):
        dice = self.roll_dice()
        player.move(dice[0]+dice[1])
        player.do_strat_square()
        if dice[0] == dice[1]:              # doubles, roll again
            dice = self.roll_dice()
            player.move(dice[0]+dice[1])
            player.do_strat_square()
            if dice[0] == dice[1]:          # third double, go to jail
                print "go to jail"
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
