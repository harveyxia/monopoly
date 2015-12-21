from monopoly.monopoly import Monopoly
from players.dumb_player import DumbPlayer


def run():
    players = [DumbPlayer("DumbPlayer1"),
               DumbPlayer("DumbPlayer2")]
    monopoly = Monopoly(players)
    monopoly.run(100000)
