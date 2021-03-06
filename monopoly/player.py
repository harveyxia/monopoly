# the player does not do any checks to make sure the board is internally
# consistent. it either does things, or implements logic that says yes or no

flag = True # set to True to turn on player explanations

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
        self.years = 0
        # these are set by monopoly
        self.board = None
        self.other_players = None

    def __str__(self):
        return "%s:\n  " \
               "position:%s\n  " \
               "balance:%s\n  " \
               "properties:%s\n  " \
               "in_jail:%s" % \
               (self.name, self.position, self.balance, self.properties, self.in_jail)

    def explain(self, message):
        if flag:
            print self.name + ": " + message

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
        square.add_building()  # now at 5
        self.board.avail_houses += 4
        self.board.avail_hotels -= 1
        self.balance -= square.price_build

    def check_square_status(self, square):
        if square.color != "None":
            color_squares = self.board.get_color_group(square.color)
            color_squares = filter(lambda x: x.name != square.name, color_squares)
            owners = set()
            sq_left = len(color_squares)
            idx = 0
            for s in color_squares:
                if s.owner != None:
                    sq_left -= 1
                    owners.add(s.owner.name)
            if sq_left == 1:
                if len(owners) == 2:
                    idx = 0  # no_monopoly
                elif self.name in owners:
                    idx = 5  # one_from_monopoly_me
                else:
                    idx = 1  # one_from_monopoly
            elif sq_left == 2:
                if self.name in owners:
                    idx = 4  # two_from_monopoly_me
                else:
                    idx = 2  # two_from_monopoly
            else:
                idx = 3  # three_from_monopoly
        else:
            idx = 0
        return idx

    # buys a square for a player
    # does NOT check permissions - will die if you try to buy something you can't
    def purchase_square(self, square):
        if not self.do_strat_unowned_square(square):
            return False
        if square.owner and not square.mortgaged:
            raise Exception("%s cannot buy square because square owned by %s" % (self.name, square.owner.name))
        price_to_pay = square.price
        if square.mortgaged:
            price_to_pay = square.price * 1.1  # 10% interest
        if self.balance < price_to_pay:
            raise Exception("%s cannot buy square because insufficient balance" % self.name)
        self.do_strat_raise_money(price_to_pay)
        # increase net_value, by how much?
        self.properties.append(square)
        if square.color != "None" and self.owns_color(square.color):
            # print self.name, "got all of", square.color
            self.owned_colors.append(square.color)

        square.set_owner(self, self.check_square_status(square))

        # print self.name, "is buying", square.name
        if square.mortgaged:
            square.unmortgage()
        return True

    def purchase_from_banks(self, potential_buildings):
        square = self.do_strat_buy_from_bank(potential_buildings)
        if square is None:
            return False
        elif square.mortgaged:
            self.purchase_square(square)
        elif square.num_buildings < 4:
            self.purchase_house(square)
            # print self.name, "is buying a house on", square.name
        else:
            self.purchase_hotel(square)
            # print self.name, "is buying a hotel on", square.name
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
        self.board.avail_hotels += 1
        if self.board.avail_houses >= 4:
            # If there are enough houses, only sell the hotel
            square.num_buildings = 4
            self.board.avail_houses -= 4
            self.balance += 0.5 * (1 * square.price_build)
        elif self.board.avail_houses == 0:
            # No more houses left, we have to sell everything
            square.num_buildings = 0
            self.balance += 0.5 * (5 * square.price_build)
        else:
            # Keep as many as we can
            square.num_buildings = self.board.avail_houses
            self.board.avail_houses = 0
            self.balance += 0.5 * ((5 - self.board.avail_houses) * square.price_build)

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

    def others_have_monopoly(self):
        if any([len(other.owned_colors) > 0 for other in self.other_players]):
            # print "others have monopoly"
            return True
        else:
            return False

    def largest_rent(self):
        rents = [square.get_rent()
                 for square in self.board.squares
                 if square.owner and square.owner != self]
        if len(rents) > 0:
            return max(rents)
        else:
            return 0

    ############################
    #                          #
    #          STRATS          #
    #                          #
    ############################

    # input value: list of squares
    # return value: the square you want to change
    #
    # strategy for buying from the bank, called at the end of every turn
    # you are given a list of squares on which you could build buildings
    # and you need to decide whether you want to unmortage a square
    # or you want to build a building on a square that was passed in
    # the return value should be the square you want to change
    # so the calling function takes care of the logic of whether to unmortage
    # or to add a building
    def do_strat_buy_from_bank(self, potential_buildings):
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
