from random import random

from monopoly.player import Player


class CapRatePlayer(Player):
    def __init__(self, name, caps):
        super(CapRatePlayer, self).__init__(name)
        self.caps = dict(caps)

    def do_strat_unowned_square(self, square):
        # print caps[square.name][0]
        if self.balance < square.price:
            return False
        if square.name in self.caps:
            # print self.caps[square.name][0] * self.balance / square.price
            return self.decide(self.prob(self.caps[square.name][self.check_square_status(square)], self.balance))
        else:
            return False

    def do_strat_raise_money(self, money):
        # sort properties descending by cap rate
        self.properties = sorted(self.properties, key=lambda prop: self.caps[prop.name][self.check_square_status(prop)], reverse=True)
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
        caps = map(lambda x: self.caps[x.name][x.num_buildings + 1], squares)
        prices = map(lambda x: x.price, squares)
        probs = map(lambda x: self.prob(x, self.balance), caps)
        p = max(probs)
        if self.decide(p):
            return squares[probs.index(p)]
        else:
            return None

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            if d[1] != d[0]:
                self.do_strat_raise_money(50)
            return True
        else:
            self.do_strat_raise_money(50)
            return False

    @staticmethod
    def decide(p):
        return True if random() < p else False

    @staticmethod
    def prob(cap, balance):
        if balance < 100:
            return 0
        return cap * 5
