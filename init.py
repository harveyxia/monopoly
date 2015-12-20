# this file provides us with the bare probabilities of landing on squares
# as well as the average number of turns per year

# run this using python init.py "npv.csv" 60000
# the game basically just runs a game of monopoly where the players don't do
# anything.

from monopoly.board import Board
from monopoly.monopoly import Monopoly
from players.basic_player import BasicPlayer
import output

############################
#                          #
#       INITIAL STUFF      #
#                          #
############################

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


def calculate_npv(square_probs, discount):
    squares = Board().squares
    npvs = []
    for i in xrange(len(squares)):
        if i in (0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38):   # skip the irrelevant squares
            continue
        square = squares[i]
        square_prob = square_probs[i]
        npv = [0,0,0,0,0,0]
        for num_properties in xrange(6):
            # return attributes on the squares for sorting and analysis
            # if num_properties > 0:
            #     square_rent = float(square.price_build) / (square.price + square.price_build * num_properties) * square.rent[num_properties]
            # else:
            #     square_rent = float(square.price) / (square.price + square.price_build * num_properties) * square.rent[num_properties]
            
            if square.rent[5] == 0: # for utilities, railroads
                square_rent = square.rent[num_properties]
            elif num_properties > 0 and square.price_build > 0:
                square_rent = float(square.price_build) / (square.price + square.price_build * 5) * square.rent[5]
            else:
                square_rent = float(square.price) / (square.price + square.price_build * 5) * square.rent[5]
            npv[num_properties] = square_rent * square_prob / (1 - discount) * 3
        npvs.append((square.name, npv))
    return npvs


def run(turns, discount=.05):
    (square_counts, years) = simulate_square_counts(turns)
    square_probs = calculate_square_probs(square_counts, years)
    return calculate_npv(square_probs, discount)

def simulate(filename, turns, discount=.05):
    npvs = run(turns, discount)
    output.output_npv_file(filename, npvs)
    return npvs

#!/usr/bin/python

import sys

def main():
    if len(sys.argv) > 3:
        simulate(sys.argv[1], int(float(sys.argv[2])), float(sys.argv[3]))
    elif len(sys.argv) > 2:
        simulate(sys.argv[1], int(float(sys.argv[2])))

if __name__ == "__main__": main()
