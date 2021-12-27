from utils.submarine import SmokeSub

TEST_PATH = "inputs/tests/day9.csv"
FILE_PATH = "inputs/day9.csv"

submarine = SmokeSub(file_path=FILE_PATH, debug=True)


def day9a():
    print("--- DAY 9A ---")
    submarine.find_low_points()


def day9b():
    print("--- DAY 9B ---")


if __name__ == "__main__":
    # day9a()  # answer = 462
    day9b()  # answer =
