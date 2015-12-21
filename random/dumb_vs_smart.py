from monopoly.monopoly import Monopoly
from players.dumb_player import DumbPlayer
from players.smart_player import SmartPlayer

players = [SmartPlayer("SmartPlayer"), DumbPlayer("DumbPlayer")]
monopoly = Monopoly(players)
monopoly.run(100000)
