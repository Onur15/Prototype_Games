import pygame

pygame.init()
screen_width = 300
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("TicTacToe")

markers = []
gameOver = False
for x in range(3): markers.append([0] * 3)
player = 1
clock = pygame.time.Clock()
FPS = 30
run = True

def drawGrid():
    bg = (255, 230, 225)
    screen.fill(bg)
    for x in range(100, screen_width, 100):
        pygame.draw.line(screen, "black", (x, 0), (x, screen_height), 5)
        pygame.draw.line(screen, "black", (0, x), (screen_width, x), 5)
        
def drawMarkers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == -1:
                pygame.draw.circle(screen, "green", (x_pos * 100 + 50, y_pos * 100 + 50), 35, 5)
            if y == 1:
                pygame.draw.line(screen, "red", (x_pos * 100  + 20, y_pos * 100 + 20), (x_pos * 100 + 80, y_pos * 100 + 80), 5)
                pygame.draw.line(screen, "red", (x_pos * 100  + 20, y_pos * 100 + 80), (x_pos * 100 + 80, y_pos * 100 + 20), 5)
            y_pos += 1
        x_pos += 1

def checkWinner():
    if not (markers[0].__contains__(0) or  markers[1].__contains__(0) or  markers[2].__contains__(0)):
        drawLine((0,0), (0,0), 0)
        return True
    for x in range(3):
        s = markers[x]
        if (len({s[0], s[1], s[2]}) == 1) and s[0] != 0:
            drawLine((x * 100 + 50, 10), (x * 100 + 50, 290), s[0])
            return True
        if (len({markers[0][x], markers[1][x], markers[2][x]}) == 1) and markers[0][x] != 0:
            drawLine((10, x * 100 + 50), (290, x * 100 + 50), markers[0][x])
            return True
    if ((len({markers[0][0], markers[1][1], markers[2][2]}) == 1) or (len({markers[0][2], markers[1][1], markers[2][0]}) == 1)) and markers[1][1] != 0:
        if markers[0][0] == markers[1][1]:
            drawLine((10,10), (290,290), markers[1][1])
        if markers[0][2] == markers[1][1]:
            drawLine((290,10), (10,290), markers[1][1])
        return True
    else:
        return False
    
def drawLine(startPos, EndPos, marker):
    draw = False
    match(marker):
        case 1:
            color = "red"
            name = "X"
        case -1:
            color = "green"
            name = "O"
        case 0:
            color = (0,0,0)
            draw = True
    pygame.draw.line(screen, color, startPos, EndPos, 8)
    surface = pygame.Surface((200, 100))    
    surface.set_alpha(150)
    surface.fill((255,255,255))
    font = pygame.font.SysFont("monospace", 27, True)
    if draw:
        drawText = font.render("Draw!", True, (0,0,0))
        surface.blit(drawText, ((surface.get_width()-drawText.get_width()) // 2, 10))
    else:
        winText = font.render(f"{name} Win!", True, (0,0,0))
        surface.blit(winText, ((surface.get_width()-winText.get_width()) // 2, 10))
    againText = font.render("Play again?", True, (0,0,0))
    surface.blit(againText, ((surface.get_width()-againText.get_width()) // 2, 60))
    global againRect; againRect = againText.get_rect(center=(150,175))
    screen.blit(surface, (50,100))

while run:
    if not gameOver:
        clock.tick(FPS)
        drawGrid()
        drawMarkers()
        gameOver = checkWinner()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if markers[pos[0] // 100][pos[1] // 100] == 0:
                    markers[pos[0] // 100][pos[1] // 100] = player
                    player *= -1
        pygame.display.update()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if againRect.collidepoint(pos[0],pos[1]):
                    markers = []
                    for x in range(3): markers.append([0] * 3)
                    player = 1
                    gameOver = False
pygame.quit()