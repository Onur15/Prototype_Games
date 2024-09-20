from random import randint
class Game():
    
    def __init__(self):
        self.over = False
        self.table = []
        self.hit = {"0": 0, "1": 0}
        self.scores = {"0": 0, "1": 0}
        self.settings = {"Display Orientation": "left", "Display On": True, "Show Hits": True, "Show Scores": True ,"Probabilities Respect To Player": 2}
        
    def reset_table(self):
        tb = self.table
        self.scores = {"0": 208, "1": 208}
        for i in range(24):
            tb.append({"player": 0,"count": 0})
        for i in (0,1):
            sign = (-1)**i
            tb[sign*0-i] = {"player" : 1+i, "count" : 2}
            tb[sign*11-i] = {"player" : 1+i, "count" : 5}
            tb[sign*16-i] = {"player" : 1+i, "count" : 3}
            tb[sign*18-i] = {"player" : 1+i, "count" : 5}
        if self.settings["Display On"]: self.display_table()
            
    def display_table(self):
        tb = self.table
        rows1 = []
        rows2 = []
        probs = list(self.calc_prob(self.settings["Probabilities Respect To Player"]).values())
        probs = [i if len(i) == 5 else i+" " for i in probs]
        if self.settings["Display Orientation"] == "left":
            print(" ".join(probs[0:6]),end=" || ")
            print(" ".join(probs[6:12]))
        if self.settings["Display Orientation"] == "right":
            print(" ".join(probs[11:5:-1]),end=" || ")
            print(" ".join(probs[0:6][::-1]))
        for index, rows in enumerate([rows1,rows2]):
            i = 0
            while True:
                row = []
                symbols = {1: "O", 2: "@"}
                j = 0
                if index == 0:
                    rg = range(12)
                if index == 1:
                    rg = range(12,24)
                for col in rg:
                    if col == 18:
                        row.append("||")
                    if col == 6:
                        row[col-1] += "   ||"
                    if tb[col]["count"] > i:
                        if col == 18:
                            row[col-12] += "   "+symbols[tb[col]["player"]]
                            row[col-12] = row[col-12][::-1]
                            continue
                        if col == 6:
                            row[col-1] += "   "+symbols[tb[col]["player"]]
                            continue
                        row.append(symbols[tb[col]["player"]])
                    if tb[col]["count"] <= i:
                        if col == 18:
                            row[col-12] += "    "
                            row[col-12] = row[col-12][::-1]
                            continue
                        if col == 6:
                            row[col-1] += "    "
                            continue
                        row.append(" ")
                        j += 1
                rows.append(row)
                # print(row)
                i += 1
                if j == 11:
                    if self.settings["Display Orientation"] == "left":
                        if rows == rows1:
                            for row in rows:
                                print("  "+"     ".join(row))
                            print()
                        if rows == rows2:
                            rows = rows[::-1]
                            for row in rows:
                                row = row[::-1]
                                row[5] = row[5]+"   "+row[6]
                                del row[6]
                                print("  "+"     ".join(row))
                            print(" ".join(probs[23:17:-1]),end=" || ")
                            print(" ".join(probs[17:11:-1]))
                    if self.settings["Display Orientation"] == "right":
                        if rows == rows1:
                            for row in rows:
                                row = row[::-1]
                                row[5] = row[5][::-1]
                                print("  "+"     ".join(row))
                            print()
                        if rows == rows2:
                            rows = rows[::-1]
                            for row in rows:
                                row[6] = row[6][::-1]
                                row[6] = row[5]+"   "+row[6]
                                del row[5]                                
                                print("  "+"     ".join(row))
                            print(" ".join(probs[12:18]),end=" || ")
                            print(" ".join(probs[18:24]))
                    j = 0
                    break
        if self.settings["Show Hits"]: print(f"Broken Pieces:  player1: {self.hit['0']}    player2: {self.hit['1']}")
        if self.settings["Show Scores"]: print(f"       Scores:  player1: {self.scores['0']}  player2: {self.scores['1']}")
        print("\n")
        
    def check_all_in(self, player):
        tb = self.table
        if self.hit[str(player-1)] != 0: return -1
        positions = set()
        for point in range(24):
            pc = tb[point]
            if pc["player"] == player and pc["count"] > 0:
                positions.add(point)
        if player == 1: p = {23,22,21,20,19,18}
        if player == 2: p = {0,1,2,3,4,5}
        if positions.issubset(p):
            return 1
        
    def move(self, x1, x2):
        tb = self.table
        pc1 = tb[x1]
        if pc1["player"] == 0 or pc1["count"] == 0:
            return -1
        if x2 < 0 or x2 > 23:
            if self.check_all_in(pc1["player"]) != 1:
                return -1
            pc1["count"] -= 1
            self.scores[str(pc1["player"]-1)] += abs(x1+1+25*(pc1["player"]-2))
            if self.settings["Display On"]: self.display_table()
            if self.scores[str(pc1["player"]-1)] == 375:
                self.over = True
            return 1
        if not(x1 in range(24)) or not(x2 in range(24)):
            return -1
        pc2 = tb[x2]
        if self.hit[str(pc1["player"]-1)] != 0:
            return -1
        if (pc1["player"] == 1 and x1 >= x2) or (pc1["player"] == 2 and x1 <= x2):
            return -1
        if pc1["player"] == pc2["player"] or pc2["player"] == 0:
            pc1["count"] -= 1
            pc2["count"] += 1
            pc2["player"] = pc1["player"]
            self.scores[str(pc1["player"]-1)] += abs(x2-x1)
        elif pc1["player"] != pc2["player"]:
            if pc2["count"] > 1:
                return -1
            elif pc2["count"] == 1:
                self.hit[str(pc2["player"]-1)] += 1
                self.scores[str(pc2["player"]-1)] -= abs(x2+1-25*(pc2["player"]-1))
                pc1["count"] -= 1
                pc2["player"] = pc1["player"]
                self.scores[str(pc1["player"]-1)] += abs(x2-x1)
            elif pc2["count"] == 0:
                pc1["count"] -= 1
                pc2["count"] += 1
                pc2["player"] = pc1["player"]
                self.scores[str(pc1["player"]-1)] += abs(x2-x1)
        if self.settings["Display On"]: self.display_table()
            
    def place(self, player, x):
        tb = self.table
        placeAt = x
        if x < 1 or x > 6: return -1
        if not(player in ("player1","player2")):
            return -1
        if player == "player1": 
            player = 1
            x -= 1
        if player == "player2":
            player = 2
            x = 24-x
        pc = tb[x]
        if pc["player"] == player or pc["player"] == 0:
            pc["count"] += 1
            pc["player"] = player
            self.hit[str(player-1)] -= 1
            self.scores[str(player-1)] += placeAt
        elif pc["player"] != player:
            if pc["count"] > 1:
                return -1
            elif pc["count"] == 1:
                self.hit[str(pc["player"]-1)] += 1
                self.scores[str(pc["player"]-1)] -= 25-placeAt
                self.hit[str(player-1)] -= 1
                self.scores[str(player-1)] += placeAt
                pc["player"] = player
            elif pc["count"] == 0:
                self.hit[str(player-1)] -= 1
                self.scores[str(player-1)] += placeAt
                pc["count"] += 1
                pc["player"] = player
        if self.settings["Display On"]: self.display_table()
            
    def calc_prob(self, player):
        tb = self.table
        lookup = {
            1 : {},
            2 : {"(1,1)":1},
            3 : {"(1,1)":1, "(1,2)":2},
            4 : {"(1,1)":1, "(1,3)":2, "(2,2)": 1},
            5 : {"(1,4)":2, "(2,3)":2},
            6 : {"(1,5)":2, "(2,2)":1, "(2,4)":2, "(3,3)":1},
            7 : {"(1,6)":2, "(2,5)":2, "(3,4)":2},
            8 : {"(2,2)":1, "(2,6)":2, "(3,5)":2, "(4,4)":1},
            9 : {"(3,3)":1, "(3,6)":2, "(4,5)":2},
            10 : {"(4,6)":2, "(5,5)":1},
            11 : {"(5,6)":2},
            12 : {"(3,3)":1, "(4,4)":1, "(6,6)":1},
            15 : {"(5,5)":1},
            16 : {"(4,4)":1},
            18 : {"(6,6)":1},
            20 : {"(5,5)":1},
        }
        z = {
            1: [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6]],
            2: [[1,1],[1,2],[2,2],[2,3],[2,4],[2,5],[2,6]],
            3: [[1,1],[1,2],[1,3],[2,3],[3,3],[3,4],[3,5],[3,6]],
            4: [[1,1],[1,3],[2,2],[1,4],[2,4],[3,4],[4,4],[4,5],[4,6]],
            5: [[1,4],[2,3],[1,5],[2,5],[3,5],[4,5],[5,5],[5,6]],
            6: [[1,5],[2,2],[2,4],[3,3],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6]],
            7: [[1,6],[2,5],[3,4]],
            8: [[2,2],[2,6],[3,5],[4,4]],
            9: [[3,3],[3,6],[4,5]],
            10: [[4,6],[5,5]],
            11: [[5,6]],
            12: [[3,3],[4,4],[6,6]],
            15: [[5,5]],
            16: [[4,4]],
            18: [[6,6]],
            20: [[5,5]]
        }
        probs = dict(zip( range(24), 24*[0]))
        probs_list = dict(zip( range(24), 24*[0]))
        op_player  = 3-player
        blocks = []
        for point in range(24):
            if tb[point]["player"] == op_player and tb[point]["count"] > 1:
                blocks.append(point)
        for point in range(-1,25):
            if (point in range(24) and tb[point]["player"] == player and tb[point]["count"] > 0) or (self.hit[str(player-1)] and (point == -1 or point == 24)):
                nums = [11,12,14,15,15,17,6,6,5,3,2,3,0,0,1,1,0,1,0,1,0,0,0]
                if player == 1: 
                    prob = dict(zip( range(point+1, 24), nums ))
                    rel_blocks = [i-point for i in blocks if i>point]
                if player == 2: 
                    prob = dict(zip( range(point-1, -1,-1), nums ))
                    rel_blocks = [point-i for i in blocks if point>i]
                rel_blocks = [val for val in rel_blocks for _ in range(2)]
                for i in range(0,len(prob)):
                    pos = list(prob)[i]
                    dist = abs(list(prob)[i] - point)
                    if prob[pos] == 0:
                        continue
                    not_appended = []
                    for k in z[dist]:
                        if not(probs_list[pos]):
                            probs_list[pos] = list()
                        if not(k in probs_list[pos]):
                            probs_list[pos].append(k)
                        else:
                            not_appended.append(k) 
                    for j in lookup[dist].keys():
                        num1 = int(j[1])
                        num2 = int(j[3])
                        lst = [num1,num2]
                        if num1 in rel_blocks and num2 in rel_blocks and not(lst in not_appended):
                            prob[pos] -= lookup[dist][j]
                            probs_list[pos].remove(lst)
                        if num1 == num2:
                            for k in range(1,dist//num1):
                                if num1*k in rel_blocks and dist>num1*k and not(lst in not_appended):
                                    prob[pos] -= lookup[dist][j]
                                    if lst in probs_list[pos]:
                                        probs_list[pos].remove(lst)
                    
        for i in probs_list:
            if type(probs_list[i]) == list:
                for j in probs_list[i]:
                    if j[0] == j[1]:
                        probs[i] += 1
                    else:
                        probs[i] += 2
            # print(i,probs_list[i])
        # print(probs)
        for i in range(24):
            probs[i] = f"%{round(100*probs[i]/36,1)}"
            if probs[i] == "%100.0": probs[i] = "%100"
        return probs
                
game = Game()
game.settings = {
    "Display Orientation": "left",
    "Display On": True,
    "Show Hits": True,
    "Show Scores": True, 
    "Probabilities Respect To Player": 2
}
game.reset_table()
# for i in range(4):
#     print(game.table[0+6*i:6+6*i])
print("O: Player 1    @: Player 2")
turn = int(input("Which player will start the game? (player 1 -> 1, player 2 -> -1)"))
if not(turn in (1, -1)):
    raise ValueError("turn must be 1 or -1")
while not(game.over):
    dice = [randint(1,6),randint(1,6)]
    print(f"Dice: {dice[0]},{dice[1]}")
    if dice[0] == dice[1]:
        dice.append(dice[0])
        dice.append(dice[1])
    print(dice)
    while dice != [] and not(game.over):
        if turn == 1: 
            print("Player 1's turn.")
            player = "player1"
        if turn == -1:
            print("Player 2's turn.")
            player = "player2"
        if game.hit[str((1-turn)//2)]:
            while True:
                inp = input("Place a piece: ").strip()
                x = int(inp)
                if not(x in dice):
                    continue
                if game.place(player,x) != -1:
                    dice.remove(x)
                    if dice != []: print(dice)
                    break
                else:
                    print("(Miss)\n")
                    dice = []
                    break
            continue
        while True:
            inp = input("Move a piece (piece position, move distance, amount(if > 1)) ('pass' for skip round): ").strip().split(",")
            print()
            if inp == ["pass"]:
                dice = []
                break
            x1 = int(inp[0])
            x2 = int(inp[1])
            if not(x2 in dice):
                continue
            amount = 1
            if len(inp) > 2 and dice[0] == dice[1]: amount = int(inp[2])
            if amount > len(dice): amount = len(dice)
            for _ in range(amount):
                if game.move(x1, x1 + x2*turn) != -1:
                    dice.remove(x2)
            if dice != []: print(dice)
            break
    turn = -turn
print("Game over!")


