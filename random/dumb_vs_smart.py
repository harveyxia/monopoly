from monopoly.board import Board
from monopoly.monopoly import Monopoly
from players.smart_player import SmartPlayer
from players.dumb_player import DumbPlayer


players = [SmartPlayer("SmartPlayer"), DumbPlayer("DumbPlayer")]
monopoly = Monopoly(players)
monopoly.run(100000)