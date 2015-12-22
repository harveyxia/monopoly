import io_cap
from monopoly.monopoly import Monopoly
from players.benchmark_player import BenchmarkPlayer
from players.cap_rate_player import CapRatePlayer


def main():
    caps = io_cap.input_cap_file("100cap.csv")
    players = [BenchmarkPlayer(name="BenchmarkPlayer1"),
               CapRatePlayer(name="CapRatePlayer1", caps=caps)]
    m = Monopoly(players=players, debug_flag=True)
    m.run(10000)


if __name__ == "__main__": main()
