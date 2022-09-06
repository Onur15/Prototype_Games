class Game:
    def blank_board(self):
        self.size = 3
        board = []
        for i in range(self.size):
            board.append([0] * self.size)
        self.board = board
    def play(self):
        self.blank_board()
        turn = True
        while not self.full():
            if turn:
                print("Player 1's turn.")
                symbol = "X"
            else:
                print("Player 2's turn.")
                symbol = "O"
            print("0,1,2\n3,4,5\n6,7,8")
            while True:
                inp = int(input())
                if inp in (0,1,2,3,4,5,6,7,8):
                    break
                else:
                    print("Please select valid area.")
            select_column = inp%3
            select_row = inp//3
            if self.board[select_row][select_column] == 0:
                self.board[select_row][select_column] = symbol
                self.print_board()
                if self.win_detection():
                    break
                turn = not turn
            else:
                print("Please select an empty square.", end = "\n\n")
        if self.full():
            print("Tie!")
    def full(self):
        value = True
        for y in self.board:
            for x in y:
                if x == 0:
                    value = False
        return value        
    def win(self, x, y):
        print(self.board[y][x], "Wins!")
    def win_detection(self):
        s = self.board
        for i in range(3):
            if (len({s[i][j], s[i][j+1], s[i][j+2]}) == 1) and s[i][j] != 0:
                self.win(j,i)
                return True
        for j in range(3):
            if (len({s[i][j], s[i+1][j], s[i+2][j]}) == 1) and s[i][j] != 0:
                self.win(j,i)
                return True
        if ((len({s[0][0], s[1][1], s[2][2]}) == 1) or (len({s[0][2], s[1][1], s[2][0]}) == 1)) and s[1][1] != 0:
            self.win(1,1)
            return True
    def print_board(self):
        print()
        for y in self.board:
            for x in y:
                if x == 0:
                    print(" ", end= " ")
                else:
                    print(x, end= " ")
            print()
        print()
board = Game()
board.play()