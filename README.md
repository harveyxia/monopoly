## Monopoly Automated Decision System

Use Monte Carlo simulations and rule-based systems for an optimal Monopoly gameplay strategy.

## Implementation

### The Game

The entirety of the game is encapsulated by the `Monopoly` class. A game consists of a finite number of **moves**. The
game steps forward by the `Monopoly.make_move()` method.

A move represents a single player's turn, consisting of the following sequence: rolling the dice, moving to that
square, performing the mandated square action (paying rent, going to jail, picking a Chance card, etc), and then
performing an action under the player's choice (buying the square, purchasing houses, etc.).

The game ends when all but one player is *bankrupt.* A player becomes bankrupt when they cannot raise sufficient funds
to perform a mandated square action such as paying rent or tax.

To aid in performing Monte Carlo simulations, we include the optional parameter `max_money` to `Monopoly()`. If this is
set, the bank will only issue up to `max_money` in $200 for players passing GO.

### Player Strategy

Player strategies are injected into the system by subclassing `Player` and overriding the abstract methods named
`do_strat_*`. The system calls upon these methods when appropriate.

## Monte Carlo Simulations

Step 1: Calculating the return on investment for each square

The script `square_roi.py` contains logic for calculating the return on investment for each square. First it runs a
simple simulation consisting of each player merely rolling die and moving around the board. Each position is recorded
in a histogram. A typical run of 1000 turns with 4 players each looks like the following:

Square Name                         | Count
---------------------------------   | ------
Go                                  |  83
Mediterranean Avenue                |  80
Community Chest                     |  86
Baltic Avenue                       |  88
Income Tax                          |  107
Reading Railroad                    |  81
Oriental Avenue                     |  93
Chance                              |  89
Vermont Avenue                      |  78
Connecticut Avenue                  |  99
Jail                                |  383
St. Charles Place                   |  89
Electric Company                    |  90
States Avenue                       |  91
Virginia Avenue                     |  92
Pennsylvania Railroad               |  96
St. James Place                     |  121
Community Chest                     |  90
Tennessee Avenue                    |  105
New York Avenue                     |  102
Free Parking                        |  93
Kentucky Avenue                     |  104
Chance                              |  79
Indiana Avenue                      |  102
Illinois Avenue                     |  80
B. & O. Railroad                    |  93
Atlantic Avenue                     |  104
Ventnor Avenue                      |  92
Water Works                         |  93
Marvin Gardens                      |  98
Go To Jail                          |  93
Pacific Avenue                      |  91
North Carolina Avenue               |  78
Community Chest                     |  93
Pennsylvania Avenue                 |  82
Short Line                          |  92
Chance                              |  83
Park Place                          |  116
Luxury Tax                          |  96
Boardwalk                           |  9

Then the probabilities for each square are calculated by dividing the counts by the total number of moves (players *
turns). For 1000 turns and 4 players, a typical run looks like this:

Square Name                         | Probability
---------------------------------   | ------
Go                                  |   0.02075
Mediterranean Avenue                |   0.02
Community Chest                     |   0.0215
Baltic Avenue                       |   0.022
Income Tax                          |   0.02675
Reading Railroad                    |   0.02025
Oriental Avenue                     |   0.02325
Chance                              |   0.02225
Vermont Avenue                      |   0.0195
Connecticut Avenue                  |   0.02475
Jail                                |   0.09575
St. Charles Place                   |   0.02225
Electric Company                    |   0.0225
States Avenue                       |   0.02275
Virginia Avenue                     |   0.023
Pennsylvania Railroad               |   0.024
St. James Place                     |   0.03025
Community Chest                     |   0.0225
Tennessee Avenue                    |   0.02625
New York Avenue                     |   0.0255
Free Parking                        |   0.02325
Kentucky Avenue                     |   0.026
Chance                              |   0.01975
Indiana Avenue                      |   0.0255
Illinois Avenue                     |   0.02
B. & O. Railroad                    |   0.02325
Atlantic Avenue                     |   0.026
Ventnor Avenue                      |   0.023
Water Works                         |   0.02325
Marvin Gardens                      |   0.0245
Go To Jail                          |   0.02325
Pacific Avenue                      |   0.02275
North Carolina Avenue               |   0.0195
Community Chest                     |   0.02325
Pennsylvania Avenue                 |   0.0205
Short Line                          |   0.023
Chance                              |   0.02075
Park Place                          |   0.029
Luxury Tax                          |   0.024
Boardwalk                           |   0.02375

Finally, the expected value of each square is calculated by multiplying its probability of a player landing on it by
its rent price. This is done for a property with no houses, 1 house, 2 houses, 3 houses, 4 houses, and a hotel (5
 houses). A run with 1000 turns and 4 players typically yields the following result for squares without houses, sorted 
 descending on expected value:

Square Name                         | Expected Value
---------------------------------   | ------
Boardwalk                                  |   1.05
Park Place                |   0.7175
Pacific Avenue                     |   0.6695
B. & O. Railroad                       |   0.66875
Short Line                          |   0.65625
Pennsylvania Avenue                    |   0.616
Reading Railroad                     |   0.6
Ventnor Avenue                              |   0.5775
Pennsylvania Railroad                      |   0.55625
Marvin Gardens                  |   0.528
Atlantic Avenue                                |   0.5115
North Carolina Avenue                   |   0.4875
Illinois Avenue                    |   0.43499999999999994
Kentucky Avenue                       |   0.4095
New York Avenue                     |   0.404
Indiana Avenue               |   0.3645
Tennessee Avenue                     |   0.35350000000000004
St. James Place                     |   0.34650000000000003
Virginia Avenue                    |   0.273
St. Charles Place                     |   0.21999999999999997
States Avenue                        |   0.21499999999999997
Connecticut Avenue                     |   0.198
Vermont Avenue                              |   0.11399999999999999
Oriental Avenue                      |   0.10799999999999998
Electric Company                     |   0.094
Baltic Avenue                    |   0.086
Water Works                     |   0.084
Mediterranean Avenue                      |   0.0435
Go                         |   0.0
Community Chest                      |   0.0
Income Tax                          |   0.0
Chance                      |   0.0
Jail               |   0.0
Community Chest                     |   0.0
Free Parking                 |   0.0
Chance                          |   0.0
Go To Jail                              |   0.0
Community Chest                          |   0.0
Chance                          |   0.0
Luxury Tax                           |   0.0

1. For each square, calculate the expected value of any player landing on such a square (# times player lands on square
/ total number of years, a year defined as passing Go). Calculate the NPV of the square by taking its rent and
multiplying by its expected value. Discount rate is due to receiving $200 when passing Go.
