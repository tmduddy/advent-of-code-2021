from utils.submarine import SegmentSub

TEST_PATH = "inputs/tests/day8.csv"
FILE_PATH = "inputs/day8.csv"

submarine = SegmentSub(file_path=FILE_PATH, debug=False)


def day8a():
    print("--- DAY 8A ---")
    submarine.run_segments()


def day8b():
    print("--- DAY 8B ---")


if __name__ == "__main__":
    # day8a()  # answer = 387
    day8b()  # answer =
