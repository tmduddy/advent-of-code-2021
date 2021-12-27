from utils.submarine import Submarine
from utils.bingo import BingoPlayer

TEST_PATH = "inputs/tests/day4.csv"
FILE_PATH = "inputs/day4.csv"

submarine = Submarine()
player = BingoPlayer()
player.initialize_game(FILE_PATH)


def day4a():
    print("--- DAY 4A ---")
    # player.play_all(win_type='FIRST')


def day4b():
    print("--- DAY 4B ---")
    player.play_all(win_type="LAST")


if __name__ == "__main__":
    day4a()  # answer = 4662
    day4b()  # answer = 12080
