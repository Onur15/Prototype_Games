class Game:
    def blank_board(self):
        self.size = 3
        board = []
        for i in range(self.size):
            board.append([0] * self.size)
        self.board = board
    def play(self):
        self.blank_board()
        turn = "Player_1"
        while not self.full():
            if turn == "Player_1":
                print("Player 1's turn.")
                inp = int(input("0,1,2\n3,4,5\n6,7,8  "))
                select_column = inp%3
                select_row = inp//3
                if self.board[select_row][select_column] == 0:
                    self.board[select_row][select_column] = "X"
                    self.print_board()
                    if self.win_detection():
                        break
                    turn = "Player_2"
                else:
                    print("Please select an empty square.", end = "\n\n")
            if turn == "Player_2" and not self.full():
                print("Player 2's turn.")
                inp = int(input("0,1,2\n3,4,5\n6,7,8\n"))
                select_column = inp%3
                select_row = inp//3
                if self.board[select_row][select_column] == 0:
                    self.board[select_row][select_column] = "O"
                    self.print_board()
                    if self.win_detection():
                        break
                    turn = "Player_1"
                else:
                    print("Please select an empty square.", end="\n\n")
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
        i = j = 0
        s = self.board
        while i <= 2:
            if (len({s[i][j], s[i][j+1], s[i][j+2]}) == 1) and s[i][j] != 0:
                self.win(j,i)
                return True
            else:
                i+=1
        i = j = 0
        while j <= 2:
            if (len({s[i][j], s[i+1][j], s[i+2][j]}) == 1) and s[i][j] != 0:
                self.win(j,i)
                return True
            else:
                j += 1
        i = j = 0
        if ((len({s[i][j], s[i+1][j+1], s[i+2][j+2]}) == 1) or (len({s[i][j+2], s[i+1][j+1], s[i+2][j]}) == 1)) and s[i+1][j+1] != 0:
            self.win(j+1,i+1)
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