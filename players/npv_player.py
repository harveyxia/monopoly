from random import random

from decision_function import generate_square_buy_decisions
from monopoly.player import Player


class NpvPlayer(Player):
    def __init__(self, name):
        super(NpvPlayer, self).__init__(name)
        self.square_buy_decisions = generate_square_buy_decisions("roi.csv")

    def do_strat_unowned_square(self, square):
        if square.price < self.balance:
            if self.decide(self.square_buy_decisions[square.name]):
                return True

    def do_strat_raise_money(self, money):
        pass

    def do_strat_buy_buildings(self, squares):
        pass

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        pass

    @staticmethod
    def decide(p):
        return True if random() < p else False
