import output
import init
import sys
from players.cap_rate_player import CapRatePlayer
from monopoly.monopoly import Monopoly

def simulate(turns, games, discount=.05):
    npvs = init.simulate("init.csv", turns, discount)
    
    for i in range(games):
        players = [CapRatePlayer(name="NpvPlayer" + str(i), npvs=npvs) for i in xrange(4)]
        monopoly = Monopoly(players=players)
        monopoly.run(100000)
        npvs = combine_npvs(npvs, monopoly.get_npvs(), i+2)
    return npvs

def combine_npvs(prev, current, nGames):
    for i in range(len(prev)):
        for j in range(6):
            if current[i][1][j] != 0:
                prev[i][1][j] = (prev[i][1][j]*(nGames-1) + current[i][1][j])/nGames
    return prev

def main():
    npvs = []
    if len(sys.argv) > 3:
        npvs = simulate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
    elif len(sys.argv) > 2:
        npvs = simulate(int(sys.argv[1]), int(sys.argv[2]))
        print npvs
    else:
        print "simulate <turns in initial npv calculation> <number of game iterations> [<discount rate>]"
    output.output_npv_file("npv.csv", npvs)

if __name__ == "__main__": main()
