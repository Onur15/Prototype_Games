import time
import random
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
        try:
            game_mode = int(input("Do you want to play with computer?(1=Yes, 0=No)"))
        except ValueError:
            quit("Error")
        if game_mode not in (1,0):
            quit("Error")
        while not self.full():
            if turn:
                print("Player 1's turn.")
                symbol = "X"
            elif not turn and not game_mode:
                print("Player 2's turn.")
                symbol = "O"
            if turn or not game_mode:
                while True:
                    print("0,1,2\n3,4,5\n6,7,8")
                    inp = int(input())
                    if inp in (0,1,2,3,4,5,6,7,8):
                        break
                    else:
                        print("Please select valid area.")
            if not turn and game_mode:
                print("Computer's turn")
                time.sleep(1)
                inp = self.computer()
                symbol = "O"
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
    def computer(self):
        global s
        s = self.board
        if s[0][0]==s[2][2] and s[0][0]!=0 and s[1][1]==0 or s[0][2]==s[2][0] and s[0][2]!=0 and s[1][1]==0:
            return 4
        a,b,c=0,1,2
        for i in range(3):
            for j in range(3):
                if s[i][a]==s[i][b] and s[i][a]!=0 and s[i][c]==0:
                    return i*3 + c
                if s[a][i]==s[b][i] and s[a][i]!=0 and s[c][i]==0:
                    return c*3 + i
                a1,b1,c1=a,b,c
                a=c1
                b=a1
                c=b1
        if s[0][0]==s[2][2] and s[0][0]=="X" or s[0][2]==s[2][0] and s[0][2]=="X":
            if s[0][1]==0 and s[2][1]==0:
                return 1
            if s[1][0]==0 and s[1][2]==0:
                return 5
        sett = set()
        for i in s:
            for j in i:
                sett.add(j)
        if len(sett) == 2 and s[1][1]==0:
            return 4
        while True:
            y = random.randint(0,2)
            x = random.randint(0,2)
            if s[y][x] == 0:
                return 3*y + x
            else:
                continue 
    def full(self):
        value = True
        for y in self.board:
            for x in y:
                if x == 0:
                    value = False
        return value        
    def win_detection(self):
        s = self.board
        for i in range(3):
            if (len({s[i][0], s[i][1], s[i][2]}) == 1) and s[i][0] != 0:
                print(s[i][0], "Wins!")
                return True
        for i in range(3):
            if (len({s[0][i], s[1][i], s[2][i]}) == 1) and s[0][i] != 0:
                print(s[0][i], "Wins!")
                return True
        if ((len({s[0][0], s[1][1], s[2][2]}) == 1) or (len({s[0][2], s[1][1], s[2][0]}) == 1)) and s[1][1] != 0:
            print(s[1][1], "Wins!")
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