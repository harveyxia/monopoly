from monopoly.board import Board
from monopoly.monopoly import Monopoly
from players.basic_player import BasicPlayer


def run():
    board = Board()
    players = [BasicPlayer(color_index=board.color_index, name="BasicPlayer1"),
               BasicPlayer(color_index=board.color_index, name="BasicPlayer2")]
    monopoly = Monopoly(players, max_money=1000)
    monopoly.run_debug()
