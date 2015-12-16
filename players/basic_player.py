from monopoly.player import Player


class BasicPlayer(Player):
    def do_strat_buy_buildings(self, board):
        pass

    def do_strat_raise_money(self):
        if self.properties:
            p = self.properties.pop()
            p.owner = None
            self.balance += p.price
            return True
        else:
            self.bankrupt = True
            return False

    def do_strat_unowned_square(self, square):
        if square.price < self.balance:
            print "purchasing square#####################################"
            self.purchase_square(square)
