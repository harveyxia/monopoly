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

### Player Strategy

Player strategies are injected into the system by subclassing `Player` and overriding the abstract methods named
`do_strat_*`. The system calls upon these methods when appropriate.
