import pygame, sys, time, random
from pygame.locals import *
class Game():
    
    def __init__(self, screen_size = 500):
        pygame.init()
        display = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Tic Tac Toe Game")
        display.fill("white")
        self.display = display
        self.screen_size = screen_size 
        self.board = []
        for _ in range(3):
            self.board.append( [" "] * 3)
    
    def print_board(self):
        height = self.display.get_height()
        width = self.display.get_width()
        for i in range(1,3):
            pygame.draw.line(self.display, (0, 0, 0), (0, (height * i) // 3), (width, (height * i) // 3), 5)
            pygame.draw.line(self.display, (0, 0, 0), ((width * i) // 3, 0), ((width * i) // 3, height), 5)
            
    def place(self, x, y, symbol: bool):
        self.board[y][x] = symbol
        size = self.screen_size // 3
        offset = size // 10
        x += 1
        y += 1
        sq_pos = {
            "x" : size * x,
            "y" : size * y,
        }
        if symbol:
            pygame.draw.line(self.display, "red", (sq_pos["x"] - size + offset, sq_pos["y"] - size + offset), (sq_pos["x"] - offset, sq_pos["y"] - offset), 5)
            pygame.draw.line(self.display, "red", (sq_pos["x"] - size + offset, sq_pos["y"] - offset), (sq_pos["x"] - offset, sq_pos["y"] - size + offset), 5)
        else:
            pygame.draw.circle(self.display, "blue", (sq_pos["x"] - size // 2, sq_pos["y"] - size // 2), (size - offset) / 2, 5)  
        pygame.display.update()
        
    def draw_buttons(self):
        global rect1, rect2
        radius = self.screen_size // 10
        offset = self.screen_size // 30
        left = self.screen_size * 0.2
        top = self.screen_size * 0.35
        width = self.screen_size * 0.6
        box = pygame.Rect(left, top, width, radius*2) 
        pygame.draw.circle(self.display, "blue", (box.x + radius, box.y + radius), radius, 5)
        pygame.draw.line(self.display, "red", (box.bottomright[0] - offset, box.bottomright[1] - offset), (box.bottomright[0] + offset - radius*2, box.bottomright[1] + offset - radius*2), 5)
        pygame.draw.line(self.display, "red", (box.bottomright[0] + offset - radius*2, box.bottomright[1] - offset), (box.bottomright[0] - offset, box.bottomright[1] + offset - radius*2), 5)
        rect1 = pygame.Rect(left - offset, top - offset, 2*(radius+offset), 2*(radius+offset))
        rect2 = pygame.Rect(left + width - 2*radius - offset, top - offset, 2*(radius+offset), 2*(radius+offset))
        pygame.draw.rect(self.display, "black", rect2, 5, 20)
        pygame.draw.rect(self.display, "black", rect1, 5, 20)
        
    def play(self):
        global run
        self.is_over = False
        run = False
        self.draw_buttons()
        font = pygame.font.SysFont("serif", 30, False)
        text = font.render("Select your symbol", True, "black")
        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
        self.display.blit(text, text_rect)
        while not run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
        self.display.fill("white")
        self.print_board()
        self.move = 0
        self.turn = self.player
        while run:
            pygame.display.update()
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_events(event)
            if self.game_over()[0]:
                run = False
                time.sleep(1.5)
            if not self.turn and run:
                best_move = self.find_best_move(not self.player)
                self.place(best_move[0], best_move[1], not self.player)
                #print("played",best_move)
                if self.game_over()[0]:
                    run = False
                    time.sleep(1.5)
                self.turn = True
            if not run:
                font = pygame.font.SysFont("serif", 40)
                self.is_over = True
                match self.game_over()[1]:
                    case "draw":
                        self.display.fill("white")
                        text = font.render("Draw!", True, "black")
                        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
                        self.display.blit(text, text_rect)
                    case "player":
                        self.display.fill("white")
                        text = font.render("Player wins!", True, "black")
                        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
                        self.display.blit(text, text_rect)
                    case "computer":
                        self.display.fill("white")
                        text = font.render("Computer wins!", True, "black")
                        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
                        self.display.blit(text, text_rect)
                self.draw_restart_button()
                pygame.display.update()
                while True:
                     for event in pygame.event.get():
                        self.handle_events(event)
                        
    def draw_line(self, player, row=None, col=None, diagonal=None):
        color = "red" if player else "blue"
        cell = self.screen_size // 3
        if row:
            pygame.draw.line(self.display, color, (cell//4, cell//2 + row*cell), (self.screen_size-cell//4, cell//2 + row*cell),10)
        if col:
            pygame.draw.line(self.display, color, (cell//2 + col*cell, cell//4), (cell//2 + col*cell, self.screen_size-cell//4),10)
        if diagonal:
            if all([self.board[i][i] == player for i in range(3)]):
                pygame.draw.line(self.display, color, (cell//4, cell//4), (self.screen_size-cell//4, self.screen_size-cell//4),10)
            else:
                pygame.draw.line(self.display, color, (cell//4, self.screen_size-cell//4), (self.screen_size-cell//4, cell//4),10)
        pygame.display.update()
            
    def draw_restart_button(self):
        global button
        font = pygame.font.SysFont("serif", 40)
        restart_text = font.render("Restart", True, "black")
        restart_rect = restart_text.get_rect(center = (self.screen_size // 2, self.screen_size // 2))
        self.display.blit(restart_text, restart_rect)
        button = restart_text.get_rect(width = 2*restart_text.get_width(), height = 1.5*restart_text.get_height(), center = (self.screen_size // 2, self.screen_size // 2))
        pygame.draw.rect(self.display, "black", button, 5, 20)
        
    def game_over(self):
        if self.check_winner(self.player)[0]:
            info = self.check_winner(self.player)
            self.draw_line(self.player, row=info[1], col=info[2], diagonal=info[3])
            return (True,"player")
        if self.check_winner(not self.player)[0]:
            info = self.check_winner(not self.player)
            self.draw_line(not self.player, row=info[1], col=info[2], diagonal=info[3])
            return (True, "computer")
        if len(self.avaliable_moves()) == 0:
            return (True, "draw")
        return (False, None)
    
    def handle_events(self,event):
        global run
        pos = pygame.mouse.get_pos()
        color = "gold"
        if event.type == MOUSEMOTION and self.is_over:
            if button.collidepoint(pos[0], pos[1]) and self.is_over:
                pygame.draw.rect(self.display, color, button, 0, 20)
                self.draw_restart_button()
            else:
                pygame.draw.rect(self.display, "white", button, 0, 20)
                self.draw_restart_button()
            pygame.display.update()
        elif event.type == MOUSEMOTION and not run:
            if rect1.collidepoint(pos[0], pos[1]):
                pygame.draw.rect(self.display, color, rect1, 0, 20)
                self.draw_buttons()
            elif rect2.collidepoint(pos[0], pos[1]):
                pygame.draw.rect(self.display, color, rect2, 0, 20)
                self.draw_buttons()
            else:
                pygame.draw.rect(self.display, "white", rect1, 0, 20)
                pygame.draw.rect(self.display, "white", rect2, 0, 20)
                self.draw_buttons()
            pygame.display.update()
        elif event.type == MOUSEMOTION and run:
            cell = self.screen_size // 3
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "f":
                        filler = pygame.Rect((cell+2) * j + 3, (cell+2) * i + 3, cell-8, cell-8)
                        pygame.draw.rect(self.display, "white", filler)
                        self.board[i][j] = " "
            if (pos[0]//cell, pos[1]//cell) in self.avaliable_moves():
                filler = pygame.Rect((cell+2) * (pos[0] // cell) + 3, (cell+2) * (pos[1] // cell) + 3, cell-8, cell-8)
                pygame.draw.rect(self.display, color, filler)
                self.board[pos[1] // cell][pos[0] // cell] = "f"
            pygame.display.update()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:    
            if self.is_over:
                if button.collidepoint(pos[0], pos[1]):
                    new_game = Game()
                    new_game.play()  
            elif run and self.turn:
                sq_size = self.screen_size // 3
                if (pos[0]//sq_size, pos[1]//sq_size) in self.avaliable_moves():
                    filler = pygame.Rect((sq_size+2) * (pos[0]//sq_size) + 3, (sq_size+2) * (pos[1]//sq_size) + 3, sq_size-8, sq_size-8)
                    pygame.draw.rect(self.display, "white", filler)
                    self.place(pos[0] // sq_size , pos[1] // sq_size, self.player)
                    pygame.display.update()
                    time.sleep(0.5)
                    self.move += 1
                    self.turn = False
            else:
                if rect1.collidepoint(pos[0], pos[1]):
                    self.player = False
                    run = True
                if rect2.collidepoint(pos[0], pos[1]):
                    self.player = True
                    run = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    def check_winner(self, player):
        for row in self.board:
            if all([cell == player for cell in row]):
                return (True, self.board.index(row), None, None)
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return (True, None, col, None)
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2-i] == player for i in range(3)]):
            return (True, None, None, True)
        return (False, None, None, None)
    
    def find_best_score(self, player):
        if self.check_winner(not self.player)[0]:
            return 1
        if self.check_winner(self.player)[0]:
            return -1
        if len(self.avaliable_moves()) == 0:
            return 0
        if player != self.player:
            best_score = -100
            for move in self.avaliable_moves():
                self.board[move[1]][move[0]] = player
                score = self.find_best_score(not player)
                self.board[move[1]][move[0]] = " "
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = 100
            for move in self.avaliable_moves():
                self.board[move[1]][move[0]] = player
                score = self.find_best_score(not player)
                self.board[move[1]][move[0]] = " "
                best_score = min(best_score, score)
            return best_score
        
    def find_best_move(self, symbol):
        if self.move == 0:
            time.sleep(0.5)
            return random.choice(self.avaliable_moves())
        best_moves = []
        best_score = -100
        for move in self.avaliable_moves():
            self.board[move[1]][move[0]] = symbol
            score = self.find_best_score(not symbol)
            #print(move, score)
            self.board[move[1]][move[0]] = " "
            if score > best_score:
                best_score = score
                best_moves.append( (move , score) )
                i = 0
                while i < len(best_moves):
                    if best_moves[i][1] < score:
                        best_moves.remove(best_moves[i])
                    else:
                        i += 1
            elif score == best_score:
                best_moves.append( (move , score) )
        #print(best_moves)
        return random.choice(best_moves)[0]
    
    def avaliable_moves(self):
        moves = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == " " or cell == "f":
                    moves.append((x,y))
        return moves 
new_game = Game()
new_game.play()