from monopoly.monopoly import Monopoly
from players.basic_player import BasicPlayer

def run():
    players = [BasicPlayer(), BasicPlayer()]
    monopoly = Monopoly(players)
    monopoly.run_debug()
