import numpy as np
from math import pi, log, exp, sin, cos
import pygame, sys
from pygame.locals import *

def reduce_angle(a):
    if a < 0:
        a += 360
    if a > 180:
        a -= 180
    return a
def main():
    pygame.init()
    # Constants
    center = [0,0]
    w = float(3) # rad/second
    radius = 4 # meter
    g = 9.8 # m/s^2
    mass = 1
    dt = 2e-3 #ms
    k = 1.4

    #Initial values
    angle = -90
    weight = pygame.Vector2(0, -mass*g)
    pos = radius*pygame.Vector2(cos(pi*(1-angle/180)),sin(pi*(1-angle/180)))
    velocity = w* pygame.Vector2(-pos[1],pos[0])
    acc = -w**2 * pos
    DISPLAY = pygame.display.set_mode((1200,720),0,32)
    pygame.display.set_caption("Pygame Window")
    font_color = (0,150,250)
    Font = pygame.font.Font("freesansbold.ttf", 25)
    black = (30,30,30)
    blue = (0,0,255)
    green = (70,255,20)
    red = (255,0,0)
    white = (255,255,255)
    center = [DISPLAY.get_width() / 2, DISPLAY.get_height() / 2]
    while True:
        pos_mag = pos.magnitude()
        if pos_mag < radius or pos.dot(velocity) < 0:
            tension = pygame.Vector2(0,0)
        if pos.dot(velocity) == 0:
            tension = -mass * w**2 * pos
        if pos_mag >= radius and pos.dot(velocity) > 0:
            tension = (exp(log(pos.dot(velocity)*mass*k)-log(pos_mag**2 * dt))+ (pos_mag-radius)*mass/dt)* (-pos)
        force = tension + weight
        acc = force / mass
        velocity += acc * dt
        pos += velocity * dt
        DISPLAY.fill(white)
        pygame.draw.line(DISPLAY, green,(-50*pos.x+center[0], -50*pos.y+center[1]),(-50*pos.x+center[0]-5*velocity.x, -50*pos.y+center[1]-5*velocity.y), 5)
        pygame.draw.line(DISPLAY, black,(-50*pos.x+center[0], -50*pos.y+center[1]),(-50*pos.x+center[0], -50*pos.y+center[1]-5*weight.y), 5)
        Textx = Font.render(f"position magnitude: {np.round(pos.magnitude(), 3)}", True, font_color)
        Textv = Font.render(f"velocity magnitude: {np.round(velocity.magnitude(), 3)}", True, font_color)
        Textangle = Font.render(f"Velocity-Position Angle: {round(reduce_angle(velocity.angle_to(pos)))}", True, font_color)
        DISPLAY.blit(Textx,(20,10))
        DISPLAY.blit(Textv,(20,40))
        DISPLAY.blit(Textangle,(20,70))
        pygame.draw.circle(DISPLAY, blue, (center[0], center[1]), 50*radius, 1)
        pygame.draw.line(DISPLAY, red, (center[0] , center[1]), (-50*pos.x+center[0], -50*pos.y+center[1]), 2)
        pygame.draw.circle(DISPLAY, blue, (-50*pos.x+center[0], -50*pos.y+center[1]), 10)
        #Exit
        pygame.display.update()
        pygame.time.delay(3)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
        
main()

    