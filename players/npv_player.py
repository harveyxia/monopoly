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
                self.buy_square()

    def do_strat_raise_money(self):
        pass

    def do_strat_buy_buildings(self, board):
        pass

    @staticmethod
    def decide(p):
        return True if random() < p else False
