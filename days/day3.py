from utils.submarine import Submarine

TEST_PATH = 'inputs/tests/day3.csv'
FILE_PATH = 'inputs/day3.csv'
submarine = Submarine(diagnostic_file_path=FILE_PATH)

def day3a():
    print('--- DAY 3A ---')
    submarine.run_diagnostic(operation='power_consumption')
    

def day3b():
    print('--- DAY 3B ---')
    submarine.run_diagnostic(operation='life_support_rating')


if __name__ == "__main__":
    day3a() # answer = 693486
    day3b() # answer = 3379326