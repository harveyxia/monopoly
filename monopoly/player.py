class Player(object):
    """
    Player object
    """

    def __init__(self, name):
        self.name = name
        self.balance = 1500  # cash balance
        # self.net_value = 1500   # net value, including houses and properties
        self.in_jail = False
        self.jail_duration = 0
        self.position = 0
        self.owned_colors = []
        self.properties = []
        self.bankrupt = False
        self.board = None
        self.years = 0

    def __str__(self):
        return "%s:\n  " \
               "position:%s\n  " \
               "balance:%s\n  " \
               "properties:%s\n  " \
               "in_jail:%s" % \
               (self.name, self.position, self.balance, self.properties, self.in_jail)

    def move(self, num_squares):
        if self.in_jail:
            raise Exception("%s cannot move because in jail." % self.name)
        if (self.position + num_squares > 40):
            self.years = self.years + 1
        self.position = (self.position + num_squares) % 40

    def buy_square(self, square):
        if square.owner:
            raise Exception("%s cannot buy square because square owned by %s" % (self.name, square.owner.name))
        if self.balance < square.price:
            raise Exception("%s cannot buy square because insufficient balance" % self.name)
        self.balance -= square.price
        # increase net_value, by how much?
        self.properties.append(square)
        if self.owns_color(square.color):
            self.owned_colors.append(square.color)
        square.owner = self

    # check if player owns all properties of a color. not an efficient implementation
    def owns_color(self, color):
        color_squares = self.board.get_color_group(color)
        for square in color_squares:
            if square not in self.properties:
                return False
        return True

    def pay_rent(self, square):
        # print "%s is paying rent" % self.name

        if square.owner != self:
            # player must mortgage or sell something to raise balance
            while self.balance < square.get_rent():
                # if bankrupt, pay with whatever balance is available
                if not self.do_strat_raise_money():
                    square.owner.balance += self.balance
                    self.balance = 0
                    return
            self.balance -= square.get_rent()
            square.owner.balance += square.get_rent()

    def pay_tax(self, square):
        tax = 0
        if square.position == 4:  # income tax
            # pay either 10% of balance or $200, whichever is smaller
            if self.balance * 0.1 < 200:
                tax = self.balance * 0.1
            else:
                tax = 200
        else:  # luxury tax
            tax = 75
        # player must mortgage or sell something to raise balance
        while self.balance < tax:
            # if bankrupt, pay with whatever balance is available
            if not self.do_strat_raise_money():
                self.balance = 0
                return
        self.balance -= tax

    def go_to_jail(self):
        self.prev_position = self.position
        self.position = 10
        self.in_jail = True

    def purchase_square(self, square):
        if square.owner:
            raise Exception("Cannot purchase square, already owned")
        if square.price > self.balance:
            raise Exception("Cannot purchase square, exceeds balance")
        square.owner = self
        self.balance -= square.price
        self.properties.append(square)

    def swap_squares(self, other_player):
        pass

    # number houses on properties of any given color cannot differ by more than 1
    def check_purchase_house(self, square, board):
        if board.avail_houses > 0 and self.balance > square.price_build:
            if square.color not in self.owned_colors:
                return False
            if square.num_building >= 4:        # can only upgrade to hotel
                return False
            other_color_squares = list(self.board.get_color_group(square.color))
            other_color_squares.remove(square)
            for s in other_color_squares:
                if abs(square.num_building + 1 - s.num_buildings) > 1:
                    return False
            return True
        return False

    def check_purchase_hotel(self, square, board):
        if board.avail_hotels > 0 and self.balance > square.price_build:
            if square.color not in self.owned_colors:
                return False
            if square.num_building != 4:        # must have 4 to purchase hotel
                return False
            other_color_squares = list(self.board.get_color_group(square.color))
            other_color_squares.remove(square)
            for s in other_color_squares:
                if abs(square.num_building + 1 - s.num_buildings) > 1:
                    return False
            return True
        return False

    def purchase_house(self, square, board):
        if self.check_purchase_house(square, board):
            board.avail_houses -= 1
            square.num_building += 1
            self.balance -= square.price_build

    def purchase_hotel(self, square, board):
        if self.check_purchase_hotel(square, board):
            board.avail_houses += 4
            board.avail_hotels -= 1
            square.num_building += 1 # now at 5
            self.balance -= square.price_build

    def do_strat_buy_buildings(self):
        raise NotImplementedError

    # strategy for unowned properties
    def do_strat_unowned_square(self, square):
        raise NotImplementedError

    # return False if bankrupt, else True
    def do_strat_raise_money(self, money):
        raise NotImplementedError

    def do_strat_get_out_of_jail(self, d):
        raise NotImplementedError

