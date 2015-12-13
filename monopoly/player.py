class Player(object):
    """
    Player object
    """
    def __init__(self, name):
        self.name = name
        self.balance = 1500     # cash balance
        self.net_value = 1500   # net value, including houses and properties
        self.in_jail = False
        self.jail_duration = 0
        self.position = 0
        self.properties = []
        self.bankrupt = False

    def move(self, num_squares):
        if self.in_jail:
            raise Exception("%s cannot move because in jail." % self.name)
        self.position = (self.position + num_squares) % 40

    def buy_square(self, square):
        if square.owner:
            raise Exception("%s cannot buy square because square owned by %s" % (self.name, square.owner.name))
        if self.balance < square.price:
            raise Exception("%s cannot buy square because insufficient balance" % self.name)
        self.balance -= square.price
        # increase net_value, by how much?
        self.properties.append(square)
        square.owner = self

    def _pay_rent(self, square):
        if square.owner != self:
            if self.balance < square.get_rent():
                pass
                # player must mortgage or sell something to raise balance
            else:
                self.balance -= square.get_rent()

    def go_to_jail(self):
        self.position = 10
        self.in_jail = True

    # override, insert player strategy in subclass
    def do_strat_square(self):
        # raise NotImplementedError
        pass

    def do_strat_raise_money(self):
        # raise NotImplementedError
        pass
