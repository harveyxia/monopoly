# used for benchmarking
# based on the strategy described here: http://www.amnesta.net/other/monopoly/
from monopoly.player import Player


class SmartPlayer(Player):
    def __init__(self, name):
        super(SmartPlayer, self).__init__(name)
        self.focus = None
        self.first_monopoly = False
        self.late_game = False

    def do_strat_unowned_square(self, square):
        if self.balance < square.price:
            return False
        if square.type == 'Railroad': # always buy railroads
            return True
        elif square.type == 'utility': # never buy utilities
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
                        # obtained our focused monopoly
                        self.focus = None
                        self.late_game = True
                    return True
                
                # If this is the color group we're currently focusing on
                if self.focus == square.color:
                    if others_owned == 0:
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
                            return True
                    should_orange = self.should_focus_color("Orange")

                    if square.color == "LightBlue" and not should_orange:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            return True
                    should_lightblue = self.should_focus_color("LightBlue")

                    if square.color == "Pink" and not should_orange and not should_lightblue:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            return True
                    should_pink = self.should_focus_color("Pink")

                    if square.color == "Brown" and not should_orange and not should_lightblue and not should_pink:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            return True

                    # fell through, don't buy
                    return False
                        
                # Waterfall step 3: focus on color group sides 2 and 3
                else:
                    sides_2_and_3 = ["Pink", "Orange", "Red", "Yellow", "Green", "Blue"]
                    if square.color in sides_2_and_3:
                        if others_owned == 0 and self.focus == None:
                            self.focus = square.color
                            return True
                    else:
                        return False



    def do_strat_raise_money(self, money):
        # filter properties
        to_sell = self.properties
        monopoly_properties = []

        # sell non-monopolies
        for prop in to_sell:
            if prop.color in self.owned_colors:
                to_sell.remove(prop)
                monopoly_properties.append(prop)
        while to_sell and self.balance < money:
            p = to_sell.pop()
            p.owner = None
            self.balance += p.price

        # sell monopolies if we still need money
        while monopoly_properties and self.balance < money:
            p = monopoly_properties.pop()
            p.owner = None
            self.balance += p.price

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
            return True
        elif self.focus == "Orange" and self.trying_to_complete_orange():
            # stay in Jail and try to get out by rolling doubles to buy St. James or Tennessee Ave
            self.jail_duration += 1
            return False
        elif self.others_have_monopoly():
            # moving around board will likely lose money
            self.jail_duration += 1
            return False
        else:
            # get out, it's too early to be in jail
            self.do_strat_raise_money(50)
            return True

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
