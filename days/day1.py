import csv

def day1a():
    increase_count = 0
    with open('inputs/day1.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            # skip initial row        
            if i == 0:
                last_row = int(row[0])
                continue
            if int(row[0]) > last_row:
                increase_count += 1
            last_row = int(row[0])
    print(increase_count)


def day2a():
    increase_count = 0
    window_size = 3
    with open('inputs/day1.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        for i, row in enumerate(data):
            current_window = 0
            previous_window = 0
            if i < window_size:
                continue
            for j in range(window_size):
                current_window += int(data[i-j][0])
                previous_window += int(data[i-(j+1)][0])
            if current_window > previous_window:
                increase_count += 1
    print(increase_count)


if __name__ == '__main__':
    # day1a()
    day2a()