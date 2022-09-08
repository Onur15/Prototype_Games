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
        opponent = "Player_2"
        global round
        round = 0
        try:
            game_mode = int(input("Do you want to play with computer?(1=Yes, 0=No) "))#game mode
        except ValueError:
            quit("Error")
        if game_mode not in (1,0):
            quit("Error")
        if game_mode == 1:
            opponent = "Computer"
        try:
            turn = int(input(f"Who plays first Player_1(1) or {opponent}(0) "))
        except ValueError:
            quit("Error")
        if turn not in (1,0):
            quit("Error")
        while not self.full():#main game loop
            if turn:
                print("Player 1's turn:")
                symbol = "X"
            elif not turn and not game_mode:
                print("Player 2's turn:")
                symbol = "O"
            if turn or not game_mode:
                while True:
                    print("0,1,2\n3,4,5\n6,7,8")
                    inp = input()
                    if inp == "exit":
                        exit()
                    if int(inp) in (0,1,2,3,4,5,6,7,8):
                        break
                    else:
                        print("Please select valid area.")
            if not turn and game_mode:
                print("Computer's turn:")
                round += 1
                time.sleep(1)
                inp = self.computer()
                symbol = "O"
            select_column, select_row = int(inp)%3, int(inp)//3
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
        #Tactics
        y1, x1 = 0, 0
        for i in range(4):#if is there two O diagonal complete to triangle shape
            if s[y1][x1] == s[1][1] and s[1][1] == "O":
                crd = self.findbetween(y1, x1, x1, 2-y1)
                if s[x1][2-y1] == 0 and s[crd[0]][crd[1]] == 0:
                    return x1*3 + 2-y1
                elif s[2-x1][y1] == 0:
                    return (2-x1)*3 + y1
            temp = [y1, x1]
            y1, x1 = temp[1], 2-temp[0]
        if s[0][0]==s[1][1] and s[0][0]=="X" and s[2][2]=="O" or s[1][1]==s[2][2] and s[1][1]=="X" and s[0][0]=="O":#1) if 2 X diagonal and third is O place corners
            return random.choices((2,6))[0]
        if s[0][2]==s[1][1] and s[0][2]=="X" and s[2][0]=="O" or s[2][0]==s[1][1] and s[2][0]=="X" and s[0][2]=="O":
            return random.choices((0,8))[0]
        if s[0][0]==s[2][2] and s[0][0]=="X" or s[0][2]==s[2][0] and s[0][2]=="X": #2) if X at opposite corners then place sides 
            if s[0][1]==0 and s[2][1]==0:
                return random.choices((1,7))[0]
            if s[1][0]==0 and s[1][2]==0:
                return random.choices((3,5))[0]
        if s[1][1] == "O":
            y,x = 0,1#X coordinates
            for i in [[0,2],[2,2],[2,0],[0,0]]:#3) if X in neighbor sides place 3 corners around X
                if s[y][x] == s[x][2-y] and s[y][x] == "X" and s[i[1]][2-i[0]] == s[2-i[1]][i[0]] and s[i[0]][i[1]] != "O":
                    return random.choices([i[0]*3 + i[1], i[1]*3 + 2-i[0], (2-i[1])*3 + i[0]])[0]
                y,x = x, 2-y
            y1, x1, y2, x2, j1, k1, j2, k2, j3, k3 = 0, 0, 1, 2, 0, 1, 0, 2, 2, 1#X coordinates and playing spots
            for i in range(4):#4) if X in corner and opposite side edge place correct spots
                if s[y1][x1] == s[y2][x2] and s[y1][x1] == "X" and round >= 2:
                    choice = random.choices([j1*3 + k1, j2*3 + k2, j3*3 + k3])[0]
                    if s[choice//3][choice%3] == 0:
                        return choice
                temp = [y1, x1, y2, x2, j1, k1, j2, k2, j3, k3]
                y1, x1, y2, x2, j1, k1, j2, k2, j3, k3 = temp[1], 2-temp[0], temp[3], 2-temp[2], temp[5], 2-temp[4], temp[7], 2-temp[6], temp[9], 2-temp[8] #rotate clockwise
            if round == 2:
                if s[1][0] == s[1][2] and s[1][0] == "X" or s[0][1] == s[2][1] and s[0][1] == "X":#5) if X opposite sides and O is in the center place corners to win
                    return random.choices([0,2,6,8])[0]
        if round == 1:#place center at start
            if s[1][1]==0:
                return 4
            else: #if center is occupied then place corners
                return random.choices((0,2,6,8))[0]
        if round == 2:
            all = [[1,1]]
            all.append(self.nearsquares(1,1))
            for i in all:
                if s[i[0]][i[1]] == "O":
                    for j in self.nearsquares(i[0], i[1]):
                        if s[j[0]][j[1]] == "X":
                            place = self.find(i[0], i[1], j[0], j[1])
                            return place[0]*3 + place[1] 
        while True:#Random
            y = random.choices((0,1,2))[0]
            x = random.choices((0,1,2))[0]
            print("It is Random")
            if s[y][x] == 0 and self.check(y, x):
                return 3*y + x
    def findbetween(self, y1, x1, y2, x2):
        crd = []
        for i in [[y1,y2],[x1,x2]]:
            if i[0] == i[1]:
                crd.append(i[0])
            else:
                crd.append(max(i)-1)
        return crd
    def check(self, y, x):#return True or False depending on whether X is in the coordinate 
        value = True
        for i in self.nearsquares(y,x):
                if s[i[0]][i[1]] == "O":
                    area = self.find(i[0],i[1],y,x)
                    if s[area[0]][area[1]] == "X": 
                        value = False 
        return value              
    def find(self, y1, x1, y2, x2):#find two points slope and return slope's next coordinate
        coordinate = []
        for i in [[y1,y2],[x1,x2]]:
            if i[0] == i[1]:
                coordinate.append(i[0])
            elif max(i) != 2:
                coordinate.append(max(i)+1)
            else:
                coordinate.append(min(i)-1)
        return coordinate
    def nearsquares(self, y, x):#return adjacent squares coordinates
        areas = []
        for i in range(-1,2):
            for j in range(-1,2):
                if (0 <= y+i <= 2) and (0 <= x+j <= 2) and (y+i,x+j) != (y,x):
                    areas.append([y+i, x+j])
        return areas
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