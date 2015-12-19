# this file provides us with the bare probabilities of landing on squares
# as well as the average number of turns per year

# run this using python square_npy.py "npv.csv" 100000
# the game basically just runs a game of monopoly where the players don't do
# anything.

import csv

from monopoly.board import Board
from monopoly.monopoly import Monopoly
from players.basic_player import BasicPlayer


def simulate_square_counts(turns):
    players = [BasicPlayer(name="BasicPlayer" + str(i)) for i in xrange(4)]
    monopoly = Monopoly(players=players)
    square_counts = [0 for i in xrange(40)]
    for i in xrange(4 * turns):
        player = monopoly.make_move()
        square_counts[player.position] += 1
    years = monopoly.return_years()
    return (square_counts, years)


def calculate_square_probs(square_counts, years):
    average_length = sum(years) / len(years)
    return map(lambda x: float(x) / average_length, square_counts)


def calculate_npv(square_probs, discount, num_properties=0):
    squares = Board().squares
    npvs = []
    for i in xrange(len(squares)):
        if i in (0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38):   # skip the irrelevant squares
            continue
        square = squares[i]
        square_prob = square_probs[i]
        # return attributes on the squares for sorting and analysis
        npvs.append((square.name, square.color, square.rent[num_properties] * square_prob / (1 - discount) * 4))
    return npvs


def run(turns, discount):
    (square_counts, years) = simulate_square_counts(turns)
    square_probs = calculate_square_probs(square_counts, years)
    npvs = {0: calculate_npv(square_probs, discount),
            1: calculate_npv(square_probs, discount, 1),
            2: calculate_npv(square_probs, discount, 2),
            3: calculate_npv(square_probs, discount, 3),
            4: calculate_npv(square_probs, discount, 4),
            5: calculate_npv(square_probs, discount, 5)}
    return npvs


def output_expected_value_file(filename, npv):
    with open('csv/'+filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'value'])
        writer.writeheader()
        for r in npv:
            writer.writerow({'name': r[0], 'value': r[2]})

def simulate(filename, turns, discount = .05):
    npvs = run(turns, discount)
    output_expected_value_file(filename, npvs[0])

#!/usr/bin/python

import sys

if len(sys.argv) > 3:
    simulate(sys.argv[1], int(float(sys.argv[2])), float(sys.argv[3]))
elif len(sys.argv) > 2:
    simulate(sys.argv[1], int(float(sys.argv[2])))
print "Success"
