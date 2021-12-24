import csv
from copy import deepcopy

TEST_PATH = "inputs/tests/day6.csv"
FILE_PATH = "inputs/day6.csv"

def load_data():
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        data = list(map(int,[row for row in reader][0]))
    return data

def day6a():
    print('--- DAY 6A ---')
    data = load_data()
    data = [0]

    days = 156
    output = deepcopy(data)
    print(f'day 0: {output}')
    for day in range(days):
        for i, value in enumerate(data):
            if value == 0:
                output[i] = 6
                output.append(8)
            else:
                output[i] -= 1
        data = deepcopy(output)
        # print(f'day {day+1}: {data}')
        print(f'day {day+1}: {len(data)}')
    print(len(data))

def day6b():
    print('--- DAY 6B ---')
    days = 256
    data = load_data()
    fish = [data.count(i) for i in range(9)]
    
    for _ in range(days):
        num = fish.pop(0)
        fish[6] += num
        fish.append(num)
    
    print(sum(fish))


if __name__ == '__main__':
    # day6a() # answer = 363101
    day6b() # answer = 1644286074024
