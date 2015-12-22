*****************************
*                           *
*           INTRO           *
*                           *
*****************************

THE PROJECT

For our project, we sought to build a monopoly player. Our general goal was to
be able to use some concept of expected returns to decide which properties to
buy. The higher the expected returns, the more likely we should be to buy a
property. Our decision model was thus based on the monte-carlo method.

One of the team members was inspired by this article: “How to Win at Monopoly” 
(http://www.amnesta.net/other/monopoly/). When he saw it, he thought it made 
sense, but wondered if we could beat it by generating more accurate data. So our
specific goal was to beat a player we built that followed the article’s “Best
Strategy” as much as possible.

THE GAME

In Monopoly, you have some number of players (here, 4) and they each take turns
rolling a pair of die, moving around the board, and buying properties. You win
when all the other players go bankrupt. 

The key concept in Monopoly is establishing monopolies. Each property belongs to
a color group. Once you own all the properties within a color group, you have a 
monopoly. Rent on undeveloped property is doubled, and you now have the option
of developing the property by putting houses and hotels on the property,
which dramatically increase the rent.

We originally set out not using the article’s suggestion but NPV instead, since
it would be easier to calculate. However, we quickly realized that is was hard
to compare the NPVs of two different investments. Instead, we decided to go back
to capitalization rates (cap rates), as in the article, to measure the
worthiness of a particular square.

Cap rate is essentially the answer to the question of "what percentage of my 
original investment do I recoup every year?" The great thing about cap rates is
that they let you compare investments of different upfront costs. So something
that costs 50 dollars but returns you 25 dollars a year has a cap rate of 50%.
You can then compare this to an investment of 25 dollars that returns 10 dollars
per year (cap rate 40%). The investment with the higher cap rate wins.

Our strategy for implementation worked in stages:

1) implement basic monopoly
2) generate initial guesses at the cap rates of all the properties
3) implement players that use those cap rates as input to make strategies
4) iterate on those guesses with players to get actual cap rates from games
5) implement players that use the article’s strategy
6) run benchmark tests

As you will later see, our results are pretty successful.

*****************************
*                           *
*           TEAM            *
*                           *
*****************************

Charles Jin / ccj23 / charles.jin@yale.edu
1. Devised strategy for using cap rates
2. Wrote the code that generated initial cap rates
3. Implemented framework for tracking and using cap rates
4. Improved existing Monopoly and Player classes and enforced a consistent 
   interface
5. Added strategy frameworks to general Player class for when decisions were
   needed

Marvin Qian / mbq3 / marvin.qian@yale.edu
1. Implemented iterative cap rate improvement simulation
2. Implemented various strategies for CapRatePlayer
3. Implemented cap rate tracking
4. Implemented various aspects of Monopoly game logic

Frank Wu / fjw22 / frank.j.wu@yale.edu
1. Implemented Monopoly game rules and logic
2. Implemented BenchmarkPlayer and its decision-making strategies
3. Added explanations for Player decisions
4. Implemented Monopoly game state tracking and loading

Harvey Xia / hx52 / harvey.xia@yale.edu
1. Designed and implemented object oriented representation of Monopoly
2. Tested Monopoly implementation
3. Implemented abstract Player class as a way of injecting player strategies
4. Implemented benchmark framework
5. Implemented GreedyPlayer

*****************************
*                           *
*           STRAT           *
*                           *
*****************************

I will talk about our basic strategy for implementation by stage:

1) implement basic monopoly
All the code for this is in monopoly/. We have board.csv which is a file
containing all the information we needed to properly model the game. Board.py
and Square.py model the board and squares, respectively, and are each
responsible only for updating their own state.

Player.py is the class for monopoly players. Basic logic for players went here,
and players implemented their specific strategies in players/.

Monopoly.py was responsible for running the game and keeping the game in a
consistent state. For instance, when monopoly asks a player wants to buy a
house, the player is not responsible for verifying that it, in fact, can buy a
house on that particular square.

2) generate initial guesses at the cap rates of all the properties
First, we ran a bunch of simulations that told gave us the probability of
landing on a particular square. We defined a year to be the amount of time
it takes for a player to go around the board once. We chose this metric because
every time you pass GO, you collect $200 - which seems like a good analog to
inflation.

Then, to get a cap rate, recall the previous discussion about houses and 
hotels being built on monopolized property. We just assume that you have a
monopoly, and then calculate how much money a fully developed piece of property
returns on expectation per year by multiplying by the probability of landing
on the square. The rent is then distributed to each component of the
property (base plus houses/hotels) in proportion to the amount of capital
each component cost. So for instance, if a property + 1 house is expected to
make 100 dollars / year, and the property cost 150 dollars while the house cost
50 dollars, then the property would be attributed 150 / 200 * 100 = 75 dollars
per year, and the house would be attributed 25. We were then able to come up
with a cap rate.

3) implement players that use those cap rates as input to make strategies
The strategies fell in a couple broad categories. For instance, we implemented
one strategy for buying properties that essentially just took the cap rate,
multiplied it by 20, and then used that a a probability that it will execute
the decision. For instance, with a property of cap rate 1%, you would end up
buying the property only 20% of the time. On the other hand, anything with
cap rate >= 5% was immediately bought by the player (if possible).

4) iterate on those guesses with players to get actual cap rates from games
We then played games with 4 players, all using the cap rate approach, and
tracked how long it took a square to recoup its initial investment. This was
meant to get us closer to an actual answer for the cap rates. The hope was that
the more accurate the data, the better the strategy.

5) compare our strategy to some benchmarks
We implemented two main strategies as benchmarks.

GreedyPlayer: The greedy player is the most naive approach to Monopoly, the 
player takes a greedy approach to all of its decisions. This player actually 
performs surprisingly well, and anyone has played monopoly can confirm that 
this strategy is pretty close to optimal. 

1. do_strat_buy_from_bank()
Buys all available houses or hotels.
1. do_strat_unowned_square()
Buys all unowned squares if it has the money.
1. do_strat_raise_money()
        Sell properties and houses/hotels in no particular order to raise money.
1. do_strat_get_out_of_jail()
Always try to roll to get out of jail, regardless of the dangers of moving out 
of jail into owned properties.

BenchmarkPlayer: The benchmark player involves a more complicated decision-
making strategy. The strategy comes from Tim Darling’s “How to Win at Monopoly”
(http://www.amnesta.net/other/monopoly/).

1. do_strat_buy_from_bank()
In the early stages of the game, only buys up to 3 houses, saving money to 
complete a second monopoly. In the later stage of the game, completes hotels and
houses when possible.
1. do_strat_unowned_square()
Buys every railroad and rejects every utility. In the early stages of the game, 
focuses on obtaining a monopoly on sides 1 and 2, prioritizing Orange over 
LightBlue over Pink over Brown. In the late stages of the game, focuses on 
obtaining a monopoly on sides 2 and 3 (Pink, Orange, Red, Yellow, Green, and 
Blue with no particular preference). In all stages of the game, buys properties
to block other players from completing a monopoly.
1. do_strat_raise_money()
Sells non-monopoly properties before breaking up its monopolies. When breaking
up its monopolies, sells houses/hotels in no particular order.
1. do_strat_get_out_of_jail()
In the early game, attempts to leave as soon as possible, unless only St. James
or Tennessee Ave are needed to complete the Orange monopoly, in which case,
stays in jail. Once another player completes a monopoly, attempts to stay in
jail as long as possible.

*****************************
*                           *
*           CODE            *
*                           *
*****************************

We chose an object oriented representation of the game of Monopoly. The entirety
of the game is encapsulated by the Monopoly class. A game consists of a finite
number of moves. The game steps forward by the Monopoly.make_move() method.

A move represents a single player's turn, consisting of the following sequence:
rolling the dice, moving to that square, performing the mandated square action
(paying rent, going to jail, picking a Chance card, etc), and then performing an
action under the player's choice (buying the square, purchasing houses, etc.).

The game ends when all but one player is bankrupt. A player becomes bankrupt
when they cannot raise sufficient funds to perform a mandated square action such
as paying rent or tax.

To aid in performing Monte Carlo simulations, we include the optional parameter
turns to Monopoly(). If this is set, the game will only run for a maximum of the
specified number of turns. If more than 1 player remains at that time, then
there is no winner. Otherwise, the winner is the last player remaining, i.e. who
isn’t bankrupt.

To inject different player strategies, the Player class in player.py is
subclassed and its various abstract methods are implemented. The particular
implementations of these abstract methods determines the logic of that
particular strategy. The abstract methods are:

* do_strat_buy_from_bank()
* do_strat_unowned_square()
* do_strat_raise_money()
* do_strat_get_out_of_jail()
Instances of subclasses of Player are then passed into the instance of
Monopoly(), and the game is then run with those particular player strategies.

Finally, we ran our player against a couple permutations of players of different
sizes and tracked the number of wins per type of player.

*****************************
*                           *
*        HOW TO RUN         *
*                           *
*****************************

$ python simulation/test.py

This runs a single instance of the Monopoly game, demonstrating that our
representation of Monopoly works end-to-end. This run will print statements
detailing the progression of the game, the decisions made, and the winner. By
default, the instance is between a BenchmarkPlayer and a CapRatePlayer.

$ export PYTHONPATH = ‘.’
$ python simulation/simulation.py

This generates the initial cap rates estimates as well as runs the iterative
process for improving the cap rate estimates by playing a bunch of four-player
games with CapRatePlayer.

$ export PYTHONPATH = ‘.’
$ python simulation/benchmark.py

This runs the simulation with results and explains the players’ various
 decisions. The results of the simulation are output to 
 simulation/simulation_results.txt. The abstract Player class supports decision 
 explanations. To view these explanations as the game is simulated and decisions
 are made, set flag in player.py to True. Once the flag is turned on, the player
 will print out a statement explaining why a specific decision was made (based
 on the implemented strategies).

The explanation is produced for each player. A player explains its decision each
time it makes a choice. The explanation is printed immediately following the
action and when relevant, the explanation mentions some state variables of the
game and justifies its decision based on that game state.
Note that which files each function reads from is a hardcoded value, so if you
want to read in the results of simulation to benchmark, you will have to go into
benchmark.py and rename it manually. Sorry!

*****************************
*                           *
*          RESULTS          *
*                           *
*****************************

Interestingly enough, BenchmarkPlayer does not perform too well. 
BenchmarkPlayer’s goal is to establish monopolies, a strategy that gets ruined
when the GreedyPlayer buys every property it can. CapRatePlayer performs the
best, probably striking a happy medium between GreedyPlayer and BenchmarkPlayer,
implementing a similar logic but with slightly more aggressive behavior.

Against GreedyPlayer, BenchmarkPlayer wins 100 times and loses 754 times for a
total of 2000 games (including ties). Against CapRatePlayer, BenchmarkPlayer
wins 104 times but loses 855 times. Finally, CapRatePlayer wins 337 against
GreedyPlayer’s 246.

So CapRatePlayer seems to have a slight edge over GreedyPlayer. As mentioned
earlier, you should most certainly buy almost everything you can. You start out
with way more money than you can spend, so starting early is the key. That means
that aggressive strategies like GreedyPlayer actually fair quite well against
BenchmarkPlayer. However, CapRatePlayer was slightly more discerning with its
choices and so did better than GreedyPlayer.

It seems that we were also easily able to defeat BenchmarkPlayer, fulfilling our
original intent. It is probably a question of human psychology - most humans do
not play as aggressively as GreedyPlayer, so the strategy has evolved for
cautious behavior. We only got here by beating BenchmarkPlayer at its own game -
essentially using its logic, but with more accurate numbers, and training
against itself. It would be interesting if you could write a strategy that was
optimal against all other strategies, rather than just a specific kind.