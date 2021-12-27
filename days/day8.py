from utils.submarine import SegmentSub

TEST_PATH = "inputs/tests/day8.csv"
FILE_PATH = "inputs/day8.csv"

submarine = SegmentSub(file_path=FILE_PATH, debug=True)


def day8a():
    print("--- DAY 8A ---")
    submarine.count_easy_digits()


def day8b():
    print("--- DAY 8B ---")
    submarine.run_segments()


if __name__ == "__main__":
    # day8a()  # answer = 387
    day8b()  # answer = 986034

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
