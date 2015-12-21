from monopoly.monopoly import Monopoly
from players.greedy_player import GreedyPlayer


def run(trials):
    players = [GreedyPlayer("BasicPlayer1"),
               GreedyPlayer("BasicPlayer2")]
    monopoly = Monopoly(players)
    move_counts = [0 for i in xrange(trials)]
    player = monopoly.players[0]
    prev_position = 0
    for i in xrange(trials):
        # reset
        prev_position = None
        player.position = 0

        while True:
            # make move
            move_counts[i] += 1
            prev_position = player.position
            if player.in_jail:
                monopoly.attempt_get_out_of_jail(player)
            else:
                monopoly.roll_and_move(player)
            if player.position < prev_position and not player.in_jail:
                # passed Go
                break
    total_moves = 0.0
    for i in xrange(trials):
        total_moves += move_counts[i]
    return (total_moves / trials)

# python -c 'import discount_rate; print discount_rate.run(1000000)'
# 6.205073 moves => 1 year

# how do we calculate an interest rate?
# because it's not dependent on how much we own... you get $200 no matter what
