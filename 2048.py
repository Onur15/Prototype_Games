import random

class Board:

    # BASIC FUNCTIONS

    # Create empty board with size board_size
    def __init__(self, board_size=4):
        self.size = board_size

        board = []
        for i in range(self.size):
            board.append([0] * self.size)

        self.board = board

    # Edit board
    def set_board(self, board):
        self.board = board

    # Print state of board
    def print_board(self):
        for x in self.board:
            for y in x:
                print(y, end=" ")
            print()
        print()

    # GENERATION & MOVEMENT

    # Generate a 2 on a random empty tile
    def gen_2(self):
        r = random.randint(0, self.size - 1)
        c = random.randint(0, self.size - 1)

        while self.board[r][c] != 0:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)

        self.board[r][c] = 2

    # Utility for rotate_board()
    # Rotate board 90 degrees counterclockwise
    def rotate_90(self):
        for x in range(0, int(self.size / 2)):
            for y in range(x, self.size - x - 1):
                temp = self.board[x][y]
                self.board[x][y] = self.board[y][self.size - 1 - x]
                self.board[y][self.size - 1 - x] = self.board[self.size - 1 - x][self.size - 1 - y]
                self.board[self.size - 1 - x][self.size - 1 - y] = self.board[self.size - 1 - y][x]
                self.board[self.size - 1 - y][x] = temp

    # Rotate board by (num_rotations * 90) degrees counterclockwise
    def rotate_board(self, num_rotations):
        for i in range(num_rotations):
            self.rotate_90()

    # Compress to the left
    def compress(self):
        for i in range(self.size):
            pos = 0
            new_row = [0] * self.size

            for j in range(self.size):
                if self.board[i][j] != 0:
                    new_row[pos] = self.board[i][j]
                    pos += 1

            self.board[i] = new_row

    # Merge to the left
    def merge_left(self):
        for i in range(self.size):
            for j in range(self.size - 1):

                # if they equal each other and not empty
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2
                    self.board[i][j + 1] = 0

    # Main move function: Compress, merge, compress
    def move_left(self):
        self.compress()
        self.merge_left()
        self.compress()

    # Other move functions: Rotate the board, move left, rotate back
    def move_up(self):
        self.rotate_board(1)
        self.move_left()
        self.rotate_board(3)

    def move_right(self):
        self.rotate_board(2)
        self.move_left()
        self.rotate_board(2)

    def move_down(self):
        self.rotate_board(3)
        self.move_left()
        self.rotate_board(1)

    # WIN DETECTION

    # Full board?
    def full(self):
        for x in self.board:
            for y in x:
                if y == 0:
                    return False
        return True

    # Win detection
    def win(self):
        for x in self.board:
            for y in x:
                if y == 2048:
                    return True
        return False


def run_game():
    board = Board()

    # board.set_board([[2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    board.gen_2()

    while True:
        board.print_board()
        previous_board = board.board[:]

        x = input("Your move [wasd]: ")

        if x == 'w':
            board.move_up()
        elif x == 'a':
            board.move_left()
        elif x == 's':
            board.move_down()
        elif x == 'd':
            board.move_right()
        else:
            break

        new_board = board.board[:]

        if board.win():
            print('You win!')
            break

        elif previous_board != new_board:
            if not board.full():
                board.gen_2()


def main():
    run_game()


if __name__ == '__main__':
    main()
