from monopoly.monopoly import Monopoly
from players.greedy_player import GreedyPlayer


def run():
    players = [GreedyPlayer("GreedyPlayer1"),
               GreedyPlayer("GreedyPlayer2")]
    monopoly = Monopoly(players)
    monopoly.run(100000)
