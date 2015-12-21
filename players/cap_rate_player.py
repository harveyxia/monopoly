from random import random

from monopoly.player import Player


class CapRatePlayer(Player):
    def __init__(self, name, caps):
        super(CapRatePlayer, self).__init__(name)
        self.caps = dict(caps)

    def do_strat_unowned_square(self, square):
        # print caps[square.name][0]
        if self.balance < square.price + self.largest_rent():
            self.explain("Rejecting " + square.name + " because we don't have enough money")
            return False
        if square.name in self.caps:
            # print self.caps[square.name][0] * self.balance / square.price
            decision = self.decide(self.prob(self.get_square_cap(square), self.balance))
            if decision:
                self.explain("Buying " + square.name + " based on its cap rate") 
            else:
                self.explain("Rejecting " + square.name + " based on its cap rate")
            return decision
        else:
            return False

    def do_strat_raise_money(self, money):
        # sort properties descending by buildings then cap rate
        # print [self.caps[prop.name][self.check_square_status(prop)] for prop in self.properties]
        while self.balance < money:
            if not self.properties:
                break
            self.sort_properties()
            prop = self.properties[len(self.properties)-1]
            if prop.num_buildings == 0:
                prop.owner = None
                self.balance += prop.price
                self.properties.pop()
                self.explain("Selling " + prop.name + " because we need the money and this has the lowest cap rate")
            elif prop.num_buildings == 5:
                self.sell_hotel(prop)
                self.explain("Selling a hotel on " + prop.name + " because we need the money and this has the lowest cap rate")
            else:
                self.sell_house(prop)
                self.explain("Selling a house on " + prop.name + " because we need the money and this has the lowest cap rate")
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
            decision = bldgs[probs.index(p)]
            self.explain("Building " + decision.name + " based on its cap rate")
            return decision
        else:
            self.explain("Intentionally deciding not to build this turn to reduce risk")
            return None

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            if d[1] != d[0]:
                self.do_strat_raise_money(50)
            self.explain("Leaving jail after our third turn (mandatory)")
            return True
        elif self.others_have_monopoly or self.balance < self.largest_rent():
            # don't want to get out of jail if too risky
            self.jail_duration += 1
            self.explain("Staying in jail because it's too risky to leave right now")
            return False
        else:
            # if no monopolies yet then gotta get in that property race
            self.do_strat_raise_money(50)
            self.explain("Leaving jail ASAP because it's too early to waste time in jail")
            return True

    @staticmethod
    def decide(p):
        return True if random() < p else False

    @staticmethod
    def prob(cap, balance):
        if balance < 100:
            return 0
        return cap * 20

    def get_square_cap(self, square):
        if self.caps[square.name][self.check_square_status(square)] == 0:
            return self.caps[square.name][0]
        else:
            return self.caps[square.name][self.check_square_status(square)]

    def sort_properties(self):
        self.properties = sorted(self.properties, key=lambda prop: (prop.num_buildings, self.get_square_cap(prop)), reverse=True)
