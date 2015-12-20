# monopoly is responsible for:
#   running the game
#   turn-by-turn mechanics
#   asking the player for input
#     check to see if legal move
#     ask player for strat (returns TRUE or FALSE)
#     if player says yes, ask player to do thing (player doesn't check anything)
#   state variable

import json
import random
from random import randint

from board import Board
from player import Player


class Monopoly(object):
    """
    Monopoly class, represents entirety of game
    """

    def __init__(self, players, max_money=None):
        """

        :type players: Player() subclass
        """
        if len(players) < 2:
            raise Exception("num_players must be greater than 1")

        self.board = Board()
        self.num_players = len(players)
        self.players = players
        for player in players:
            player.board = self.board
        # num_active_players and active_players don't include bankrupt players
        self.num_active_players = self.num_players
        self.active_players = self.players
        self.player_turn = 0  # which Player has next move, default first player
        self.dice = None

        self.max_money = max_money  # artificial cap on maximum money given out from passing GO

        self.is_over = False  # true if game is over
        self.winner = None

        self.chance_jail_owner = None
        self.shuffle_chance_cards()
        self.community_chest_jail_owner = None
        self.shuffle_community_chest_cards()

    ############################
    #                          #
    #      OTHER GETTERS       #
    #                          #
    ############################

    def return_years(self):
        years = []
        for player in self.players:
            years.append(player.years)
        return years

    ############################
    #                          #
    #            RUN           #
    #                          #
    ############################

    def run(self):
        while self.num_active_players > 1:
            self.make_move()
        self.is_over = True
        self.winner = self.active_players[0]
        print "--------------------Game finished---------------------"
        print "%s wins!" % self.winner.name

    def run_debug(self):
        while self.num_active_players > 1:
            player = self.make_move()
            # print player
            print "%s balance: %s" % (player.name, str(player.balance))
        self.is_over = True
        self.winner = self.active_players[0]
        print "--------------------Game finished---------------------"
        print "%s wins!" % self.winner.name

    ############################
    #                          #
    #      TURN MECHANICS      #
    #                          #
    ############################

    def roll_dice(self):
        self.dice = randint(1, 6), randint(1, 6)
        return self.dice

    def use_get_out_of_jail_free_card(self, player):
        if player != self.chance_jail_owner or player != self.community_chest_jail_owner:
            return False # doesn't own one
        if player == self.chance_jail_owner:
            player.in_jail = False
            self.chance_jail_owner = None
            self.chance_cards.insert(0, 7) # add the card to the back of the deck
        elif player == self.community_chest_jail_owner:
            player.in_jail = False
            self.community_chest_jail_owner = None
            self.community_chest_cards.insert(0, 5)
        return True

    # game consists of N moves until all but one player is bankrupt
    def make_move(self):
        player = self.active_players[self.player_turn]
        self.player_turn = (self.player_turn + 1) % self.num_active_players
        if player.in_jail:
            # TODO: use community chest, should be part of the jail strategy
            # if player == self.chance_jail_owner or player == self.community_chest_jail_owner:
            #     if self.use_get_out_of_jail_free_card(player):
            #         successfully used it, now roll
            #         self.roll_and_move(player, dice)
            #         return
            dice = self.roll_dice()
            if player.leave_jail(dice):
                self.roll_and_move(player, dice)
        else:
            self.roll_and_move(player)
        return player

    def roll_and_move(self, player, dice=None, turn=1):
        if dice is None:
            dice = self.roll_dice()
        if turn == 3 and dice[0] == dice[1]:
            player.go_to_jail()
        else:
            prev_position = player.position
            player.move(dice[0] + dice[1])
            self.do_square_action(player, prev_position)
            if dice[0] == dice[1] and not player.in_jail:  # first doubles, roll again if not in jail
                self.roll_and_move(player, turn=turn + 1)

    # chance flag is true if we are performing an action after being moved there via a chance card
    def do_square_action(self, player, prev_position, chance=False):
        square = self.board.squares[player.position]
        # if pass GO, get $200
        if player.position < prev_position:
            self.change_player_balance(player, 200)

        # do nothing jail, free parking squares
        if player.position in (0, 10, 20):
            return

        # if go to jail, go to jail
        if player.position == 30:
            player.go_to_jail()
        # if land on income or luxury tax, pay tax
        elif player.position == 4 or player.position == 38:
            player.pay_tax(square)
        # if land on owned property, pay rent
        elif square.owner and square.owner is not player:
            if self.on_utility(player):
                roll = self.dice[0] + self.dice[1]
                if chance == True:
                    # chance card: utilities have to pay 10 times your roll
                    player.pay_rent(square, 10 * roll)
                elif self.board.squares[12].owner == self.board.squares[28].owner:
                    # same owner owns both utilities, pay 10 * roll
                    player.pay_rent(square, 10 * roll)
                else:
                    # different owners, pay 4 * roll
                    player.pay_rent(square, 4 * roll)
            elif self.on_railroad(player):
                railroads_owned = self.railroads_owned(square.owner)
                if chance == True:
                    # chance card: have to pay double the normal railroad rent
                    player.pay_rent(square, multiple=(railroads_owned * 2))
                else:
                    player.pay_rent(square, multiple=railroads_owned)
            else: # normal rent
                player.pay_rent(square)
        # if land on unowned property, do strat
        elif square.owner is None:
            # print "##########################################################"
            player.purchase_square(square)
        # if land on chance, pick card and do card
        elif self.on_chance(player):
            self.do_chance_card(player)
        elif self.on_community_chest(player):
            self.do_community_chest_card(player)
        # check if player is bankrupt, if so remove
        if player.bankrupt:
            self.active_players.remove(player)
            self.num_active_players -= 1

        while player.purchase_buildings(self.get_purchasable_buildings(player)):
            pass

    def change_player_balance(self, player, amount):
        if amount == 0:
            return
        if self.max_money is None:
            player.balance += amount
        elif self.max_money and self.max_money >= amount:
            player.balance += amount
            self.max_money -= amount

    def shuffle_chance_cards(self):
        self.chance_cards = range(1, 16)
        if self.chance_jail_owner != None:
            self.chance_cards.remove(7) # remove get out of jail card
        random.shuffle(self.chance_cards)


    def shuffle_community_chest_cards(self):
        self.community_chest_cards = range(1, 17)
        if self.community_chest_jail_owner != None:
            self.community_chest_cards.remove(5)
        random.shuffle(self.community_chest_cards)

    def do_chance_card(self, player):
        if len(self.chance_cards) == 0:
            self.shuffle_chance_cards()
        card = self.chance_cards.pop()
        prev_position = player.position

        if card == 1:
            # Advance to Go (Collect $200)
            player.position = 0
            self.change_player_balance(player, 200)
        elif card == 2:
            # Advance to Illinois Ave. - If you pass Go, collect $200
            player.position = 24
            self.do_square_action(player, prev_position, chance=True)
        elif card == 3:
            # Advance to St. Charles Place - If you pass Go, collect $200
            player.position = 11
            self.do_square_action(player, prev_position, chance=True)
        elif card == 4:
            # Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown.
            if player.position > 28:
                player.position = 28
            else:
                player.position = 12
            self.do_square_action(player, prev_position, chance=True)
        elif card == 5:
            # Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.
            if player.position > 35:
                player.position = 35
            elif player.position > 25:
                player.position = 25
            elif player.position > 15:
                player.position = 15
            else:
                player.position = 5
            self.do_square_action(player, prev_position, chance=True)
        elif card == 6:
            # Bank pays you dividend of $50
            self.change_player_balance(player, 50)
        elif card == 7:
            # Get out of Jail Free - This card may be kept until needed, or traded/sold
            if self.chance_jail_owner == None:
                self.chance_jail_owner = player
        elif card == 8:
            # Go Back 3 Spaces"
            player.position = prev_position - 3
            self.do_square_action(player, prev_position, chance=True)
        elif card == 9:
            # Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200
            player.go_to_jail()
        elif card == 10:
            # Make general repairs on all your property - For each house pay $25 - For each hotel $100
            to_pay = 0
            for property in player.properties:
                if property.num_buildings == 5:
                    to_pay -= 100
                else:
                    to_pay -= property.num_buildings * 25
            self.change_player_balance(player, to_pay)
        elif card == 11:
            # Pay poor tax of $15
            self.change_player_balance(player, -15)
        elif card == 12:
            # Take a trip to Reading Railroad - If you pass Go, collect $200
            player.position = 5
            self.do_square_action(player, prev_position, chance=True)
        elif card == 13:
            # Take a walk on the Boardwalk - Advance token to Boardwalk
            player.position = 39
            self.do_square_action(player, prev_position, chance=True)
        elif card == 14:
            # You have been elected Chairman of the Board - Pay each player $50
            for p in self.active_players:
                player.pay_player(p, 50)
        elif card == 15:
            # Your building and loan matures - Collect $150
            self.change_player_balance(player, 150)
        elif card == 16:
            # You have won a crossword competition - Collect $100
            self.change_player_balance(player, 100)

    def do_community_chest_card(self, player):
        if len(self.community_chest_cards) == 0:
            self.shuffle_community_chest_cards()
        card = self.community_chest_cards.pop()
        prev_position = player.position

        if card == 1:
            # Advance to Go (Collect $200)
            player.position = 0
            self.change_player_balance(player, 200)
        elif card == 2:
            # Bank error in your favor - Collect $200
            self.change_player_balance(player, 200)
        elif card == 3:
            # Doctor's fees - Pay $50
            self.change_player_balance(player, -50)
        elif card == 4:
            # From sale of stock you get $50
            self.change_player_balance(player, 50)
        elif card == 5:
            # Get out of Jail Free - This card may be kept until needed, or traded/sold
            if self.community_chest_jail_owner == None:
                self.community_chest_jail_owner = player
        elif card == 6:
            # Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200
            player.go_to_jail()
        elif card == 7:
            # Grand Opera Night - Collect $50 from every player for opening night seats
            for p in self.active_players:
                p.pay_player(player, 50)
        elif card == 8:
            # Holiday Fund matures - Receive $100
            self.change_player_balance(player, 100)
        elif card == 9:
            # Income tax refund - Collect $20
            self.change_player_balance(player, 20)
        elif card == 10:
            # It is your birthday - Collect $10 from each player
            for p in self.active_players:
                p.pay_player(player, 10)
        elif card == 11:
            # Life insurance matures - Collect $100
            self.change_player_balance(player, 100)
        elif card == 12:
            # Pay hospital fees of $100
            self.change_player_balance(player, -100)
        elif card == 13:
            # Pay school fees of $150
            self.change_player_balance(player, -150)
        elif card == 14:
            # Receive $25 consultancy fee
            self.change_player_balance(player, 25)
        elif card == 15:
            # You are assessed for street repairs - $40 per house - $115 per hotel
            to_pay = 0
            for property in player.properties:
                if property.num_buildings == 5:
                    to_pay -= 115
                else:
                    to_pay -= property.num_buildings * 40
            self.change_player_balance(player, to_pay)
        elif card == 16:
            # You have won second prize in a beauty contest - Collect $10
            self.change_player_balance(player, 10)
        elif card == 17:
            # You inherit $100
            self.change_player_balance(player, 100)

    ############################
    #                          #
    #     INTEGRITY CHECK      #
    #                          #
    ############################

    # number houses on properties of any given color cannot differ by more than 1
    # should return the set of squares for which houses are possible
    def check_purchase_house(self, square, player):
        if self.board.avail_houses > 0 and player.balance > square.price_build:
            if square.color not in player.owned_colors:
                return False
            if square.num_buildings >= 4:        # can only upgrade to hotel
                return False
            other_color_squares = list(self.board.get_color_group(square.color))
            other_color_squares.remove(square)
            for s in other_color_squares:
                if abs(square.num_buildings + 1 - s.num_buildings) > 1:
                    return False
            return True
        return False

    # should return the set of squares for which hotels are possible
    def check_purchase_hotel(self, square, player):
        if self.board.avail_hotels > 0 and player.balance > square.price_build:
            if square.color not in player.owned_colors:
                return False
            if square.num_buildings != 4:        # must have 4 to purchase hotel
                return False
            other_color_squares = list(self.board.get_color_group(square.color))
            other_color_squares.remove(square)
            for s in other_color_squares:
                if abs(square.num_buildings + 1 - s.num_buildings) > 1:
                    return False
            return True
        return False

    ############################
    #                          #
    #         HELPERS          #
    #                          #
    ############################

    def on_utility(self, player):
        return player.position == 12 or player.position == 28

    def on_railroad(self, player):
        return player.position == player.position == 5 or player.position == 15 or player.position == 25 or player.position == 35

    def on_chance(self, player):
        return player.position == 7 or player.position == 22 or player.position == 36

    def on_community_chest(self, player):
        return player.position == 2 or player.position == 17 or player.position == 33

    def railroads_owned(self, player):
        owned = 0
        if self.board.squares[5].owner == player:
            owned += 1
        if self.board.squares[15].owner == player:
            owned += 1
        if self.board.squares[25].owner == player:
            owned += 1
        if self.board.squares[35].owner == player:
            owned += 1
        return owned

    def get_purchasable_buildings(self, player):
        return [square for square in player.properties
                if self.check_purchase_house(square, player)
                or self.check_purchase_hotel(square, player)]

    ############################
    #                          #
    #          STATE           #
    #                          #
    ############################

    def get_npvs():
        return [(square.name, square.npvs) for square in board.squares]

    # Reads in a JSON transcript and returns a new Monopoly instance
    @classmethod
    def set_state(self, transcript):
        if transcript:
            m = Monopoly()
            data = open(transcript).read()
            data = json.loads(data)
            m.board = Board()
            m.board.avail_houses = data["board"]["avail_houses"]
            m.board.avail_hotels = data["board"]["avail_hotels"]
            m.active_players = [Player(data["players"][i]["name"]) for i in xrange(data["num_players"])]
            m.player_turn = data["player_turn"]
            m.is_over = data["is_over"]
            m.winner = data["winner"]
            for i, player in enumerate(m.active_players):
                player.balance = data["players"][i]["balance"]
                player.net_value = data["players"][i]["net_value"]
                player.in_jail = data["players"][i]["in_jail"]
                player.position = data["players"][i]["position"]
                player.bankrupt = data["players"][i]["bankrupt"]
                for property in data["players"][i]["properties"]:
                    square = next((x for x in m.board.squares if x.name == property["name"]), None)
                    if square:
                        square.num_buildings = property["num_buildings"]
                        player.properties.append(square)
            return m
        else:
            raise Exception("Must pass in a transcript JSON file")

    # Takes current Monopoly game and optionally creates a pretty-printed JSON file that
    # can be loaded using Monopoly.set_state()
    # returns the dict
    def save_state(self, output_file=False, transcript="transcript.json"):
        data = {}
        data["num_players"] = self.num_active_players
        data["player_turn"] = self.player_turn
        data["is_over"] = self.is_over
        data["winner"] = self.winner
        data["board"] = {}
        data["board"]["avail_houses"] = self.board.avail_houses
        data["board"]["avail_hotels"] = self.board.avail_hotels
        data["players"] = []
        for player in self.active_players:
            player_data = {}
            player_data["name"] = player.name
            player_data["balance"] = player.balance
            player_data["net_value"] = player.net_value
            player_data["in_jail"] = player.in_jail
            player_data["position"] = player.position
            player_data["bankrupt"] = player.bankrupt
            player_data["properties"] = []
            for property in player.properties:
                property_data = {}
                property_data["name"] = property.name
                property_data["num_buildings"] = property.num_buildings
                player_data["properties"].append(property_data)
            data["players"].append(player_data)
        if output_file:
            with open(transcript, 'w') as outfile:
                json.dump(data, outfile, indent=2)
        return data
