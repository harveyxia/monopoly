import re
from multiprocessing.pool import ThreadPool

import io_cap
from monopoly.monopoly import Monopoly
from players.cap_rate_player import CapRatePlayer
from players.dumb_player import DumbPlayer
from players.smart_player import SmartPlayer

NUM_THREADS = 4

player_type_to_class = {
    "DumbPlayer": DumbPlayer,
    "SmartPlayer": SmartPlayer,
    "CapRatePlayer": CapRatePlayer
}


def run(games, turns_per_game, teams, cap_rate_file="100cap.csv"):
    caps = io_cap.input_cap_file(cap_rate_file)

    (names, player_to_team) = init_player_names(teams)
    flat_names = [player for team in names for player in team]
    def run_n_games(num_games):
        stats = {player: 0 for player in flat_names}
        for i in xrange(num_games):
            players = init_new_players(teams, names, caps)
            m = Monopoly(players=players)
            m.run(turns_per_game)
            if m.winner:
                stats[m.winner.name] += 1
        return stats

    thread_pool = ThreadPool(processes=NUM_THREADS)
    a = thread_pool.apply_async(run_n_games, (games / 4,))
    b = thread_pool.apply_async(run_n_games, (games / 4,))
    c = thread_pool.apply_async(run_n_games, (games / 4,))
    d = thread_pool.apply_async(run_n_games, (games / 4,))

    results = [a.get(), b.get(), c.get(), d.get()]
    return reduce_results_by_team(results, len(teams), player_to_team)


# returns number of wins per player
def reduce_results_by_player(results):
    stats = results[0]
    for i in range(1, len(results)):
        r = results[i]
        for k, v in r.iteritems():
            stats[k] += v
    return stats


# returns number of wins per player type
def reduce_results_by_player_type(results):
    regex = "^([A-z]+)"
    stats = {}
    for i in range(len(results)):
        r = results[i]
        for k, v in r.iteritems():
            player_type = re.match(regex, k).group(0)
            if player_type not in stats:
                stats[player_type] = v
            else:
                stats[player_type] += v
    return stats


# returns number of wins per player type
def reduce_results_by_team(results, n_teams, player_to_team):
    stats = [0] * n_teams
    for i in range(len(results)):
        r = results[i]
        for k, v in r.iteritems():
            team = player_to_team[k]
            stats[team] += v
    return stats


# instantiate a new set of players
def init_new_players(teams, names, caps):
    players = []
    for i in xrange(len(teams)):
        for j in xrange(len(teams[i])):
            player_type = teams[i][j]
            player_name = names[i][j]
            if player_type == "InitCapRatePlayer":
                init = io_cap.input_cap_file("init.csv")
                players.append(CapRatePlayer(player_name, caps=init))
            elif player_type == "CapRatePlayer":
                players.append(player_type_to_class[player_type](player_name, caps=caps))
            else:
                players.append(player_type_to_class[player_type](player_name))
    return players


# create list of ordered player names according to list of player types
def init_player_names(teams):
    names = []
    player_to_team = {}
    for i in xrange(len(teams)):
        names.append([])
        for j in xrange(len(teams[i])):
            player_name = "Team{0} Player{1}".format(i, j)
            names[i].append(player_name)
            player_to_team[player_name] = i
    return (names, player_to_team)


def run_all_benchmarks(output_filename='simulation_results.txt'):
    a = run(500, 10000, [['DumbPlayer', 'DumbPlayer'], ['SmartPlayer', 'SmartPlayer']])
    b = run(500, 10000, [['DumbPlayer', 'DumbPlayer'], ['CapRatePlayer', 'CapRatePlayer']])
    c = run(500, 10000, [['SmartPlayer', 'SmartPlayer'], ['CapRatePlayer', 'CapRatePlayer']])
    d = run(1500, 10000, [['InitCapRatePlayer', 'InitCapRatePlayer'], ['CapRatePlayer', 'CapRatePlayer']])
    e = run(1500, 10000, [['InitCapRatePlayer', 'InitCapRatePlayer'], ['InitCapRatePlayer', 'InitCapRatePlayer']])
    with open(output_filename, 'w') as f:
        f.write("Scenarios and Results")
        f.write("----------------------------\n")
        f.write("DumbPlayer vs. SmartPlayer = %s:%s\n" % (a[0], a[1]))
        f.write("DumbPlayer vs. CapRatePlayer = %s:%s\n" % (b[0], b[1]))
        f.write("SmartPlayer vs. CapRatePlayer = %s:%s\n" % (c[0], c[1]))
        f.write("InitCapRatePlayer vs. CapRatePlayer = %s:%s\n" % (d[0], d[1]))
        f.write("InitCapRatePlayer vs. InitCapRatePlayer = %s:%s\n" % (e[0], e[1]))

def main():
    run_all_benchmarks()

if __name__ == "__main__": main()
