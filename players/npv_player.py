from random import random

from decision_function import generate_square_buy_decisions
from monopoly.player import Player


class NpvPlayer(Player):
    def __init__(self, name):
        super(NpvPlayer, self).__init__(name)
        if self.npvs is None:
            raise Exception("cannot create NPV player %s without npv file." % self.name)

    def do_strat_unowned_square(self, square):
        # print npvs[square.name][0]
        print npvs[square.name][0] * self.money / square.cost
        return decide(npvs[square.name][0] * self.money / square.cost)

    def do_strat_raise_money(self, money):
        while self.properties and self.balance < money:
            p = self.properties.pop()
            p.owner = None
            self.balance += p.price
        if self.balance < money:
            self.bankrupt = True
            return self.balance
        self.balance -= money
        return money

    def do_strat_buy_buildings(self, squares):
        pass

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        return False

    @staticmethod
    def decide(p):
        return True if random() < p else False
