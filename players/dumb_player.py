from monopoly.player import Player


class DumbPlayer(Player):

    # buy all the houses/hotels as possible
    def do_strat_buy_buildings(self, squares):
        if squares:
            return squares[0]
        else:
            return None

    # sell properties to raise money, in no particular order
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

    # always buy unowned properties if landed
    def do_strat_unowned_square(self, square):
        if square.price < self.balance:
            return True


    # needs better logic
    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if d[0] == d[1]:                        # roll doubles
            return True
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            self.do_strat_raise_money(50)
            return True
        else:
            self.jail_duration += 1
            return False
