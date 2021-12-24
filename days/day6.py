import csv
from copy import deepcopy

TEST_PATH = "inputs/tests/day6.csv"
FILE_PATH = "inputs/day6.csv"

def day6a():
    print('--- DAY 6A ---')
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        data = list(map(int,[row for row in reader][0]))

    days = 80
    output = deepcopy(data)
    for _ in range(days):
        for i, value in enumerate(data):
            if value == 0:
                output[i] = 6
                output.append(8)
            else:
                output[i] -= 1
        data = deepcopy(output)
        # print(data)
    print(len(data))

def day6b():
    print('--- DAY 6B ---')


if __name__ == '__main__':
    # day6a() # answer = 363101
    day6b() # answer = 
