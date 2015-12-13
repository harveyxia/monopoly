from monopoly.monopoly import Monopoly
from monopoly.board import Board


def simulate_square_counts(turns, num_players):
    """
    Using Monte Carlo simulation calculate the probability of landing on each square of the board.
    :param num_players: number of players
    :param turns: number of turns to run (a turn consists of one move for each player)
    """
    monopoly = Monopoly(num_players=num_players)
    square_counts = [0 for i in xrange(40)]
    for i in xrange(num_players * turns):
        player = monopoly.make_move()
        square_counts[player.position] += 1
    return square_counts


def calculate_square_probs(square_counts):
    total = float(sum(square_counts))
    return map(lambda x: x/total, square_counts)


def calculate_roi(square_probs, num_properties=0):
    if num_properties > 5:
        raise Exception("%s exceeds max properties of 5." % str(num_properties))
    squares = Board().squares
    roi = []
    for i in xrange(len(squares)):
        square = squares[i]
        square_prob = square_probs[i]
        # return attributes on the squares for sorting and analysis
        roi.append((square.name, square.color, square.rent[num_properties]*square_prob))
    return roi


def run(turns, num_players):
    square_counts = simulate_square_counts(turns, num_players)
    square_probs = calculate_square_probs(square_counts)
    roi = {0: calculate_roi(square_probs),
           1: calculate_roi(square_probs, 1),
           2: calculate_roi(square_probs, 2),
           3: calculate_roi(square_probs, 3),
           4: calculate_roi(square_probs, 4),
           5: calculate_roi(square_probs, 5)}
    return roi
