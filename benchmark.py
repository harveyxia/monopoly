import re
import io_cap
from multiprocessing.pool import ThreadPool

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


def main(games, turns_per_game, player_types, cap_rate_file="cap.csv"):

    caps = io_cap.input_cap_file(cap_rate_file)

    def run_n_games(num_games):
        player_names = init_player_names(player_types)
        stats = {player: 0 for player in player_names}
        for i in xrange(num_games):
            players = init_new_players(player_types, player_names, caps)
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
    return reduce_results_by_player_type(results)


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


# instantiate a new set of players
def init_new_players(player_types, player_names, caps):
    players = []
    for i in xrange(len(player_types)):
        player_type = player_types[i]
        player_name = player_names[i]
        if player_type == "CapRatePlayer":
            players.append(player_type_to_class[player_type](player_name, caps=caps))
        else:
            players.append(player_type_to_class[player_type](player_name))
    return players


# create list of ordered player names according to list of player types
def init_player_names(player_types):
    player_type_counts = {}
    player_names = []
    for player_type in player_types:
        if player_type not in player_type_counts:
            player_type_counts[player_type] = 1
        else:
            player_type_counts[player_type] += 1
        player_names.append(player_type + str(player_type_counts[player_type]))
    return player_names
