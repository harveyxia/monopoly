from monopoly.player import Player


class BasicPlayer(Player):
    def do_strat_buy_buildings(self, squares):
        pass

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

    def do_strat_unowned_square(self, square):
        if square.price < self.balance:
           return True


    # needs better logic
    def do_strat_get_out_of_jail(self, d):
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            return True
        else:
            self.jail_duration += 1
            return False
