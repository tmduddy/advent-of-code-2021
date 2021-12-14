#!/bin/zsh

DAY_NUMBER=$1
DATA_FILE_NAME="day${DAY_NUMBER}.csv"
SCRIPT_NAME="day${DAY_NUMBER}.py"

touch inputs/$DATA_FILE_NAME
touch inputs/tests/$DATA_FILE_NAME
touch days/$SCRIPT_NAME

cat <<EOF > days/$SCRIPT_NAME
from utils.submarine import Submarine

TEST_PATH = "inputs/tests/$DATA_FILE_NAME"
FILE_PATH = "inputs/$DATA_FILE_NAME"

submarine = Submarine()

def day${DAY_NUMBER}a():
    print('--- DAY ${DAY_NUMBER}A ---')
    

def day${DAY_NUMBER}b():
    print('--- DAY ${DAY_NUMBER}B ---')


if __name__ == '__main__':
    day${DAY_NUMBER}a() # answer = 
    day${DAY_NUMBER}b() # answer = 
EOF