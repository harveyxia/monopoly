from monopoly.player import Player


class BasicPlayer(Player):
    def do_strat_buy_buildings(self):
        pass

    def do_strat_raise_money(self, money):
        while self.properties and self.balance < money:
            p = self.properties.pop()
            p.owner = None
            self.balance += p.price
        if self.balance < money:
            self.bankrupt = True
            return False
        return True

    def do_strat_unowned_square(self, square):
        if square.price < self.balance:
           return True


    # needs better logic
    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            return True
        else:
            self.jail_duration += 1
            return False
