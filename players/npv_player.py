from random import random

from decision_function import generate_square_buy_decisions
from monopoly.player import Player


class NpvPlayer(Player):
    def __init__(self, name, npvs):
        super(NpvPlayer, self).__init__(name)
        self.npvs = dict(npvs)

    def do_strat_unowned_square(self, square):
        # print npvs[square.name][0]
        if self.balance < square.price:
            return False
        if square.name in self.npvs:
            # print self.npvs[square.name][0] * self.balance / square.price
            return self.decide(self.prob(self.npvs[square.name][0], self.balance, square.price))
        else:
            return False

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
        squares = filter(lambda x: x.num_buildings < 5 and x.price <= self.balance, squares)
        if len(squares) == 0:
            return None
        npvs = map(lambda x: self.npvs[x.name][x.num_buildings + 1], squares)
        prices = map(lambda x: x.price, squares)
        probs = map(lambda x, y: self.prob(x, self.balance, y), npvs, prices)
        p = max(probs)
        if decide(p):
            return squares[probs.index(r)]
        else:
            return None

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            return True
        else:
            self.jail_duration += 1
            return False

    @staticmethod
    def decide(p):
        return True if random() < p else False

    @staticmethod
    def prob(npv, balance, price):
        return npv * balance / price
