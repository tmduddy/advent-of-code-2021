from utils.submarine import Submarine

def day2a():
    file_path = 'inputs/day2.csv'
    test_path = 'inputs/tests/day2.csv'

    submarine = Submarine(file_path)
    submarine.run()

def day2b():
    file_path = 'inputs/day2.csv'
    test_path = 'inputs/tests/day2.csv'

    submarine = Submarine(file_path)
    submarine.run()

if __name__ == '__main__':
    # day2a()
    day2b()