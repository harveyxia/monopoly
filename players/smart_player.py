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
                print self.focus
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



    # sell properties to raise money, in no particular order
    # todo: change this! this is currently here so that payment isn't None
    def do_strat_raise_money(self, money):
        while self.properties and self.balance < money:
            p = self.properties.pop()
            p.owner = None
            self.balance += p.price
        if self.balance < money:
            self.bankrupt = True
            return self.balance
        self.balance -= money
        return money

    def do_strat_buy_buildings(self, squares):
        pass

    def do_strat_get_out_of_jail(self, d):
        pass

    # look at board
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
