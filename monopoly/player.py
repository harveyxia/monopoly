# the player does not do any checks to make sure the board is internally
# consistent. it either does things, or implements logic that says yes or no

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

    ############################
    #                          #
    #           MOVE           #
    #                          #
    ############################

    # advances the player by num_squares
    def move(self, num_squares):
        if self.in_jail:
            raise Exception("%s cannot move because in jail." % self.name)
        if (self.position + num_squares > 40):
            self.years = self.years + 1
        self.position = (self.position + num_squares) % 40

    def go_to_jail(self):
        self.prev_position = self.position
        self.position = 10
        self.in_jail = True

    def leave_jail(self, d):
        return self.do_strat_get_out_of_jail(d)

    # def swap_squares(self, other_player):
    #     pass

    ############################
    #                          #
    #          PAY UP          #
    #                          #
    ############################

    # pays rent
    # calls do_strat_raise_money
    def pay_rent(self, square):
        # print "%s is paying rent" % self.name
        if square.owner == self:
            raise Exception("I (%s) own %s" % (self.name, square.owner.name))
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

    ############################
    #                          #
    #         PURCHASE         #
    #                          #
    ############################

    def purchase_house(self, square, board):
        board.avail_houses -= 1
        square.num_building += 1
        self.balance -= square.price_build

    def purchase_hotel(self, square, board):
        board.avail_houses += 4
        board.avail_hotels -= 1
        square.num_building += 1 # now at 5
        self.balance -= square.price_build

    # buys a square for a player
    # does NOT check permissions - will die if you try to buy something you can't
    def purchase_square(self, square):
        if not self.do_strat_unowned_square(square):
            return
        if square.owner:
            raise Exception("%s cannot buy square because square owned by %s" % (self.name, square.owner.name))
        if self.balance < square.price:
            raise Exception("%s cannot buy square because insufficient balance" % self.name)
        self.balance -= square.price
        # increase net_value, by how much?
        self.properties.append(square)
        if square.color is None and self.owns_color(square.color):
            self.owned_colors.append(square.color)
        square.set_owner(self)

    def purchase_buildings(self):
        return self.do_strat_buy_buildings()

    ############################
    #                          #
    #       HELPFUL STUFF      #
    #                          #
    ############################

    # check if player owns all properties of a color. 
    # not an efficient implementation
    def owns_color(self, color):
        color_squares = self.board.get_color_group(color)
        for square in color_squares:
            if square not in self.properties:
                return False
        return True

    ############################
    #                          #
    #          STRATS          #
    #                          #
    ############################

    def do_strat_buy_buildings(self):
        raise NotImplementedError

    # strategy for unowned properties
    def do_strat_unowned_square(self, square):
        raise NotImplementedError

    # return False if bankrupt, else True
    # this will raise the amount of money or die trying
    def do_strat_raise_money(self, money):
        raise NotImplementedError

    # it returns TRUE if you got out of jail and FALSE otherwise
    # all the game mechanism - such as paying 50 bucks if you fail to
    # get out of jail on your third turn - should be implemented HERE
    # you pass the dice roll in so that you can figure out if you
    # successfully rolled out of jail, BUT the actually movement of the player
    # should take place in monopoly
    def do_strat_get_out_of_jail(self, d):
        raise NotImplementedError

