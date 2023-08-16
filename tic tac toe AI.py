import pygame, sys, time, random
from pygame.locals import *
class Game():
    def __init__(self, screen_size = 500):
        pygame.init()
        display = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Tic Tac Toe Game")
        display.fill(pygame.Color("white"))
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
    def play(self):
        global run, rect1, rect2
        run = False
        font = pygame.font.SysFont("serif", 30)
        text = font.render("Select your symbol", True, "black")
        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
        self.display.blit(text, text_rect)
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
        while not run:
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
        self.display.fill("white")
        self.print_board()
        self.move = 0
        self.turn = True
        while run:
            pygame.display.update()
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
            if self.game_over():
                run = False
                break
            if not self.turn:
                best_move = self.find_best_move(not self.player)
                self.place(best_move[0], best_move[1], not self.player)
                print("played",best_move)
                if self.game_over():
                    run = False
                    break
                self.move += 1
                self.turn = True
            
    def game_over(self):
        if self.check_winner(self.player):
            print("player wins")
            return True
        if self.check_winner(not self.player):
            print("computer wins")
            return True
        if len(self.avaliable_moves()) == 0:
            return True
        return False
    def handle_events(self,event):
        global run
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if run:
                sq_size = self.screen_size // 3
                self.place(pos[0] // sq_size , pos[1] // sq_size, self.player)
                pygame.display.update()
                self.turn = False
            else:
                if rect1.collidepoint(pos[0], pos[1]):
                    self.player = False
                if rect2.collidepoint(pos[0], pos[1]):
                    self.player = True
                run = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    def check_winner(self, player):
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2-i] == player for i in range(3)]):
            return True
        return False
    
    def find_best_score(self, player):
        if self.check_winner(not self.player):
            return 1
        if self.check_winner(self.player):
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
        best_move = (-1,-1)
        best_score = -100
        for move in self.avaliable_moves():
            self.board[move[1]][move[0]] = symbol
            score = self.find_best_score(not symbol)
            print(move, score)
            self.board[move[1]][move[0]] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    def avaliable_moves(self):
        moves = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == " ":
                    moves.append((x,y))
        return moves 
Game().play()