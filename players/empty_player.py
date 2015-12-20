# this guy just avoids everything so we can calculate the
# bare probabilities of landing on squares and such

from monopoly.player import Player


class EmptyPlayer(Player):

    def do_strat_unowned_square(self, square):
        pass

    def do_strat_raise_money(self, money):
        pass

    def do_strat_buy_buildings(self, squares):
        pass

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        pass