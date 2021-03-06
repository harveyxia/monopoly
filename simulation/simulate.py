import sys

import init
import io_cap
from monopoly.monopoly import Monopoly
from players.cap_rate_player import CapRatePlayer


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
        num_obs.append([0] * 11)
        for j in range(11):
            save = prev[i][1][j]
            if current[i][1][j] != 0:
                if prev[i][1][j] == 0:
                    prev[i][1][j] = current[i][1][j]
                else:
                    prev[i][1][j] = (prev[i][1][j] * (num_obs[i][j]) + current[i][1][j]) / (num_obs[i][j] + 1)
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
    io_cap.output_cap_file("cap.csv", caps)


if __name__ == "__main__": main()
