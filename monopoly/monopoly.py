from board import Board
from player import Player
from random import randint
import json


class Monopoly(object):
    """
    Monopoly class, represents entirety of game
    """

    def __init__(self, num_players=4):
        self.board = Board()
        self.num_players = num_players
        self.players = [Player("player" + str(i)) for i in xrange(num_players)]
        self.player_turn = 0    # which Player has next move, default first player

        self.is_over = False    # true if game is over
        self.winner = None

    # game consists of N moves until all but one player is bankrupt
    def make_move(self):
        player = self.players[self.player_turn]
        dice = self.roll_dice()
        player.do_strategy()
        if dice[0] == dice[1]:              # doubles, roll again
            dice = self.roll_dice()
            player.do_strategy()
            if dice[0] == dice[1]:          # third double, go to jail
                player.go_to_jail()

    def roll_dice(self):
        return randint(1, 6), randint(1, 6)

    def do_square_action(self):
        # if pass GO, get $200
        # if go to jail, go to fail
        # if land on owned property, pay rent
        # if land on tax, pay tax
        # if land on chance or community, pick card and do card
        pass

    def run(self):
        while not self.is_over:
            pass

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
            m.players = [Player(data["players"][i]["name"]) for i in xrange(data["num_players"])]
            m.player_turn = data["player_turn"]
            m.is_over = data["is_over"]
            m.winner = data["winner"]
            for i, player in enumerate(m.players):
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

    # Takes current Monopoly game and creates a pretty-printed JSON file that
    # can be loaded using Monopoly.set_state()
    def save_state(self, transcript="transcript.json"):
        data = {}
        data["num_players"] = self.num_players
        data["player_turn"] = self.player_turn
        data["is_over"] = self.is_over
        data["winner"] = self.winner
        data["board"] = {}
        data["board"]["avail_houses"] = self.board.avail_houses
        data["board"]["avail_hotels"] = self.board.avail_hotels
        data["players"] = []
        for player in self.players:
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
        with open(transcript, 'w') as outfile:
            json.dump(data, outfile, indent = 2)
