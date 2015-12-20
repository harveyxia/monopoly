import output
import init
import sys
from players.npv_player import NpvPlayer
from monopoly.monopoly import Monopoly

def simulate(turns, games, discount=.05):
    npvs = init.run(turns, discount)
    
    for _ in range(games):
        players = [NpvPlayer(name="NpvPlayer" + str(i), npvs=npvs) for i in xrange(4)]
        monopoly = Monopoly(players=players)
        monopoly.run(100000)
        npvs = monopoly.get_npvs()
    return npvs

def main():
    if len(sys.argv) > 3:
        npvs = simulate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
        print npvs
    elif len(sys.argv) > 2:
        npvs = simulate(int(sys.argv[1]), int(sys.argv[2]))
        print npvs
    else:
        print "simulate <turns in initial npv calculation> <number of game iterations> [<discount rate>]"
    output.output_npv_file("npv.csv", npvs)

if __name__ == "__main__": main()
