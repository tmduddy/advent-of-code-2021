import csv

TEST_PATH = "inputs/tests/day7.csv"
FILE_PATH = "inputs/day7.csv"

def load_data():
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        data = list(map(int, [row for row in reader][0]))
    return data

def day7a():
    print('--- DAY 7A ---')
    data = load_data()
    diff_map = {}
    diffs = []
    for position in range(max(data)):
        diff_map[position] = sum([abs(i-position) for i in data])
        diffs.append(sum([abs(i-position) for i in data]))
        
    # print(diff_map)
    print(min(diffs))

def day7b():
    print('--- DAY 7B ---')
    data = load_data()


if __name__ == '__main__':
    # day7a() # answer = 341558
    day7b() # answer = 
