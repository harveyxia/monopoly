from multiprocessing.pool import ThreadPool

from monopoly.monopoly import Monopoly
from players.cap_rate_player import CapRatePlayer
from players.dumb_player import DumbPlayer

NUM_THREADS = 4

player_type_to_class = {
    "DumbPlayer": DumbPlayer,
    "CapRatePlayer": CapRatePlayer
}


def main(games, turns_per_game, player_types):
    player_names = init_player_names(player_types)
    stats = {player: 0 for player in player_names}

    def run_n_games(num_games):
        for i in xrange(num_games):
            players = init_new_players(player_types, player_names)
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
    return reduce_results(results)


def reduce_results(results):
    stats = results[0]
    for i in range(1, len(results)):
        r = results[i]
        for k, v in r.iteritems():
            stats[k] += v
    return stats


# instantiate a new set of players
def init_new_players(player_types, player_names):
    players = []
    for i in xrange(len(player_types)):
        player_type = player_types[i]
        player_name = player_names[i]
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
