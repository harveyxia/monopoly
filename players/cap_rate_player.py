from random import random

from monopoly.player import Player


class CapRatePlayer(Player):
    def __init__(self, name, caps):
        super(CapRatePlayer, self).__init__(name)
        self.caps = dict(caps)

    def do_strat_unowned_square(self, square):
        # print caps[square.name][0]
        if self.balance < square.price + self.largest_rent():
            return False
        if square.name in self.caps:
            # print self.caps[square.name][0] * self.balance / square.price
            return self.decide(self.prob(self.get_square_cap(square), self.balance))
        else:
            return False

    def do_strat_raise_money(self, money):
        # sort properties descending by buildings then cap rate
        self.properties = sorted(self.properties, key=lambda prop: (
        prop.num_buildings, self.caps[prop.name][self.check_square_status(prop)]), reverse=True)
        # print [self.caps[prop.name][self.check_square_status(prop)] for prop in self.properties]
        while self.properties and self.balance < money:
            p = self.properties.pop()
            p.owner = None
            self.balance += p.price
        if self.balance < money:
            self.bankrupt = True
            return self.balance
        self.balance -= money
        return money

    def do_strat_buy_from_bank(self, bldgs):
        bldgs = filter(lambda x: x.num_buildings < 5 and x.price <= self.balance, bldgs)
        if len(bldgs) == 0:
            return None
        caps = map(lambda x: self.caps[x.name][x.num_buildings + 1], bldgs)
        prices = map(lambda x: x.price, bldgs)
        probs = map(lambda x: self.prob(x, self.balance), caps)
        p = max(probs)
        if self.decide(p):
            return bldgs[probs.index(p)]
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
        elif self.others_have_monopoly or self.balance < self.largest_rent():
            # don't want to get out of jail if too risky
            self.jail_duration += 1
            return False
        else:
            # if no monopolies yet then gotta get in that property race
            self.do_strat_raise_money(50)
            return True

    @staticmethod
    def decide(p):
        return True if random() < p else False

    @staticmethod
    def prob(cap, balance):
        if balance < 100:
            return 0
        return cap * 5

    def get_square_cap(self, square):
        if self.caps[square.name][self.check_square_status(square)] == 0:
            return self.caps[square.name][0]
        else:
            return self.caps[square.name][self.check_square_status(square)]
