from monopoly.board import Board
from monopoly.monopoly import Monopoly
from players.basic_player import BasicPlayer


def run():
    players = [BasicPlayer("BasicPlayer1"),
               BasicPlayer("BasicPlayer2")]
    monopoly = Monopoly(players, max_money=1000)
    monopoly.run_debug()
