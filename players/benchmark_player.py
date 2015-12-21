# used for benchmarking
# based on the strategy described here: http://www.amnesta.net/other/monopoly/
from monopoly.player import Player


class BenchmarkPlayer(Player):
    def __init__(self, name):
        super(BenchmarkPlayer, self).__init__(name)
        self.focus = None
        self.first_monopoly = False
        self.late_game = False
        self.late_game_finished = False

    def do_strat_unowned_square(self, square):
        if self.balance < square.price + self.largest_rent():
            self.explain("Rejecting " + square.name + " because we don't have enough money")
            return False
        if square.type == 'Railroad':  # always buy railroads
            self.explain("Buying " + square.name + " because we always buy railroads")
            return True
        elif square.type == 'utility':  # never buy utilities
            self.explain("Rejecting " + square.name + " because we never buy utilities")
            return False
        else:
            if square.color:
                # Waterfall step 1: try to obtain or block a monopoly
                rest_of_monopoly = self.board.get_color_group(square.color)
                owned = 0
                others_owned = 0
                personally_owned = 0
                owners = set()
                total = len(rest_of_monopoly)
                for s in rest_of_monopoly:
                    if s != square:
                        if s.owner:
                            owned += 1
                            if self == s.owner:
                                personally_owned += 1
                            else:
                                others_owned += 1
                            owners.add(s.owner)
                if owned == total - 1 and len(owners) == 1:
                    # obtain monopoly or block it
                    if self.focus == square.color:
                        # obtained our current focused monopoly
                        self.explain("Buying " + square.name + " to finish our monopoly on " + square.color)
                        self.focus = None
                        if not self.late_game:
                            # start looking at sides 2 and 3
                            self.late_game = True
                        else:
                            # we got our sides 2 and 3 monopoly now as well
                            self.late_game_finished = True
                    else:
                        self.explain("Buying " + square.name + " to block opponent monopoly on " + square.color)
                    return True

                # If this is the color group we're currently focusing on
                if self.focus == square.color:
                    if others_owned == 0:
                        self.explain("Buying " + square.name + " because we are currently focusing on the " + square.color + " color group")
                        return True
                    else:
                        # need to change focus now
                        self.focus = None

                # Waterfall step 2: focus on color group in sides 1 and 2
                if not self.late_game:
                    # waterfall through color priorities if we don't have a focus
                    if square.color == "Orange":
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            self.explain("Buying " + square.name + " because " + square.color + " is the best color group we can monopolize right now")
                            return True
                    should_orange = self.should_focus_color("Orange")

                    if square.color == "LightBlue" and not should_orange:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            self.explain("Buying " + square.name + " because " + square.color + " is the best color group we can monopolize right now")
                            return True
                    should_lightblue = self.should_focus_color("LightBlue")

                    if square.color == "Pink" and not should_orange and not should_lightblue:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            self.explain("Buying " + square.name + " because " + square.color + " is the best color group we can monopolize right now")
                            return True
                    should_pink = self.should_focus_color("Pink")

                    if square.color == "Brown" and not should_orange and not should_lightblue and not should_pink:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            self.explain("Buying " + square.name + " because " + square.color + " is the best color group we can monopolize right now")
                            return True
                    should_brown = self.should_focus_color("Brown")

                    # all of our prioritized colors are gone, enter late game strategy
                    if not should_orange and not should_lightblue and not should_pink and not should_brown:
                        self.late_game = True
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            self.explain("Buying " + square.name + " because " + square.color + " is the best color group we can monopolize right now")
                            return True

                    # fell through, don't buy
                    self.explain("Rejecting " + square.name + " because " + square.color + " is not our current focus")
                    return False

                # Waterfall step 3: focus on color group sides 2 and 3
                else:
                    sides_2_and_3 = ["Pink", "Orange", "Red", "Yellow", "Green", "Blue"]
                    if square.color in sides_2_and_3:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            self.explain("Buying " + square.name + " because " + square.color + " is the best color group we can monopolize right now")
                            return True
                    else:
                        self.explain("Rejecting " + square.name + " because " + square.color + " is not our current focus")
                        return False

    def do_strat_raise_money(self, money):
        # filter properties
        to_sell = self.properties
        monopoly_properties = []
        for prop in to_sell:
            if prop.color in self.owned_colors:
                to_sell.remove(prop)
                monopoly_properties.append(prop)

        # sell non-monopolies
        while to_sell and self.balance < money:
            p = to_sell.pop()
            p.owner = None
            self.balance += p.price
            self.explain("Selling " + p.name + " because we don't have a monopoly here and we need the money")

        # sell monopolies if we still need money
        while monopoly_properties and self.balance < money:
            p = monopoly_properties.pop()
            if p.num_buildings == 0:
                p.owner = None
                self.balance += p.price
                self.explain("Selling " + p.name + " and breaking up our monopoly because we need the money and we have no other choice")
            elif p.num_buildings == 5:
                self.sell_hotel(p)
                self.explain("Selling a hotel on " + p.name + " because we need the money and we have no other choice")
            else:
                self.sell_house(p)
                self.explain("Selling a house on " + p.name + " because we need the money and we have no other choice")

        # process
        if self.balance < money:
            self.bankrupt = True
            return self.balance
        self.balance -= money
        return money

    def do_strat_buy_from_bank(self, bldgs):
        if bldgs:
            # buy max 3
            for bldg in bldgs:
                if bldg.num_buildings < 3:
                    self.explain("Building " + bldg.name + " up to 3 houses max, so we can save money for other properties")
                    return bldg

            # all already have 3 AND we have a late game monopoly, so now
            # we can just buy more and more
            if self.late_game_finished:
                self.explain("Building " + bldg.name + " all the way since we have a late game monopoly already")
                return bldg
        else:
            return None

    def do_strat_get_out_of_jail(self, d):
        # TODO: use get out of jail cards
        if self.jail_duration >= 3:
            self.jail_duration = 0
            self.in_jail = False
            if d[1] != d[0]:
                self.do_strat_raise_money(50)
            self.explain("Leaving jail after our third turn (mandatory)")
            return True
        elif self.focus == "Orange" and self.trying_to_complete_orange():
            # stay in Jail and try to get out by rolling doubles to buy St. James or Tennessee Ave
            self.jail_duration += 1
            self.explain("Staying in jail and trying to roll doubles to buy St. James or Tennessee Ave to complete our monopoly")
            return False
        elif self.others_have_monopoly():
            # moving around board will likely lose money
            self.jail_duration += 1
            self.explain("Staying in jail to try and avoid losing money to opponent monopoly")
            return False
        else:
            # get out, it's too early to be in jail
            self.do_strat_raise_money(50)
            self.explain("Leaving jail ASAP because it's too early to waste time in jail")
            return True

    ############################
    #                          #
    #         HELPERS          #
    #                          #
    ############################

    # look at board and check if we should focus on a specific color
    def should_focus_color(self, color):
        rest_of_monopoly = self.board.get_color_group(color)
        others_owned = 0
        for s in rest_of_monopoly:
            if s.owner and self != s.owner:
                others_owned += 1
        if others_owned > 0:
            return False
        else:
            return True

    def trying_to_complete_orange(self):
        if self.board.squares[16].owner == self and self.board.squares[19].owner == self:
            # need Tennessee Avenue to complete monopoly
            return True
        elif self.board.squares[18].owner == self and self.board.squares[19].owner == self:
            # need St. James Place to complete monopoly
            return True
        else:
            return False
