from os import times_result
from utils.submarine import Submarine

TEST_PATH = "inputs/tests/day5.csv"
FILE_PATH = "inputs/day5.csv"

submarine = Submarine(vent_file_path=FILE_PATH)

def day5a():
    print('--- DAY 5A ---')
    submarine.check_vents(diagonal=False)
    

def day5b():
    print('--- DAY 5B ---')
    submarine.check_vents(diagonal=True)


if __name__ == '__main__':
    # day5a() # answer = 6311
    day5b() # answer = 
