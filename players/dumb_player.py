from monopoly.player import Player


class DumbPlayer(Player):
    # buy all the houses/hotels as possible
    def do_strat_buy_from_bank(self, bldgs):
        if bldgs:
            self.explain("Building " + bldgs[0].name + " up -- as well as any other building -- as soon as possible")
            return bldgs[0]
        else:
            return None

    # sell properties to raise money, in no particular order
    def do_strat_raise_money(self, money):
        while self.properties and self.balance < money:
            p = self.properties.pop()
            self.explain("Selling " + p.name + "because we need the money and we don't really care which properties we own")
            if p.num_buildings == 0:
                p.owner = None
                self.balance += p.price
            elif p.num_buildings == 5:
                self.sell_hotel(p)
            else:
                self.sell_house(p)
        if self.balance < money:
            self.bankrupt = True
            return self.balance
        self.balance -= money
        return money

    # always buy unowned properties if landed
    def do_strat_unowned_square(self, square):
        if square.price < self.balance:
            self.explain("Buying " + square.name + " because we buy everything")
            return True

    # needs better logic
    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if d[0] == d[1]:  # roll doubles
            return True
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            if d[1] != d[0]:
                self.do_strat_raise_money(50)
            self.explain("Leaving jail after our third turn (mandatory)")
            return True
        else:
            self.explain("Staying in jail because we don't know any better")
            self.jail_duration += 1
            return False
