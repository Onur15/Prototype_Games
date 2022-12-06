import pygame, sys, numpy
from pygame.locals import *

def get_sign(x): #function for return numbers negative or positive sign
    if x == 0:
        return 0
    return x/numpy.abs(x)

def main():
    pygame.init()
    
    #Initialize variables
    DISPLAY = pygame.display.set_mode((1200,720),0,32)
    pygame.display.set_caption("Pygame Window")
    black = (30,30,30)
    blue = (0,0,255)
    green = (100,255,100)
    red = (255,0,0)
    x = 100
    y = 100
    frict = 0.6
    velocity = pygame.Vector2()
    velocity.xy = 3, 4
    acceleration = 0.1
    
    #Display constant values
    font_color = (0,150,250)
    Font = pygame.font.Font("freesansbold.ttf", 25)
    Text1 = Font.render("Press: 'w' to jump", True, font_color)
    Text2 = Font.render("'a','d' to move", True, font_color)
    Friction_Text = Font.render(f"Friction Multiplier: {frict}", True, font_color)
    Gravity = Font.render(f"Gravitational Acceleration Multiplier: {acceleration}", True, font_color)
    
    while True: #Main loop
        
        #Calculate things for display
        speed= (velocity.x**2+velocity.y**2)**0.5
        TextSpeed = Font.render(f"{numpy.round(speed,1)} m/s", True, (255,0,160))
        Textx = Font.render(f"X velocity: {numpy.round(velocity.x, 2)}", True, font_color)
        Texty = Font.render(f"Y velocity: {numpy.round(velocity.y, 2)}", True, font_color)
        Position = Font.render(f"Position(x,y): {round(x),round(y)}", True, font_color)
        
        
        #Display texts and background
        DISPLAY.fill(black)
        
        if x+130 < DISPLAY.get_width():
            DISPLAY.blit(TextSpeed,(x+60, y+20))
        else:
            DISPLAY.blit(TextSpeed,(x-100, y+20))
        DISPLAY.blit(Text1,(900,10))
        DISPLAY.blit(Text2,(900,45))
        DISPLAY.blit(Textx,(20,10))
        DISPLAY.blit(Texty,(20,45))
        DISPLAY.blit(Position,(20,80))
        DISPLAY.blit(Gravity,(20,120))
        DISPLAY.blit(Friction_Text,(20,160))
        
        #Update  object position
        pygame.draw.rect(DISPLAY,blue,(x,y,50,50))
        
        #Controls
        keys = pygame.key.get_pressed()
        if y == DISPLAY.get_height() - 51:
            if numpy.abs(velocity.x) >= 0.08: 
                velocity.x *= 0.972
            if numpy.abs(velocity.x) < 0.08:
                velocity.x = 0
        if y != DISPLAY.get_height() - 51:
            acceleration = 0.1
        if keys[pygame.K_d]:
            velocity.x += 0.1
        if keys[pygame.K_a]:
            velocity.x -= 0.1
        if keys[pygame.K_w]:
            velocity.y = -3
        
        #Frictions when object touch edges
        #And keep in the screen
        if x + 50 > DISPLAY.get_width():
            velocity.x = -velocity.x*frict
            x = DISPLAY.get_width() - 51
        if x < 0:
            velocity.x = -velocity.x*frict
            x = 1
        if y + 50 > DISPLAY.get_height():
            velocity.y = -velocity.y*frict
            y = DISPLAY.get_height() - 51
            velocity.x *= frict
            if velocity.y > -0.6:
                velocity.y, acceleration = 0, 0
        if y < 0:
            y = 1
        
        #Update position and velocity
        x += velocity.x
        y += velocity.y
        velocity.y += acceleration
        
        #Velocity lines
        pygame.draw.line(DISPLAY, green, (x+25, y+25), (x+25+get_sign(velocity.x)*numpy.abs(velocity.x)*10, y+25), 5)
        pygame.draw.line(DISPLAY, red, (x+25, y+25), (x+25, y+25+get_sign(velocity.y)*numpy.abs(velocity.y)*10), 5)
        pygame.draw.line(DISPLAY, (50,120,190), (x+25, y+25), (x+25+get_sign(velocity.x)*numpy.abs(velocity.x)*10, y+25+get_sign(velocity.y)*numpy.abs(velocity.y)*10), 5)
        
        #Exit
        pygame.display.update()
        pygame.time.delay(11)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
main()