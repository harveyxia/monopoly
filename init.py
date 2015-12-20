# this file provides us with the bare probabilities of landing on squares
# as well as the average number of turns per year

# run this using python init.py "cap.csv" 60000
# the game basically just runs a game of monopoly where the players don't do
# anything.

from monopoly.board import Board
from monopoly.monopoly import Monopoly
from players.dumb_player import DumbPlayer
import output

############################
#                          #
#       INITIAL STUFF      #
#                          #
############################

def simulate_square_counts(turns):
    players = [DumbPlayer(name="BasicPlayer" + str(i)) for i in xrange(4)]
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

# calculate the cap rate. 
# assumes you buy a square with all hotels immediately
# also assumes no discount rate
def calculate_cap(square_probs):
    squares = Board().squares
    caps = []
    for i in xrange(len(squares)):
        if i in (0, 2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38):   # skip the irrelevant squares
            continue
        square = squares[i]
        square_prob = square_probs[i]
        cap = [0,0,0,0,0,0]
        for num_properties in xrange(6):
            # return attributes on the squares for sorting and analysis
            price = square.price + num_properties * square.price_build
            if square.rent[num_properties] == 0: # for utilities, railroads
                square_rent = 0
            elif num_properties > 0 and square.price_build > 0:
                square_rent = float(square.price_build) / price * square.rent[num_properties]
            else:
                square_rent = float(square.price) / price * square.rent[num_properties]
            cap[num_properties] = (square_rent * square_prob * 3) / price
        caps.append((square.name, cap))
    return caps


def run(turns):
    (square_counts, years) = simulate_square_counts(turns)
    square_probs = calculate_square_probs(square_counts, years)
    return calculate_cap(square_probs)

def simulate(filename, turns):
    caps = run(turns)
    output.output_cap_file(filename, caps)
    return caps

#!/usr/bin/python

import sys

def main():
    if len(sys.argv) > 2:
        simulate(sys.argv[1], int(float(sys.argv[2])))

if __name__ == "__main__": main()
