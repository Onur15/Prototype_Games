import time
import random
class Game:
    def blank_board(self):#create blank board
        self.size = 3
        board = []
        for i in range(self.size):
            board.append([0] * self.size)
        self.board = board
    def play(self):
        self.blank_board()
        turn = True
        try:
            game_mode = int(input("Do you want to play with computer?(1=Yes, 0=No) "))#game mode
        except ValueError:
            quit("Error")
        if game_mode not in (1,0):
            quit("Error")
        while not self.full():#main game loop
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
            if self.board[select_row][select_column] == 0: #is square full?
                self.board[select_row][select_column] = symbol
                self.print_board()
                if self.win_detection():
                    break
                turn = not turn
            else:
                print("Please select an empty square.", end = "\n\n")
        if self.full(): #Tie
            print("Tie!")
    def computer(self):
        global s
        s = self.board
        a,b,c = 0,1,2
        dict = {0:2, 2:0, 1:1}
        for symbol in ("O", "X"): #first look for win then try to block your opponent
            for i in range(3): #diagonals
                if s[a][a]==s[b][b] and s[a][a]==symbol and s[c][c]==0:
                    return c*3 + c
                if s[a][dict[a]]==s[b][dict[b]] and s[a][dict[a]]==symbol and s[c][dict[c]]==0:    
                    return c*3 + dict[c]
                a1,b1,c1 = a,b,c
                a,b,c = c1,a1,b1 #shift variables
            for i in range(3):
                for j in range(3):
                    if s[i][a]==s[i][b] and s[i][a]==symbol and s[i][c]==0: #rows
                        return i*3 + c
                    if s[a][i]==s[b][i] and s[a][i]==symbol and s[c][i]==0: #columns
                        return c*3 + i
                    a1,b1,c1 = a,b,c
                    a,b,c = c1,a1,b1
        if s[0][0]==s[1][1] and s[0][0]=="X" and s[2][2]=="O" or s[1][1]==s[2][2] and s[1][1]=="X" and s[0][0]=="O": #don't being tricked
            return random.choices((2,6))[0]
        if s[0][2]==s[1][1] and s[0][2]=="X" and s[2][0]=="O" or s[2][0]==s[1][1] and s[2][0]=="X" and s[0][2]=="O":
            return random.choices((0,8))[0]
        if s[0][0]==s[2][2] and s[0][0]=="X" or s[0][2]==s[2][0] and s[0][2]=="X": #if X at opposite corners then place sides 
            if s[0][1]==0 and s[2][1]==0:
                return random.choices((1,7))[0]
            if s[1][0]==0 and s[1][2]==0:
                return random.choices((3,5))[0]
        sett = set()
        for i in s: #place center at start
            for j in i:
                sett.add(j)
        if len(sett) <= 2 and s[1][1]==0:
            return 4
        elif len(sett) <= 2 and s[1][1]!=0: #if center is occupied then place corners
            return random.choices((0,2,6,8))[0]
        while True: #random
            y = random.randint(0,2)
            x = random.randint(0,2)
            if s[y][x] == 0: 
                return 3*y + x
    def full(self): #is broad full?
        value = True
        for y in self.board:
            for x in y:
                if x == 0:
                    value = False
        return value        
    def win_detection(self): #is anyone wins?
        s = self.board
        for i in range(3):
            if (len({s[i][0], s[i][1], s[i][2]}) == 1) and s[i][0] != 0: #win check logic with sets properities
                print(s[i][0], "Wins!")
                return True
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