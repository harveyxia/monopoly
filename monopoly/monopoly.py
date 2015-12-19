# monopoly is responsible for:
#   running the game
#   turn-by-turn mechanics
#   asking the player for input
#     check to see if legal move
#     ask player for strat (returns TRUE or FALSE)
#     if player says yes, ask player to do thing (player doesn't check anything)
#   state variable

import json
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

        self.max_money = max_money  # artificial cap on maximum money given out from passing GO

        self.is_over = False  # true if game is over
        self.winner = None

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

    @staticmethod
    def roll_dice():
        return randint(1, 6), randint(1, 6)

    # game consists of N moves until all but one player is bankrupt
    def make_move(self, move_only=False):
        player = self.active_players[self.player_turn]
        self.player_turn = (self.player_turn + 1) % self.num_active_players
        if player.in_jail:
            if not player.do_strat_get_out_of_jail(self.roll_dice()):
                return player
        
        self.roll_and_move(player, move_only=move_only)
        return player

    def roll_and_move(self, player, move_only=False):
        dice = self.roll_dice()
        prev_position = player.position
        player.move(dice[0] + dice[1])
        if not move_only:
            self.do_square_action(player, prev_position)
        if dice[0] == dice[1] and not player.in_jail:  # first doubles, roll again if not in jail
            dice = self.roll_dice()
            prev_position = player.position
            player.move(dice[0] + dice[1])
            if not move_only:
                self.do_square_action(player, prev_position)
            if dice[0] == dice[1] and not player.in_jail:  # second doubles, roll again if not in jail
                dice = self.roll_dice()
                if dice[0] == dice[1]:  # third doubles, go to jail
                    player.go_to_jail()
                else:
                    prev_position = player.position
                    player.move(dice[0] + dice[1])
                    if not move_only:
                        self.do_square_action(player, prev_position)

    def do_square_action(self, player, prev_position):
        square = self.board.squares[player.position]
        # if pass GO, get $200
        if player.position < prev_position:
            if self.max_money is None:
                player.balance += 200
            elif self.max_money and self.max_money >= 200:
                player.balance += 200
                self.max_money -= 200

        # add logic to buy houses here
        player.do_strat_buy_buildings()

        # do nothing on chance, community, jail, free parking squares
        if player.position in (0, 2, 7, 10, 17, 20, 22, 33, 36):
            return

        # if go to jail, go to jail
        if player.position == 30:
            player.go_to_jail()
        # if land on income or luxury tax, pay tax
        elif player.position == 4 or player.position == 38:
            player.pay_tax(square)
        # if land on owned property, pay rent
        elif square.owner and square.owner is not player:
            player.pay_rent(square)
        # if land on unowned property, do strat
        elif square.owner is None:
            # print "##########################################################"
            player.do_strat_unowned_square(square)
        # if land on chance or community, pick card and do card
        # check if player is bankrupt, if so remove
        if player.bankrupt:
            self.active_players.remove(player)
            self.num_active_players -= 1

    ############################
    #                          #
    #     INTEGRITY CHECK      #
    #                          #
    ############################

    # number houses on properties of any given color cannot differ by more than 1
    def check_purchase_house(self, square, player):
        if se.fboard.avail_houses > 0 and player.balance > square.price_build:
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

    def check_purchase_hotel(self, square, player):
        if self.board.avail_hotels > 0 and player.balance > square.price_build:
            if square.color not in player.owned_colors:
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

    ############################
    #                          #
    #          STATE           #
    #                          #
    ############################

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
                        square.num_building = property["num_building"]
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
                property_data["num_building"] = property.num_building
                player_data["properties"].append(property_data)
            data["players"].append(player_data)
        if output_file:
            with open(transcript, 'w') as outfile:
                json.dump(data, outfile, indent=2)
        return data
