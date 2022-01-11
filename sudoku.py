import copy
import sys
import time
class Sudoku:
    def __init__(self, clues):
        self.clues = clues
        self.board = copy.deepcopy(clues)
        self.pointer = [0, 0]
    
    # Checks whether a list of integers has duplicates. Only checks for numbers 1-9
    # lst: list of integers
    def check_valid_lst(self, lst):
        for element in lst:
            assert 0 <= element and element < 10
            if element == 0:
                continue
            else:
                if lst.count(element) > 1:
                    return False
        return True

    # Checks the row, column, and block that the pointer is currently pointing to and see if it violates any of the Sudoku rules.
    def check_valid(self):
        row = self.pointer[0]
        col = self.pointer[1]
        boardrow = self.board[row]
        boardcol = self.get_column()
        boardblock = self.get_block()
        return self.check_valid_lst(boardrow) and self.check_valid_lst(boardcol) and self.check_valid_lst(boardblock)
    
    def check_whole_board(self):
        rows = self.get_rows()
        cols = self.get_columns()
        blocks = self.get_blocks()
        for row in rows:
            if self.check_valid_lst(row) is False:
                return False
        for col in cols:
            if self.check_valid_lst(col) is False:
                return False
        for block in blocks:
            if self.check_valid_lst(block) is False:
                return False
        return True
        
    # Returns a list containing the numbers from the block that the pointer is currently pointing to.
    def get_block(self):
        row = self.pointer[0]
        col = self.pointer[1]
        blocks = self.get_blocks()
        block = []
        if 0 <= row and row <= 2:
            if 0 <= col and col <= 2:
                block = blocks[0]
            elif 3 <= col and col <= 5:
                block = blocks[1]
            elif 6 <= col and col <= 8:
                block = blocks[2]
        elif 3 <= row and row <= 5:
            if 0 <= col and col <= 2:
                block = blocks[3]
            elif 3 <= col and col <= 5:
                block = blocks[4]
            elif 6 <= col and col <= 8:
                block = blocks[5]
        elif 6 <= row and row <= 8:
            if 0 <= col and col <= 2:
                block = blocks[6]
            elif 3 <= col and col <= 5:
                block = blocks[7]
            elif 6 <= col and col <= 8:
                block = blocks[8]
        return block
    
    # Returns a list containing all the numbers from all the blocks.
    # From https://stackoverflow.com/questions/21270501/how-to-create-lists-of-3x3-sudoku-block-in-python by Code_Buddy9000
    def get_blocks(self):
        blocks = []
        for i in range(9):
            if i == 0 or i % 3 == 0:
                block_set_1 = self.board[i][:3] + self.board[i + 1][:3] + self.board[i + 2][:3]
                blocks.append(block_set_1)
                block_set_2 = self.board[i][3:6] + self.board[i + 1][3:6] + self.board[i + 2][3:6]
                blocks.append(block_set_2)
                block_set_3 = self.board[i][6:] + self.board[i + 1][6:] + self.board[i + 2][6:]
                blocks.append(block_set_3)
        return blocks
    
    # Returns a list containing the numbers from the column that the pointer is currently pointing to.
    def get_column(self):
        column = []
        col = self.pointer[1]
        for row in self.board:
            column.append(row[col])
        return column

    # Returns a list of all columns.
    def get_columns(self):
        original_row = self.pointer[0]
        original_col = self.pointer[1]
        self.pointer[0] = 0
        self.pointer[1] = 0
        columns = []
        for col in range(9):
            columns.append(self.get_column())
            self.point_next()
        self.pointer[0] = original_row
        self.pointer[1] = original_col
        return columns

    # Returns a list of all rows.
    def get_rows(self):
        return self.board
    # Modifies the number in the position that the pointer is currently pointing to with num.
    # num: integer
    def modify_position(self, num):
        self.board[self.pointer[0]][self.pointer[1]] = num
    
    # Checks whether the position the pointer is currently pointing to is a part of the clues. Returns True or False.
    def check_in_clues(self):
        if self.clues[self.pointer[0]][self.pointer[1]] == 0:
            return False
        else:
            return True
    
    # Returns the number that the pointer is currently pointing to.
    def get_position(self):
        return self.board[self.pointer[0]][self.pointer[1]]
    
    # Moves the pointer to the next position. Returns True if successful and False if not.
    def point_next(self):
        if self.pointer[0] == 8 and self.pointer[1] == 8:
            return False
        elif self.pointer[1] == 8:
            self.pointer[0] = self.pointer[0] + 1
            self.pointer[1] = 0
            return True
        else:
            self.pointer[1] = self.pointer[1] + 1
            return True
    
    # Moves the pointer to the previous position. Returns True if successful and False if not.
    def point_prev(self):
        if self.pointer[0] == 0 and self.pointer[1] == 0:
            return False
        elif self.pointer[1] == 0:
            self.pointer[0] = self.pointer[0] - 1
            self.pointer[1] = 8
            return True
        else:
            self.pointer[1] = self.pointer[1] - 1
            return True
    
    # Prints out a Sudoku board
    # From https://stackoverflow.com/questions/37952851/formating-sudoku-grids-python-3 by Blckknght
    def print_sudoku(self):
        print("-"*37)
        for i, row in enumerate(self.board):
            print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
            if i == 8:
                print("-"*37)
            elif i % 3 == 2:
                print("|" + "---+"*8 + "---|")
            else:
                print("|" + "   +"*8 + "   |")

    # Solves the Sudoku. Returns True if successful and False if not.
    def solve_sudoku(self):
        self.pointer[0] = 0
        self.pointer[1] = 0
        while True:
            # self.print_sudoku()
            if self.check_in_clues() is False:
                pointed_element = self.get_position()
                if pointed_element == 9:
                    self.modify_position(0)
                    point_result = self.point_prev()
                    if point_result is False:
                        return False
                    while self.check_in_clues() is True:
                        point_result = self.point_prev()
                        if point_result is False:
                            return False
                    continue
                else:
                    self.modify_position(pointed_element + 1)
                    if self.check_valid() is True:
                        point_result = self.point_next()
                        if point_result is False:
                            return True
                        continue
            else:
                point_result = self.point_next()
                if point_result is False:
                    return True
                continue






if __name__ == '__main__':
    board1 = [ #easy
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]

    board2 = [ #easy
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ]

    board3 = [ #intermediate
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0]
    ]

    board4 = [ #very hard
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 3],
        [0, 7, 4, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 2],
        [0, 8, 0, 0, 4, 0, 0, 1, 0],
        [6, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 7, 8, 0],
        [5, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 4, 0]
    ]
    board5 = [ #hardest
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ]
    board6 = [ #hardest
        [5, 0, 6, 9, 0, 8, 0, 0, 1],
        [1, 4, 8, 0, 3, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 9, 5, 0],
        [0, 5, 0, 2, 0, 3, 0, 6, 0],
        [0, 6, 3, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 2, 0, 1, 3, 9],
        [3, 0, 0, 7, 0, 9, 4, 0, 6]
    ]
    board7 = [ # takes an hour
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ]

    game1 = Sudoku(board1)
    game2 = Sudoku(board2)
    game3 = Sudoku(board3)
    game4 = Sudoku(board4)
    game5 = Sudoku(board5)
    game6 = Sudoku(board6)
    game7 = Sudoku(board7)

    
    print("Please enter your own Sudoku. Please enter row by row, followed by an enter key. Empty spots please enter 0. For example, to enter the first row of the following board:")
    game1.print_sudoku()
    print("Enter the following sequence:")
    print("0, 0, 0, 2, 6, 0, 7, 0, 1")
    print("Then press enter, and repeat the above step for all rows.")
    while True:
        rows = []
        for i in range(9):
            if i == 0:
                print("Enter the 1st row:")
            elif i == 1:
                print("Enter the 2nd row:")
            elif i == 2:
                print("Enter the 3rd row:")
            else:
                print(f"Enter the {i + 1}th row:")
            row = input()
            row = row.split(", ")
            row = [int(x) for x in row]
            rows.append(row)
        game = Sudoku(rows)
        if game.check_whole_board() is True:
            break
        else:
            print("Board is invalid! Try again.")
    print("This is the board that you entered:")
    game.print_sudoku()
    print("Solving...")
    game.solve_sudoku()
    print("Done!")
    game.print_sudoku()
