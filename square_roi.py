# deprecated

# # this file provides us with the bare probabilities of landing on squares
# # as well as the average number of turns per year

# import csv

# from monopoly.board import Board
# from monopoly.monopoly import Monopoly
# from players.basic_player import BasicPlayer


# def simulate_square_counts(turns):
#     """
#     Using Monte Carlo simulation calculate the probability of landing on each square of the board.
#     :param turns: number of turns to run (a turn consists of one move for each player)
#     """
#     players = [BasicPlayer("BasicPlayer" + str(i)) for i in xrange(num_players)]
#     monopoly = Monopoly(players=players)
#     square_counts = [0 for i in xrange(40)]
#     for i in xrange(4 * turns):
#         player = monopoly.make_move()
#         square_counts[player.position] += 1
#     years = monopoly.return_years()
#     return (square_counts, years)


# def calculate_square_probs(square_counts):
#     total = float(sum(square_counts))
#     return map(lambda x: x / total, square_counts)


# def calculate_roi(square_probs, num_properties=0):
#     squares = Board().squares
#     roi = []
#     for i in xrange(len(squares)):
#         if i in (0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38):   # skip the irrelevant squares
#             continue
#         square = squares[i]
#         square_prob = square_probs[i]
#         # return attributes on the squares for sorting and analysis
#         roi.append((square.name, square.color, square.rent[num_properties] * square_prob))
#     return roi


# def run(turns, num_players):
#     square_counts = simulate_square_counts(turns, num_players)
#     square_probs = calculate_square_probs(square_counts)
#     roi = {0: calculate_roi(square_probs),
#            1: calculate_roi(square_probs, 1),
#            2: calculate_roi(square_probs, 2),
#            3: calculate_roi(square_probs, 3),
#            4: calculate_roi(square_probs, 4),
#            5: calculate_roi(square_probs, 5)}
#     return roi


# def output_expected_value_file(filename, roi):
#     with open('csv/'+filename, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=['name', 'value'])
#         writer.writeheader()
#         for r in roi:
#             writer.writerow({'name': r[0], 'value': r[2]})

# def main():
#     print run(100, 2)

# if __name__ == "__main__": main()
