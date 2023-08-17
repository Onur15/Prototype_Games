import pygame, sys, time, random
from pygame.locals import *
class Game():
    
    def __init__(self, screen_size : int = 500):
        pygame.init()
        display = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Tic Tac Toe Game")
        display.fill("white")
        self.display = display
        self.screen_size = screen_size
        self.font = pygame.font.SysFont("serif", 40, False)
        self.is_over = False
        self.blank_board()
        
    def blank_board(self):
        self.board = []
        for _ in range(3):
            self.board.append( [" "] * 3)
            
    def print_board_lines(self):
        height = self.display.get_height()
        width = self.display.get_width()
        thickness = 5
        
        for i in range(1,3):
            pygame.draw.line(self.display, "black", (0, (height * i) // 3), (width, (height * i) // 3), thickness) # Row lines
            pygame.draw.line(self.display, "black", ((width * i) // 3, 0), ((width * i) // 3, height), thickness) # Column lines
            
    def place(self, x, y, symbol: bool):
        self.board[y][x] = symbol
        cell_size = self.screen_size // 3
        offset = cell_size // 10
        width = 5
        # Coordinates
        sq_pos = [cell_size * x, cell_size * y]
        top_left = (sq_pos[0] + offset, sq_pos[1] + offset)
        bottom_right = (sq_pos[0] + cell_size - offset, sq_pos[1] + cell_size - offset)
        bottom_left = (sq_pos[0] + offset, sq_pos[1] + cell_size - offset)
        top_right = (sq_pos[0] + cell_size - offset, sq_pos[1] + offset)
        center = (sq_pos[0] + cell_size // 2, sq_pos[1] + cell_size // 2)
        radius = (cell_size - offset) / 2
        
        if symbol: # Place X
            pygame.draw.line(self.display, "red", top_left, bottom_right, width)
            pygame.draw.line(self.display, "red", bottom_left, top_right, width)
            
        else: # Place O
            pygame.draw.circle(self.display, "blue", center, radius, width)
        
    def draw_buttons(self):
        global button_o, button_x
        screen = self.screen_size
        
        radius = screen // 10
        offset = screen // 30
        left = screen * 0.2
        top = screen * 0.35
        width = screen - 2*left # Center box
        
        box = pygame.Rect(left, top, width, radius*2) # Only for alignment / invisible
        # Drawing O
        pygame.draw.circle(self.display, "blue", (box.x + radius, box.y + radius), radius, 5)
        # Drawing X
        bottom_right = (box.bottomright[0] - offset, box.bottomright[1] - offset)
        top_left = (box.bottomright[0] + offset - radius*2, box.bottomright[1] + offset - radius*2)
        bottom_left = (box.bottomright[0] + offset - radius*2, box.bottomright[1] - offset)
        top_right = (box.bottomright[0] - offset, box.bottomright[1] + offset - radius*2)
        pygame.draw.line(self.display, "red", bottom_right, top_left, 5)
        pygame.draw.line(self.display, "red", bottom_left, top_right, 5)
        
        button_o = pygame.Rect(left - offset, top - offset, 2*(radius+offset), 2*(radius+offset)) # Button for O
        button_x = pygame.Rect(left + width - 2*radius - offset, top - offset, 2*(radius+offset), 2*(radius+offset)) # Button for X
        pygame.draw.rect(self.display, "black", button_o, 5, 20)
        pygame.draw.rect(self.display, "black", button_x, 5, 20)
        
    def play(self):
        global run
        run = False
        
        self.draw_buttons()
        text = self.font.render("Select your symbol", True, "black")
        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
        self.display.blit(text, text_rect)
        
        while not run: # Starting screen
            pygame.time.delay(10)
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
                
        # Player selected symbol
        self.display.fill("white")
        self.print_board_lines()
        self.move = 0
        self.turn = self.player
        # Game started
        while run:
            pygame.display.update()
            pygame.time.delay(10)
            # Player plays
            for event in pygame.event.get():
                self.handle_events(event)
                pygame.display.update()
                
            if self.game_over()[0]:
                run = False
                time.sleep(1.5)
            # Computer plays
            if not self.turn and run:
                best_move = self.find_best_move(not self.player)
                self.place(best_move[0], best_move[1], not self.player)
                #print("played",best_move)
                if self.game_over()[0]:
                    run = False
                    time.sleep(1.5)
                self.turn = True
            
            # Game Over
            if not run:
                self.is_over = True
                match self.game_over()[1]:
                    case "draw":
                        self.display.fill("white")
                        text = self.font.render("Draw!", True, "black")
                        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
                        self.display.blit(text, text_rect)
                    case "player":
                        self.display.fill("white")
                        text = self.font.render("Player wins!", True, "black")
                        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
                        self.display.blit(text, text_rect)
                    case "computer":
                        self.display.fill("white")
                        text = self.font.render("Computer wins!", True, "black")
                        text_rect = text.get_rect(center=(self.screen_size // 2, text.get_height() * 2))
                        self.display.blit(text, text_rect)
                self.draw_restart_button()
                pygame.display.update()
                # Loop for player to press restart
                while True:
                     for event in pygame.event.get():
                        self.handle_events(event)
                        pygame.display.update()
                        
    def draw_line(self, player, row = None, col = None, diagonal = None):
        color = "red" if player else "blue"
        cell_size = self.screen_size // 3
        offset = cell_size // 4
        screen = self.screen_size
        width = 10
        if row != None:
            left = (offset, cell_size // 2 + row * cell_size)
            right = (screen - offset, cell_size // 2 + row * cell_size)
            pygame.draw.line(self.display, color, left, right, width)
            
        if col != None:
            top = (cell_size // 2 + col * cell_size, offset)
            bottom = (cell_size // 2 + col * cell_size, screen-offset)
            pygame.draw.line(self.display, color, top, bottom, width)
            
        if diagonal != None:
            if all([self.board[i][i] == player for i in range(3)]):
                pygame.draw.line(self.display, color, (offset, offset), (screen - offset, screen - offset), width)
            else:
                pygame.draw.line(self.display, color, (offset, screen - offset), (screen - offset, offset), width)
                
        pygame.display.update()
            
    def draw_restart_button(self):
        global res_button
        restart_text = self.font.render("Restart", True, "black")
        restart_rect = restart_text.get_rect(center = (self.screen_size // 2, self.screen_size // 2)) # Only for alignment / invisible
        self.display.blit(restart_text, restart_rect)
        res_button = restart_text.get_rect(width = 2*restart_text.get_width(), height = 1.5*restart_text.get_height(), center = (self.screen_size // 2, self.screen_size // 2))
        pygame.draw.rect(self.display, "black", res_button, 5, 20)
        
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
        cell_size = self.screen_size // 3
        pos = pygame.mouse.get_pos()
        x = pos[0] // cell_size
        y = pos[1] // cell_size
        offset = 3
        box_size = cell_size - 8
        margin = lambda x: (cell_size + 2) * x + offset
        bg_color = "gold"
        
        # Hover effect for restart button
        if event.type == MOUSEMOTION and self.is_over:
            
            # Coloring button's background
            if res_button.collidepoint(pos[0], pos[1]) and self.is_over:
                pygame.draw.rect(self.display, bg_color, res_button, 0, 20)
                self.draw_restart_button()
                
            # Resetting button's background
            else:
                pygame.draw.rect(self.display, "white", res_button, 0, 20)
                self.draw_restart_button()
        
        # Hover effect for selection buttons
        elif event.type == MOUSEMOTION and not run:
            
            # Coloring buttons' background
            if button_o.collidepoint(pos[0], pos[1]):
                pygame.draw.rect(self.display, bg_color, button_o, 0, 20)
                self.draw_buttons()
            elif button_x.collidepoint(pos[0], pos[1]):
                pygame.draw.rect(self.display, bg_color, button_x, 0, 20)
                self.draw_buttons()
                
            # Reseting buttons' background
            else:
                pygame.draw.rect(self.display, "white", button_o, 0, 20)
                pygame.draw.rect(self.display, "white", button_x, 0, 20)
                self.draw_buttons()
        
        # Hover effect for avaliable cells
        elif event.type == MOUSEMOTION and run:
            
            # Reseting cell's background
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "f":
                        filler = pygame.Rect(margin(j), margin(i), box_size, box_size)
                        pygame.draw.rect(self.display, "white", filler)
                        self.board[i][j] = " "
                        
            # Coloring cell's background
            if (x, y) in self.avaliable_moves():
                filler = pygame.Rect(margin(x), margin(y), box_size, box_size)
                pygame.draw.rect(self.display, bg_color, filler)
                self.board[y][x] = "f"
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1: # Left click
            # Reset button
            if self.is_over:
                if res_button.collidepoint(pos[0], pos[1]):
                    new_game = Game()
                    new_game.play()
            
            # Placing symbol on the cell  
            elif run and self.turn:
                if (x, y) in self.avaliable_moves():
                    # Resetting cell's background color before placing
                    filler = pygame.Rect(margin(x), margin(y), box_size, box_size)
                    pygame.draw.rect(self.display, "white", filler)
                    
                    self.place(x , y, self.player)
                    pygame.display.update()
                    time.sleep(0.5)
                    self.move += 1
                    self.turn = False
                    
            # Selecting symbol
            else:
                if button_o.collidepoint(pos[0], pos[1]):
                    self.player = False
                    run = True
                if button_x.collidepoint(pos[0], pos[1]):
                    self.player = True
                    run = True

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    def check_winner(self, player : bool):
        # Returns row, col or diagonal values for drawing winning line
        
        for row in self.board:
            if all([cell == player for cell in row]):
                return (True, self.board.index(row), None, None)
            
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return (True, None, col, None)
            
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2-i] == player for i in range(3)]):
            return (True, None, None, True)
        
        return (False, None, None, None)
    
    def find_best_score(self, player : bool): # Minimax Algorithm
        if self.check_winner(not self.player)[0]:
            return 1
        
        if self.check_winner(self.player)[0]:
            return -1
        
        if len(self.avaliable_moves()) == 0:
            return 0
        
        # Own perspective
        if player != self.player:
            best_score = -100
            for move in self.avaliable_moves():
                self.board[move[1]][move[0]] = player
                score = self.find_best_score(not player)
                self.board[move[1]][move[0]] = " "
                best_score = max(best_score, score)
            return best_score
        
        # Opponent's perspective
        else:
            best_score = 100
            for move in self.avaliable_moves():
                self.board[move[1]][move[0]] = player
                score = self.find_best_score(not player)
                self.board[move[1]][move[0]] = " "
                best_score = min(best_score, score)
            return best_score
        
    def find_best_move(self, symbol : bool):
        # All moves are equal at the start
        if self.move == 0:
            time.sleep(0.5)
            return random.choice(self.avaliable_moves())
        
        best_moves = []
        best_score = -100
        for move in self.avaliable_moves():
            self.board[move[1]][move[0]] = symbol
            score = self.find_best_score(not symbol)
            print(move, score)
            self.board[move[1]][move[0]] = " "
            # Selecting moves that has highest score
            if score > best_score:
                best_score = score
                # If it finds move that has higher score than it already stored moves
                # Deletes previous moves
                best_moves.clear()
                best_moves.append( (move , score) )
                
            # Adds move to list if the move has same score 
            elif score == best_score:
                best_moves.append( (move , score) )
        print(best_moves)
        # Selects one of the best moves
        return random.choice(best_moves)[0]
    
    def avaliable_moves(self):
        moves = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == " " or cell == "f":
                    moves.append((x,y))
        return moves

if __name__ == "__main__":
    new_game = Game()
    new_game.play()