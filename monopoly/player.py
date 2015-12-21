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
        if self.position + num_squares > 40:
            self.years += 1
        self.position = (self.position + num_squares) % 40

    def go_to_jail(self):
        self.prev_position = self.position
        self.position = 10
        self.in_jail = True

    def leave_jail(self, d):
        if self.do_strat_get_out_of_jail(d):
            self.in_jail = False

    # def swap_squares(self, other_player):
    #     pass

    ############################
    #                          #
    #          PAY UP          #
    #                          #
    ############################

    # pays rent
    # calls do_strat_raise_money
    def pay_rent(self, square, multiple=1):
        # print "%s is paying rent" % self.name
        if square.owner == self:
            raise Exception("I (%s) own %s" % (self.name, square.owner.name))
        # player must mortgage or sell something to raise balance
        payment = self.do_strat_raise_money(square.get_rent() * multiple)
        square.track_payment(payment)
        square.owner.balance += payment

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
        self.do_strat_raise_money(tax)

    def pay_player(self, other_player, amount, track=False, square=None):
        payment = self.do_strat_raise_money(amount)
        if track and square:
            square.track_payment(payment)
        other_player.balance += payment

    ############################
    #                          #
    #         PURCHASE         #
    #                          #
    ############################

    def purchase_house(self, square):
        square.add_building()
        self.board.avail_houses -= 1
        self.balance -= square.price_build

    def purchase_hotel(self, square):
        square.add_building() # now at 5
        self.board.avail_houses += 4
        self.board.avail_hotels -= 1
        self.balance -= square.price_build

    # buys a square for a player
    # does NOT check permissions - will die if you try to buy something you can't
    def purchase_square(self, square):
        if not self.do_strat_unowned_square(square):
            return False
        if square.owner and not square.mortgaged:
            raise Exception("%s cannot buy square because square owned by %s" % (self.name, square.owner.name))
        price_to_pay = square.price
        if square.mortgaged:
            price_to_pay = square.price * 1.1 # 10% interest    
        if self.balance < price_to_pay:
            raise Exception("%s cannot buy square because insufficient balance" % self.name)
        self.balance -= price_to_pay
        # increase net_value, by how much?
        self.properties.append(square)
        if square.color != "None" and self.owns_color(square.color):
            # print self.name, "got all of", square.color
            self.owned_colors.append(square.color)
        square.set_owner(self)
        # print self.name, "is buying", square.name
        if square.mortgaged:
            square.unmortgage()
        return True

    def purchase_buildings(self, squares):
        building = self.do_strat_buy_buildings(squares)
        if building is None:
            return False
        elif building.num_buildings < 4:
            self.purchase_house(building)
            # print self.name, "is buying a house on", building.name
        else:
            self.purchase_hotel(building)
            # print self.name, "is buying a hotel on", building.name
        return True

    ############################
    #                          #
    #           SELL           #
    #                          #
    ############################

    def sell_house(self, square):
        square.remove_building()
        self.board.avail_houses += 1
        self.balance += 0.5 * square.price_build

    def sell_hotel(self, square):
        square.remove_building()
        self.board.avail_hotels += 1
        self.balance += 0.5 * (5 * square.price_build) # sell all 5

    def mortgage_square(self, square):
        square.mortgage()
        self.balance += 0.5 * square.price

    def liquidate(self):
        for prop in self.properties:
            prop.owner = None
            if prop.num_buildings == 5:
                self.board.avail_hotels += 1
            else:
                self.board.avail_houses += prop.num_buildings
            prop.num_buildings = 0
            prop.mortgaged = False

    ############################
    #                          #
    #       HELPFUL STUFF      #
    #                          #
    ############################

    # check if player owns all properties of a color. 
    # not an efficient implementation
    def owns_color(self, color):
        if color is None:
            return False
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

    # input value: list of square
    # return value: none
    #
    # strategy for buying buildings, called at the end of every turn
    def do_strat_buy_buildings(self, squares):
        raise NotImplementedError

    # input value: square
    # return value: TRUE if you want to buy and FALSE otherwise
    #
    # strategy for unowned properties
    def do_strat_unowned_square(self, square):
        raise NotImplementedError

    # input value: amount of money needed
    # return value: amount of money raised
    #
    # this will raise the amount of money or die trying
    # returns the amount of money raised
    # responsible for keeping player consistent, i.e. should bankrupt self
    # also updates amount of money a player has
    def do_strat_raise_money(self, money):
        raise NotImplementedError

    # input value: dice
    # output value: TRUE if you got out of jail and FALSE otherwise
    #
    # all the game mechanism - such as paying 50 bucks if you fail to
    # get out of jail on your third turn - should be implemented HERE
    # you pass the dice roll in so that you can figure out if you
    # successfully rolled out of jail, BUT the actually movement of the player
    # should take place in monopoly
    def do_strat_get_out_of_jail(self, d):
        raise NotImplementedError

