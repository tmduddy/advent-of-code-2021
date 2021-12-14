from typing import Tuple, List, Dict
import numpy as np
from copy import deepcopy
import csv
from math import ceil

class BingoBoard:
    """
    represents a single "bingo" board, an NxN list of list of ints. 
    a bingo board can process "moves" where a move is a single integer. 
    The board will be searched for that integer and all instances replaced with a -1
    when a board "wins" (that is, 5 -1s appear in any row or column, no diagonals) its score is
    calculated as the sum of the positive numbers still on the board multiplied by the move value
    """
    def __init__(self, board_list: List[List], index, board_size):
        self.raw_board = board_list
        self.int_board = self._raw_list_to_int_board(board_list)
        self.index = index
        self.score = 0
        self.board_size = board_size

    def _raw_list_to_int_board(self, board_list: List) -> List[List[int]]:
        """converts the list provided by the puzzle input into a nicely formatted list of list of ints
        """
        int_board = []
        for row in board_list:
            int_row = [int(i) for i in row[0].split(' ') if i != '']
            int_board.append(int_row)
        return int_board

    def refresh_raw_board(self):
        """
        converts an int_board back into a pretty_printable "raw" board for display purposes
        """
        new_board = []
        for i, row in enumerate(self.int_board):
            new_board.append([])
            for number in row:
                add_string = str(number) if len(str(number)) == 2 else f' {number}'
                new_board[i].append(add_string)
            self.raw_board[i] = [' '.join(new_board[i])]
        
        print(self)

    def process_move(self, move: int, move_number: int) -> int:
        # print(f'{move_number=} :: {move=} :: {self.index=}')
        for i, row in enumerate(self.int_board):
            for j, number in enumerate(row):
                if number == move:
                    self.int_board[i][j] = -1

    def has_won(self) -> bool:
        """
        checks for the win condition
        """
        # check rows
        for row in self.int_board:
            if sum(row) == -5:
                return True
        
        # check columns
        for column in np.transpose(self.int_board):
            if sum(column) == -5:
                return True

        # check both diags (actually the prompt says dont do this, dummy)
        # if sum([self.int_board[i][i] for i in range(self.board_size)]) == -5:
        #     return True
        # if sum([self.int_board[i][self.board_size - (i+1)] for i in range(self.board_size)]) == -5:
        #     return True
        # return False

    def get_score(self, move: int) -> int:
        """
        calculates the score by multiplying the last move by the sum of the positive integers on the board.
        """
        board_score = 0
        for row in self.int_board:
            for num in row:
                board_score += num if num >= 0 else 0
        return board_score * move

    def __repr__(self):
        """pretty prints the board
        """
        output = ''
        for row in self.raw_board:
            output += row[0] + '\n'
        return '\n' + output

class BingoPlayer:
    """a BingoPlayer takes a raw puzzle input and creates a collection of BingoBoards and applies moves to them.
    """

    def __init__(self, board_size=5):
        self.all_boards: Dict[str, BingoBoard] = {}
        self.all_scores: List[Tuple] = []
        self.board_size = board_size

    def initialize_game(self, bingo_file_path: str):
        with open(bingo_file_path, 'r') as f:
            reader = list(csv.reader(f))
            self.moves = [int(i) for i in reader[0]]
            board_lists = [i for i in reader[2:] if len(i) > 0]
        for i in range(len(board_lists)):
            if (i > 0 and i % self.board_size == 0):
                board = board_lists[i-self.board_size:i]
            elif i == len(board_lists) - 1:
                board = board_lists[i-(self.board_size-1):i+1]
            else:
                continue
            index = ceil(i/self.board_size) - 1
            bingo_board = BingoBoard(board_list=board, index=index, board_size=self.board_size)
            self.all_boards[index] = bingo_board
    
    def print_boards(self, index=None):
        if not index:
            for i in self.all_boards:
                print(self.all_boards[i])
        else:
            print(f'{index=}')
            print(self.all_boards.get(index))

    def _handle_win(self, board: BingoBoard, move: int):
        print('----WIN----')
        board.refresh_raw_board()
        print(f'score={board.get_score(move)}')
        print(f'{board.index=}')

    def play_all(self, win_type: str = "FIRST"):
        valid_indices = [i for i in self.all_boards.keys()]
        for i, move in enumerate(self.moves):
            for index, board in self.all_boards.items():
                if index not in valid_indices:
                    continue
                board.process_move(move=move, move_number=i+1)
                # dont check for a win until at least self.board_size - 1 moves have been made
                if (i > self.board_size - 2) and board.has_won():
                    if win_type == 'LAST':
                        valid_indices.remove(index)
                        self.all_scores.append((index, board.get_score(move)))
                        if len(self.all_scores) == len(self.all_boards):
                            self._handle_win(board, move)
                            return
                        continue
                    self._handle_win(board, move)
                    return
