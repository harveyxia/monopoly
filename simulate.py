import output
import init
import sys
from players.cap_rate_player import CapRatePlayer
from monopoly.monopoly import Monopoly

def simulate(turns, games, discount=.05):
    caps = init.simulate("init.csv", turns)
    
    for i in range(games):
        players = [CapRatePlayer(name="CapPlayer" + str(i), caps=caps) for i in xrange(4)]
        monopoly = Monopoly(players=players)
        monopoly.run(100000)
        caps = combine_caps(caps, monopoly.get_caps())
    return caps

def combine_caps(prev, current):
    num_obs = []
    for i in range(len(prev)):
        num_obs.append([0] * 7)
        for j in range(6):
            if current[i][1][j] != 0:
                prev[i][1][j] = (prev[i][1][j]*(num_obs[i][j]) + current[i][1][j])/(num_obs[i][j] + 1)
                num_obs[i][j] += 1
    return prev

def main():
    caps = []
    if len(sys.argv) > 3:
        caps = simulate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
    elif len(sys.argv) > 2:
        caps = simulate(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print "simulate <turns in initial cap calculation> <number of game iterations> [<discount rate>]"
    output.output_cap_file("cap.csv", caps)

if __name__ == "__main__": main()
