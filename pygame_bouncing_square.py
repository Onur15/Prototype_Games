import pygame, sys, numpy
from pygame.locals import *
def get_sign(x):
    if x == 0:
        return 0
    return x/numpy.abs(x)
def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((750,600),0,32)
    pygame.display.set_caption("Pygame Window")
    black = (30,30,30)
    blue = (0,0,255)
    green = (100,255,100)
    red = (255,0,0)
    x = 100
    y = 100
    velocity = pygame.Vector2()
    velocity.xy = 3, 4
    acceleration = 0.1
    font_color = (0,150,250)
    Font = pygame.font.Font("freesansbold.ttf", 25)
    Text1 = Font.render("Press: 'w' to jump", True, font_color)
    Text2 = Font.render("'a','d' to move", True, font_color)
    while True:
        frict = 0.6
        speed= (velocity.x**2+velocity.y**2)**0.5
        TextSpeed = Font.render(f"{numpy.round(speed,1)} m/s", True, (255,0,160))
        Textx = Font.render(f"X velocity: {numpy.round(velocity.x, 2)}", True, font_color)
        Texty = Font.render(f"Y velocity: {numpy.round(velocity.y, 2)}", True, font_color)
        Position = Font.render(f"Position(x,y): {round(x),round(y)}", True, font_color)
        DISPLAY.fill(black)
        pygame.draw.rect(DISPLAY,blue,(x,y,50,50))
        if x+130 < DISPLAY.get_width():
            DISPLAY.blit(TextSpeed,(x+60, y+20))
        else:
            DISPLAY.blit(TextSpeed,(x-100, y+20))
        DISPLAY.blit(Text1,(500,10))
        DISPLAY.blit(Text2,(500,45))
        DISPLAY.blit(Textx,(20,10))
        DISPLAY.blit(Texty,(20,45))
        DISPLAY.blit(Position,(20,80))
        keys = pygame.key.get_pressed()
        if y == 549:
            if numpy.abs(velocity.x) >= 0.08: 
                velocity.x *= 0.972
            if numpy.abs(velocity.x) < 0.08:
                velocity.x = 0
        if y != 549:
            acceleration = 0.1
        if keys[pygame.K_d]:
            velocity.x += 0.1
        if keys[pygame.K_a]:
            velocity.x -= 0.1
        if keys[pygame.K_w]:
            velocity.y = -3
        if x + 50 > DISPLAY.get_width():
            velocity.x = -velocity.x*frict
            x = 699
        if x < 0:
            velocity.x = -velocity.x*frict
            x = 1
        if y + 50 > DISPLAY.get_height():
            velocity.y = -velocity.y*frict
            y = 549
            velocity.x *= frict
            if velocity.y > -0.6:
                velocity.y, acceleration = 0, 0
        if y < 0:
            y = 1
        x += velocity.x
        y += velocity.y
        velocity.y += acceleration
        pygame.draw.line(DISPLAY, green, (x+25, y+25), (x+25+get_sign(velocity.x)*numpy.abs(velocity.x)*10, y+25), 5)
        pygame.draw.line(DISPLAY, red, (x+25, y+25), (x+25, y+25+get_sign(velocity.y)*numpy.abs(velocity.y)*10), 5)
        pygame.draw.line(DISPLAY, (50,120,190), (x+25, y+25), (x+25+get_sign(velocity.x)*numpy.abs(velocity.x)*10, y+25+get_sign(velocity.y)*numpy.abs(velocity.y)*10), 5)
        pygame.display.update()
        pygame.time.delay(11)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
main()