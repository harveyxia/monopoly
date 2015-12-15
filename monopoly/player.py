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

    def pay_rent(self, square):
        if square.owner != self:
            while self.balance < square.get_rent():
                # player must mortgage or sell something to raise balance
                self.do_strat_raise_money()
            self.balance -= square.get_rent()

    def pay_tax(self, square):
        tax = 0
        if square.position == 4:        # income tax
            # pay either 10% of balance or $200, whichever is smaller
            if self.balance*0.1 < 200:
                tax = self.balance*0.1
            else:
                tax = 200
        else:                           # luxury tax
            tax = 75
        while self.balance < tax:
            self.do_strat_raise_money()
        self.balance -= tax

    def go_to_jail(self):
        self.position = 10
        self.in_jail = True

    # strategy for unowned properties
    def do_strat_unowned_square(self, square):
        # raise NotImplementedError
        pass

    def do_strat_raise_money(self):
        # BANKRUPTCY HAPPENS HERE
        # raise NotImplementedError
        pass
