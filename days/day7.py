import csv
from tqdm import tqdm

TEST_PATH = "inputs/tests/day7.csv"
FILE_PATH = "inputs/day7.csv"


def load_data():
    with open(FILE_PATH, "r") as f:
        reader = csv.reader(f)
        data = list(map(int, [row for row in reader][0]))
    return data


def get_fuel(index, position, part):
    if part.lower() == "a":
        return abs(index - position)
    elif part.lower() == "b":
        offset = abs(index - position) + 1
        return sum(range(1, offset))
    else:
        raise Exception("invalid day specified")


def day7a():
    print("--- DAY 7A ---")
    data = load_data()
    diff_map = {}
    diffs = []
    for position in range(max(data)):
        diff_step = [get_fuel(i, position, "a") for i in data]
        diff_map[position] = sum(diff_step)
        diffs.append(sum(diff_step))

    # print(diff_map)
    print(min(diffs))


def day7b():
    print("--- DAY 7B ---")
    data = load_data()
    diff_map = {}
    diffs = []
    for position in tqdm(range(max(data))):
        diff_step = [get_fuel(i, position, "b") for i in data]
        diff_map[position] = sum(diff_step)
        diffs.append(sum(diff_step))

    # print(diff_map)
    print(min(diffs))


if __name__ == "__main__":
    # day7a() # answer = 341558
    day7b()  # answer = 93214037
