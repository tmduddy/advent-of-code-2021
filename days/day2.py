from utils.submarine import Submarine, MoveSub

FILE_PATH = "inputs/day2.csv"
TEST_PATH = "inputs/tests/day2.csv"


def day2a():
    submarine = MoveSub(file_path=FILE_PATH)
    submarine.run_movement_no_aim()


def day2b():
    submarine = MoveSub(file_path=FILE_PATH)
    submarine.run_movement()


if __name__ == "__main__":
    # day2a()
    day2b()
