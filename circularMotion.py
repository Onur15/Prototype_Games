import numpy as np
from math import pi, log, exp, sin, cos
import pygame, sys
from pygame.locals import *

def reduce_angle(a:float)->float:
    if a < 0:
        a += 360
    if a > 180:
        a -= 180
    return a

def calc_tension(position: pygame.math.Vector2, velocity:pygame.math.Vector2, lengthOfRope:float, mass:float, dt:float, k:float) -> pygame.math.Vector2:
    pos_mag = position.magnitude()
    T_len = exp(log(position.dot(velocity)*mass*k) - log(pos_mag*dt)) + (pos_mag-lengthOfRope)*mass/dt**2
    T_dir = -position/pos_mag
    return T_len * T_dir
    
def main():
    pygame.init()
    # pygame Constants
    DISPLAY = pygame.display.set_mode((1200,720),0,32)
    pygame.display.set_caption("Pygame Window")
    font_color = (0,150,250)
    Font = pygame.font.Font("freesansbold.ttf", 25)
    black = (30,30,30)
    blue = (0,0,255)
    green = (70,200,20)
    red = (200,30,60)
    white = (255,255,255)
    center = [DISPLAY.get_width() / 2, DISPLAY.get_height() / 2]
    
    #Simulation Constants
    radius = 4 # meter
    g = 9.8 # m/s^2
    mass = 1 #kg
    dt = 5e-3 #ms
    k = 1 
    motion_type = "vertical" #vertical or horizontal
    weight = pygame.Vector2(0, -mass*g)
    
    #Initial values
    w = -float((5*g/radius)**(1/2)-0.1) # rad/second
    angle = -90
    pos = radius*pygame.Vector2(cos(pi*(1-angle/180)),sin(pi*(1-angle/180)))
    velocity = w*pygame.Vector2(-pos[1],pos[0])
    
    while True:        
        #Calculations
        pos_mag = pos.magnitude()
        if pos_mag < radius or pos.dot(velocity) < 0:
            tension = pygame.Vector2(0,0)
        if pos.dot(velocity) == 0:
            tension = -mass * w**2 * pos
        if pos_mag >= radius and pos.dot(velocity) > 0:
            tension = calc_tension(pos, velocity, radius, mass, dt, k)
        match motion_type:
            case "vertical":
                force = tension + weight            
            case "horizontal":
                force = tension
            case _: raise ValueError()
        acc = force / mass
        velocity += acc * dt
        pos += velocity * dt
        
        #Display
        DISPLAY.fill(white)
        pygame.draw.line(DISPLAY, green,(-50*pos.x+center[0], -50*pos.y+center[1]),(-50*pos.x+center[0]-5*velocity.x, -50*pos.y+center[1]-5*velocity.y), 5)
        Textx = Font.render(f"Position magnitude: {round(pos.magnitude(), 3)} m", True, font_color)
        Textv = Font.render(f"Velocity magnitude: {round(velocity.magnitude(), 3)} m/s", True, font_color)
        Textangle = Font.render(f"Velocity-Position Angle: {round(reduce_angle(velocity.angle_to(pos)), 3)}°", True, font_color)
        Textt = Font.render(f"Tension magnitude: {round(tension.magnitude(), 1)} N", True, font_color)
        Textkinetic = Font.render(f"Kinetic Energy: {round(mass*velocity.magnitude_squared()/2,1)} J", True, red)
        Textmotion = Font.render(f"{motion_type.capitalize()} Motion", True, green)
        if motion_type == "vertical":
            pygame.draw.line(DISPLAY, black,(-50*pos.x+center[0], -50*pos.y+center[1]),(-50*pos.x+center[0], -50*pos.y+center[1]-5*weight.y), 5)
            Textpotential = Font.render(f"Potential Energy: {round(mass*g*(pos.y+radius),1)} J", True, red)
            Textenergy = Font.render(f"Total Energy: {round(mass*velocity.magnitude_squared()/2+mass*g*(pos.y+radius),1)} J", True, red)
            DISPLAY.blit(Textpotential,(900,40))
            DISPLAY.blit(Textenergy,(900,70))
        DISPLAY.blit(Textx,(20,10))
        DISPLAY.blit(Textv,(20,40))
        DISPLAY.blit(Textangle,(20,70))
        DISPLAY.blit(Textt,(20,100))
        DISPLAY.blit(Textmotion,(510,10))
        DISPLAY.blit(Textkinetic,(900,10))
        pygame.draw.circle(DISPLAY, blue, (center[0], center[1]), 50*radius, 2)
        pygame.draw.line(DISPLAY, red, (center[0] , center[1]), (-50*pos.x+center[0], -50*pos.y+center[1]), 2)
        pygame.draw.circle(DISPLAY, blue, (-50*pos.x+center[0], -50*pos.y+center[1]), 10)
        pygame.draw.circle(DISPLAY, black, (center[0], center[1]), 5, 5)
        #Exit
        pygame.display.update()
        pygame.time.delay(int(dt*1000))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
        
main()

    