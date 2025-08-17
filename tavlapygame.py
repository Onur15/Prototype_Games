from random import randint
import pygame, sys, os, time, math
from pygame.locals import *
class Game():
    def __init__(self):
        pygame.init()
        desktop_width=pygame.display.get_desktop_sizes()[0][0]
        sc_width=int(desktop_width*17/20)
        self.sc_ratio = 0.65
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,25)
        display = pygame.display.set_mode((desktop_width,sc_width*self.sc_ratio),pygame.RESIZABLE)
        draw_surf = pygame.Surface((desktop_width,sc_width*self.sc_ratio), pygame.SRCALPHA)
        draw_surf.fill("white")
        pygame.display.set_caption("Tavla")
        width,height=draw_surf.get_width(),draw_surf.get_height()
        self.btn_surf=pygame.Surface((width,height), pygame.SRCALPHA)
        global left, pt, rad, bar_width, h, w, board_colors
        board_colors=[(38,1,1),(80,30,30),(240,150,50)]
        pt=width/100
        bar_width=int(pt*16/3)
        left=width/2-bar_width/2-(height-8*pt)*self.sc_ratio
        w,h=width/2-bar_width/2-left,height-8*pt
        rad=h*23/500
        self.turn = 1
        self.flipped = False
        self.select = [-1,0]
        self.window = display
        self.display = draw_surf
        self.font = pygame.font.SysFont("serif", sc_width//50)
        self.over = True
        self.waiting = False
        self.table = []
        self.hit = {"0": 0, "1": 0}
        self.scores = {"0": 0, "1": 0}
        self.collected = {"1": 0, "2": 0}
        self.settings = {
            "Display Orientation": "right",
            "Show Scores": False,
            "Show Moves": True,
            "Flip Board": True,
            "probs": True,
            "Double Dice": False,
            "debug": False,
            "custom board": False}  
    def reset_table(self):
        self.turn=1
        self.hit = {"0": 0, "1": 0}
        self.scores = {"0": 0, "1": 0}
        self.collected = {"1": 0, "2": 0}
        self.table.clear()
        self.flipped=False
        self.waiting=False
        self.select=[-1,0]
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
        self.display_table()
    def display_table(self,stones=True):
        global left, pt, rad, bar_width, h, w, board_colors
        disp_orientation=self.settings["Display Orientation"]
        if self.flipped: 
            disp_orientation="right" if disp_orientation=="left" else "left"
        self.display.fill("white")
        p1c=[(245,70,70),(200,55,55)]
        p2c=[(225,225,225),(190,190,190)]
        probs = list(self.calc_prob(3-self.turn).values())
        if self.flipped: probs=probs[::-1]
        width=self.display.get_width()
        height=self.display.get_height()
        size=(height-8*pt)*self.sc_ratio
        #Draw Board
        pygame.draw.rect(self.display,board_colors[2],(left,4*pt,2*size+bar_width+1,height-8*pt+1))
        pygame.draw.rect(self.display,board_colors[0],(left-int(bar_width/2),4*pt-int(bar_width/2),2*size+2*bar_width,height-8*pt+bar_width),int(bar_width/2))
        pygame.draw.line(self.display,board_colors[0],(width/2,4*pt),(width/2,height-4*pt),bar_width)
        pygame.draw.rect(self.display,board_colors[1],(width/2-bar_width/3,4*pt+h*0.08,bar_width*2/3,h/3))
        pygame.draw.rect(self.display,board_colors[1],(width/2-bar_width/3,height-4*pt-h*0.08-h/3,bar_width*2/3,h/3))
        pygame.draw.line(self.display,board_colors[0],(width/2,4*pt+h*0.08+h/9),(width/2,5*pt+h*0.08+h/9),bar_width)
        pygame.draw.line(self.display,board_colors[0],(width/2,height-4*pt-h*0.08-h/3+h*2/9),(width/2,height-3*pt-h*0.08-h/3+h*2/9),bar_width)
        self.boxes=[0 for _ in range(26)]
        for j in range(6): #Create Boxes
            if disp_orientation == "left":
                self.boxes[0]=pygame.Rect(left-w/6,4*pt,w/6,h/2)
                self.boxes[25]=pygame.Rect(left-w/6,height-4*pt-h/2,w/6,h/2)
                self.boxes[j+1]=pygame.Rect(left+w*j/6,4*pt,w/6,h/2)
                self.boxes[j+7]=pygame.Rect(left+bar_width+w*(1+j/6),4*pt,w/6,h/2)
                self.boxes[j+13]=pygame.Rect(left+bar_width+w*(11/6-j/6),height-4*pt-h/2,w/6,h/2)
                self.boxes[j+19]=pygame.Rect(left+w*(5/6-j/6),height-4*pt-h/2,w/6,h/2)
            if disp_orientation == "right":
                self.boxes[0]=pygame.Rect(left+bar_width+w*2,4*pt,w/6,h/2)
                self.boxes[25]=pygame.Rect(left+bar_width+w*2,height-4*pt-h/2,w/6,h/2)
                self.boxes[j+1]=pygame.Rect(left+bar_width+w*(11/6-j/6),4*pt,w/6,h/2)
                self.boxes[j+7]=pygame.Rect(left+w*(5/6-j/6),4*pt,w/6,h/2)
                self.boxes[j+13]=pygame.Rect(left+w*j/6,height-4*pt-h/2,w/6,h/2)
                self.boxes[j+19]=pygame.Rect(left+bar_width+w*(1+j/6),height-4*pt-h/2,w/6,h/2)
            if self.settings["debug"]:
                pygame.draw.rect(self.display,"black",self.boxes[0],2)
                pygame.draw.rect(self.display,"black",self.boxes[25],2)
                pygame.draw.rect(self.display,"black",self.boxes[j+1],2)
                pygame.draw.rect(self.display,"black",self.boxes[j+7],2)
                pygame.draw.rect(self.display,"black",self.boxes[j+13],2)
                pygame.draw.rect(self.display,"black",self.boxes[j+19],2)
            if j%2==1: #Draw Triangles
                pygame.draw.polygon(self.display,(166,3,33),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j,4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j,4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j,4*pt+h*0.4)])
                pygame.draw.polygon(self.display,(166,3,33),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j+w+bar_width,4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,4*pt+h*0.4)])
                pygame.draw.polygon(self.display,(64,1,13),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j,height-4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j,height-4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j,height-4*pt-h*0.4)])
                pygame.draw.polygon(self.display,(64,1,13),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,height-4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j+w+bar_width,height-4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,height-4*pt-h*0.4)])
            else:
                pygame.draw.polygon(self.display,(64,1,13),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j,4*pt),(left+2*rad+(w-12*rad)*(1+j)/7+(2*rad)*j,4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j,4*pt+h*0.4)])
                pygame.draw.polygon(self.display,(64,1,13),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j+w+bar_width,4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,4*pt+h*0.4)])
                pygame.draw.polygon(self.display,(166,3,33),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j,height-4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j,height-4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j,height-4*pt-h*0.4)])
                pygame.draw.polygon(self.display,(166,3,33),[(left+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,height-4*pt),(left+(w-12*rad)*(1+j)/7+2*rad+(2*rad)*j+w+bar_width,height-4*pt),(left+rad+(w-12*rad)*(1+j)/7+(2*rad)*j+w+bar_width,height-4*pt-h*0.4)])   
        def disp_scores(self):
            scores = [f"Player1 Score: {self.scores["0"]}",f"Player2 Score: {self.scores["1"]}"]
            font=pygame.font.SysFont("serif", self.display.get_width()//70)
            tx1=font.render(scores[0],True,"black")
            sz1=pygame.font.Font.size(self.font,scores[0])
            tx2=font.render(scores[1],True,"black")
            self.display.blit(tx1,(left+w+bar_width-pt-sz1[0],0))
            self.display.blit(tx2,(left+w+bar_width/2+pt,0))
        def disp_prob(self,tx,coord): #Display Probabilities
            text=self.font.render(tx,True,"white")
            self.display.blit(text,coord)
        if self.settings["probs"]:
            sz1=pygame.font.Font.size(self.font,"%0")
            sz2=pygame.font.Font.size(self.font,"%99")
            sz3=pygame.font.Font.size(self.font,"%100")
            szl=[sz1,sz2,sz3]
            spc=(w-12*rad)/7+2*rad
            if disp_orientation == "left":
                for j in range(6): 
                    disp_prob(self,probs[j],(left+(w-12*rad)/7+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,4*pt-szl[len(probs[j])-2][1]))
                    disp_prob(self,probs[j+6],(left+(w-12*rad)/7+w+bar_width+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,4*pt-szl[len(probs[j])-2][1]))
                    disp_prob(self,probs[23-j],(left+(w-12*rad)/7+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,height-4*pt))
                    disp_prob(self,probs[17-j],(left+(w-12*rad)/7+w+bar_width+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,height-4*pt))
            if disp_orientation == "right":
                for j in range(6):
                    disp_prob(self,probs[11-j],(left+(w-12*rad)/7+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,4*pt-szl[len(probs[j])-2][1]))
                    disp_prob(self,probs[5-j],(left+(w-12*rad)/7+w+bar_width+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,4*pt-szl[len(probs[j])-2][1]))
                    disp_prob(self,probs[j+12],(left+(w-12*rad)/7+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,height-4*pt))
                    disp_prob(self,probs[j+18],(left+(w-12*rad)/7+w+bar_width+(2*rad-szl[len(probs[j])-2][0])/2+j*spc,height-4*pt))
        if stones:
            for i in range(24): #Draw Stones
                self.draw_stones(p1c,p2c,i)
        if self.settings["Show Scores"]: #Display Scores
            disp_scores(self)
        step=h/85 #Draw Middle of the Board
        for j in range(self.hit["0"]):
            if self.flipped:
                pygame.draw.ellipse(self.display,p1c[0],(width/2-bar_width/3,4*pt+h*0.08-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3,4*pt+h*0.08-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3+bar_width/6,4*pt+h*0.08-h/240+step*j,bar_width/3,h/40))
            else:
                pygame.draw.ellipse(self.display,p1c[0],(width/2-bar_width/3,height-3*pt-h*0.08-h/3+h*2/9-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3,height-3*pt-h*0.08-h/3+h*2/9-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3+bar_width/6,height-3*pt-h*0.08-h/3+h*2/9-h/240+step*j,bar_width/3,h/40))
        for j in range(self.hit["1"]):
            if self.flipped:
                pygame.draw.ellipse(self.display,p2c[0],(width/2-bar_width/3,height-3*pt-h*0.08-h/3+h*2/9-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3,height-3*pt-h*0.08-h/3+h*2/9-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3+bar_width/6,height-3*pt-h*0.08-h/3+h*2/9-h/240+step*j,bar_width/3,h/40))
            else:
                pygame.draw.ellipse(self.display,p2c[0],(width/2-bar_width/3,4*pt+h*0.08-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3,4*pt+h*0.08-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3+bar_width/6,4*pt+h*0.08-h/240+step*j,bar_width/3,h/40))
        for j in range(self.collected["1"]):
            if self.flipped:
                pygame.draw.ellipse(self.display,p1c[0],(width/2-bar_width/3,5*pt+h*0.08+h/9-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3,5*pt+h*0.08+h/9-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3+bar_width/6,5*pt+h*0.08+h/9-h/240+step*j,bar_width/3,h/40))
            else:
                pygame.draw.ellipse(self.display,p1c[0],(width/2-bar_width/3,height-4*pt-h*0.08-h/3-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3,height-4*pt-h*0.08-h/3-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p1c[1],(width/2-bar_width/3+bar_width/6,height-4*pt-h*0.08-h/3-h/240+step*j,bar_width/3,h/40))
        for j in range(self.collected["2"]):
            if self.flipped:
                pygame.draw.ellipse(self.display,p2c[0],(width/2-bar_width/3,height-4*pt-h*0.08-h/3-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3,height-4*pt-h*0.08-h/3-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3+bar_width/6,height-4*pt-h*0.08-h/3-h/240+step*j,bar_width/3,h/40))
            else:
                pygame.draw.ellipse(self.display,p2c[0],(width/2-bar_width/3,5*pt+h*0.08+h/9-h/60+step*j,bar_width*2/3,h/20))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3,5*pt+h*0.08+h/9-h/60+step*j,bar_width*2/3,h/20),int(h/400))
                pygame.draw.ellipse(self.display,p2c[1],(width/2-bar_width/3+bar_width/6,5*pt+h*0.08+h/9-h/240+step*j,bar_width/3,h/40))
        self.window.blit(self.display,(0,0))
        self.button_screen()
    def draw_stones(self,p1c,p2c,i,count=-1):
        tb = self.table
        disp_orientation=self.settings["Display Orientation"]
        if self.flipped: 
            disp_orientation="right" if disp_orientation=="left" else "left"
        if disp_orientation == "right": tb=self.table[0:12][::-1]+self.table[12:24][::-1]
        if self.flipped: tb=tb[::-1]
        pos = tb[i]
        if pos["player"]==1: c0,c1=p1c[0],p1c[1]
        if pos["player"]==2: c0,c1=p2c[0],p2c[1]
        a=pos["count"]
        count1=count
        b=a if a<5 else 5
        if count==-1 or count>a: count=b
        elif a>5: count=count-(a-5)
        for j in range(b-1,b-1-count,-1):
            if j<0:break
            m=i%6
            if i//6==0:
                pygame.draw.circle(self.display,c0,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m,4*pt+rad+2*rad*j),rad)
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m,4*pt+rad+2*rad*j),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m,4*pt+rad+2*rad*j),rad/2)
            if i//6==1:
                pygame.draw.circle(self.display,c0,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m+w+bar_width,4*pt+rad+2*rad*j),rad)
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m+w+bar_width,4*pt+rad+2*rad*j),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m+w+bar_width,4*pt+rad+2*rad*j),rad/2)
            if i//6==2:
                pygame.draw.circle(self.display,c0,(left+2*w+bar_width-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-rad-2*rad*j),rad)
                pygame.draw.circle(self.display,c1,(left+2*w+bar_width-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-rad-2*rad*j),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+2*w+bar_width-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-rad-2*rad*j),rad/2)
            if i//6==3:
                pygame.draw.circle(self.display,c0,(left+w-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-rad-2*rad*j),rad)
                pygame.draw.circle(self.display,c1,(left+w-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-rad-2*rad*j),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+w-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-rad-2*rad*j),rad/2)
        
        def draw_extra_stones(self,j):
            if j<0:return
            m=i%6
            j,d=j%4,{0:-1,1:0,2:1,3:0}
            if i//6==0:
                pygame.draw.circle(self.display,c0,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m,4*pt+9*rad+d[j]*pt/2),rad)
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m,4*pt+9*rad+d[j]*pt/2),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m,4*pt+9*rad+d[j]*pt/2),rad/2)
            if i//6==1:
                pygame.draw.circle(self.display,c0,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m+w+bar_width,4*pt+9*rad+d[j]*pt/2),rad)
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m+w+bar_width,4*pt+9*rad+d[j]*pt/2),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+rad+(w-12*rad)*(1+m)/7+(2*rad)*m+w+bar_width,4*pt+9*rad+d[j]*pt/2),rad/2)
            if i//6==2:
                pygame.draw.circle(self.display,c0,(left+2*w+bar_width-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-9*rad-d[j]*pt/2),rad)
                pygame.draw.circle(self.display,c1,(left+2*w+bar_width-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-9*rad-d[j]*pt/2),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+2*w+bar_width-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-9*rad-d[j]*pt/2),rad/2)
            if i//6==3:
                pygame.draw.circle(self.display,c0,(left+w-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-9*rad-d[j]*pt/2),rad)
                pygame.draw.circle(self.display,c1,(left+w-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-9*rad-d[j]*pt/2),rad,int(rad/10))
                pygame.draw.circle(self.display,c1,(left+w-rad-(w-12*rad)*(1+m)/7-(2*rad)*m,4*pt+h-9*rad-d[j]*pt/2),rad/2)
        if count1==-1:
            for j in range(a-5):
                draw_extra_stones(self,j)
        else:
            if count1==-1 or count1>a-6: count1=a-5
            for j in range(a-5-count1,a-5):
                draw_extra_stones(self,j)
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
            if player==1: m=24-min(positions)
            if player==2: m=1+max(positions)
            return [1,m]
        return -1
    def move(self, x1, x2):
        tb = self.table
        pc1 = tb[x1]
        player=pc1["player"]
        if player == 0 or pc1["count"] == 0:
            return -1
        if x2 in (-1,24) and self.check_all_in(player)!=-1:
            check = self.check_all_in(player)
            if check[0] != 1:
                return -1
            if (self.turn==1 and x2-x1 in self.dice2) or (self.turn==2 and x1-x2 in self.dice2):
                pc1["count"] -= 1
                if pc1["count"]==0: pc1["player"]=0
                self.collected[str(player)] += 1
                self.scores[str(player-1)] += abs(x1+1+25*(player-2))
                if player==1: self.dice2.remove(x2-x1)
                if player==2: self.dice2.remove(x1-x2)
                self.select[1] -= 1
                if self.select[1]==0: self.select = [-1,-1]
                self.display_table()
                self.move_dp=False
                self.draw_dice()
                self.window.blit(self.display,(0,0))
                self.button_screen()
                pygame.display.update()
                if self.scores[str(player-1)] == 375 or self.collected[str(player)] == 15:
                    self.over = True
                return 1
            mx=max(self.dice2)
            if mx>check[1]:
                pc1["count"] -= 1
                if pc1["count"]==0: pc1["player"]=0
                self.collected[str(player)] += 1
                self.scores[str(player-1)] += abs(x1+1+25*(player-2))
                self.dice2.remove(mx)
                self.select[1] -= 1
                if self.select[1]==0: self.select = [-1,-1]
                self.display_table()
                self.move_dp=False
                self.draw_dice()
                self.window.blit(self.display,(0,0))
                self.button_screen()
                pygame.display.update()
                if self.scores[str(player-1)] == 375 or self.collected[str(player)] == 15:
                    self.over = True
                return 1            
            return -1
        if not(x1 in range(24)) or not(x2 in range(24)):
            return -1
        if (self.turn==1 and x2-x1 in self.dice2) or (self.turn==2 and x1-x2 in self.dice2):
            pc2 = tb[x2]
            if self.hit[str(player-1)] != 0:
                return -1
            if (player == 1 and x1 >= x2) or (player == 2 and x1 <= x2):
                return -1
            if player == pc2["player"] or pc2["player"] == 0:
                pc1["count"] -= 1
                if pc1["count"]==0: pc1["player"]=0
                pc2["count"] += 1
                pc2["player"] = player
                self.scores[str(player-1)] += abs(x2-x1)
            elif player != pc2["player"]:
                if pc2["count"] > 1:
                    return -1
                elif pc2["count"] == 1:
                    self.hit[str(pc2["player"]-1)] += 1
                    self.scores[str(pc2["player"]-1)] -= abs(x2+1-25*(pc2["player"]-1))
                    pc1["count"] -= 1
                    if pc1["count"]==0: pc1["player"]=0
                    pc2["player"] = player
                    self.scores[str(player-1)] += abs(x2-x1)
                elif pc2["count"] == 0:
                    pc1["count"] -= 1
                    if pc1["count"]==0: pc1["player"]=0
                    pc2["count"] += 1
                    pc2["player"] = player
                    self.scores[str(player-1)] += abs(x2-x1)
            if player==1: self.dice2.remove(x2-self.select[0])
            if player==2: self.dice2.remove(self.select[0]-x2)
            self.select[1] -= 1
            if self.select[1]==0: self.select = [-1,-1]
            self.display_table()
            self.move_dp=False
            self.draw_dice()
            self.window.blit(self.display,(0,0))
            self.button_screen()
            pygame.display.update()
        else: return -1
    def place(self, player, x):
        tb = self.table
        placeAt = x+1
        if not(player in (1,2)): return -1
        if not(x in range(0,6)): return -1
        if player==2: x=23-x 
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
        self.dice2.remove(placeAt)
        self.display_table()
        self.move_dp=False
        self.draw_dice()
        self.window.blit(self.display,(0,0))
        self.button_screen()
        pygame.display.update()
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
            20 : {"(5,5)":1}, }
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
            20: [[5,5]] }
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
        for i in blocks:
            if tb[i]["count"]>2: probs[i]=0
        for i in range(24):
            probs[i] = f"%{int(round(100*probs[i]/36,0))}"
        return probs 
    def moveable_slots(self,p):
        tb=self.table
        moveable_slots=set()
        if all(num==self.dice2[0] for num in self.dice2) and len(self.dice2)>1:
            for n in range(len(self.dice2)):
                n=self.dice2[0]*(n+1)
                point=p+(3-2*self.turn)*n
                if self.flipped: point+=23-2*p
                if not(point in range(24)):
                    point=-1 if point<0 else 24
                    check=self.check_all_in(self.turn)
                    if check==-1: continue
                    if check[1]>abs(p-point):
                        if self.turn==1 and n!=24-p or self.turn==2 and n!=p+1:
                            continue
                    if self.flipped: moveable_slots.add(23-point)
                    else: moveable_slots.add(point)
                elif tb[point]["player"]!=self.turn and tb[point]["count"]>1:
                    break
                if self.flipped: moveable_slots.add(23-point)
                else: moveable_slots.add(point)
        else:
            for n in range(len(self.dice2)+1):
                if n<len(self.dice2): n=self.dice2[n]
                elif len(moveable_slots)!=0 and len(self.dice2)==2: n=sum(self.dice2)
                else: break
                point=p+(3-2*self.turn)*n
                if self.flipped: point+=23-2*p
                if not(point in range(24)):
                    point=-1 if point<0 else 24
                    check=self.check_all_in(self.turn)
                    if check==-1: continue
                    if check[1]>abs(p-point):
                        if self.turn==1 and n!=24-p or self.turn==2 and n!=p+1:
                            continue
                    if self.flipped: moveable_slots.add(23-point)
                    else: moveable_slots.add(point)
                elif tb[point]["player"]!=self.turn and tb[point]["count"]>1:
                    continue
                if self.flipped: moveable_slots.add(23-point)
                else: moveable_slots.add(point)
        if len(moveable_slots)==0: return -1
        else: return moveable_slots
    def draw_dice(self):
        if self.dice2==[]:
            self.waiting=False
            if self.settings["Flip Board"]:
                self.display_table()
                self.move_dp=False
                self.window.blit(self.display,(0,0))
                self.button_screen()
                pygame.display.update()
                time.sleep(0.5)
                self.flipped=not(self.flipped)
            self.turn = 3-self.turn
        else:
            sc_width = self.display.get_width()
            ft = pygame.font.SysFont("serif", sc_width//40)
            dctx=",".join(str(d) for d in dice)
            txs=pygame.font.Font.size(ft,dctx)
            col = (200,55,55) if self.turn==1 else (225,225,225)
            txcol = "white" if self.turn==1 else "black"
            dicetext=ft.render(dctx,True,txcol)
            pygame.draw.circle(self.display,col,(sc_width/2,2*pt+h/2+txs[1]/2),txs[1]*3/4)
            self.display.blit(dicetext,(sc_width/2-txs[0]/2,2*pt+h/2))
    def random_dice(self):
        if not self.waiting:
            global dice
            dice=[randint(1,6),randint(1,6)]
            if self.settings["Double Dice"]:
                r=randint(1,6)
                dice=[r,r]
            self.dice2=[dice[0],dice[1]]
            if dice[0]==dice[1]:
                self.dice2=[dice[0] for _ in range(4)]
            self.waiting=True
            self.display_table()
            self.move_dp=False
            self.draw_dice()
            self.window.blit(self.display, (0,0))
            self.button_screen()
    def settings_events(self):
        if not self.over:
            self.display_table()
            self.draw_dice()
            self.button_screen((215,85,45,200),1)
            self.window.blit(self.display,(0,0))
        height=self.display.get_height()
        width=self.display.get_width()
        bg_rect=pygame.Rect((width-bar_width-w)/2,height/2-h/4,w+bar_width,h/2)
        close_btn=pygame.Rect(bg_rect.right-bg_rect.width/12,bg_rect.top+bg_rect.width/60,bg_rect.width/15,bg_rect.width/15)
        center=close_btn.center; width=close_btn.width
        pygame.draw.rect(self.btn_surf,(164,151,151,240),bg_rect,0,int(w/40))
        self.draw_settings()
        pygame.draw.circle(self.btn_surf,"black",center,width/2,int(width/10))
        pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]-width/4),(center[0]+width/4,center[1]+width/4),int(bg_rect.width/150))
        pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]+width/4),(center[0]+width/4,center[1]-width/4),int(bg_rect.width/150))
        self.window.blit(self.btn_surf,(0,0))
        settings=True
        while settings:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==MOUSEBUTTONDOWN:
                    pos=pygame.mouse.get_pos()
                    if close_btn.collidepoint(pos):
                        if not self.over:
                            self.display_table()
                            self.draw_dice()
                            self.button_screen((215,85,45,200),1)
                        self.window.blit(self.display,(0,0))
                        pygame.draw.rect(self.btn_surf,(164,151,151,240),bg_rect,0,int(w/40))
                        self.draw_settings()
                        pygame.draw.circle(self.btn_surf,"black",center,width/2,int(width/10))
                        pygame.draw.circle(self.btn_surf,(255,30,30),center,width/2-int(width/10))
                        pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]-width/4),(center[0]+width/4,center[1]+width/4),int(bg_rect.width/150))
                        pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]+width/4),(center[0]+width/4,center[1]-width/4),int(bg_rect.width/150))
                        self.window.blit(self.btn_surf,(0,0))
                        settings=False
                        pygame.display.update()
                        time.sleep(0.2)
                        if not self.over:
                            self.display_table()
                            self.draw_dice()
                            self.button_screen((215,85,45,200),1)
                        self.window.blit(self.display,(0,0))
                        pygame.draw.rect(self.btn_surf,(164,151,151,240),bg_rect,0,int(w/40))
                        self.draw_settings()
                        pygame.draw.circle(self.btn_surf,"black",center,width/2,int(width/10))
                        pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]-width/4),(center[0]+width/4,center[1]+width/4),int(bg_rect.width/150))
                        pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]+width/4),(center[0]+width/4,center[1]-width/4),int(bg_rect.width/150))
                        self.window.blit(self.btn_surf,(0,0))
                        pygame.display.update()
                        time.sleep(0.1)
                        if not self.over:
                            self.display_table()
                            self.draw_dice()
                            self.window.blit(self.display,(0,0))
                            self.button_screen()
                            self.window.blit(self.btn_surf,(0,0))
                        else:
                            self.btn_surf.fill("white")
                            self.window.blit(self.btn_surf,(0,0))
                            self.disp_main()
                        pygame.display.update()
                        return
                    if self.setting_buttons[0].collidepoint(pos):
                        if self.settings["Display Orientation"]=="left": self.settings["Display Orientation"]="right"
                        else: self.settings["Display Orientation"]="left"
                    if self.setting_buttons[1].collidepoint(pos): self.settings["Show Scores"]=not(self.settings["Show Scores"])
                    if self.setting_buttons[2].collidepoint(pos): self.settings["Show Moves"]=not(self.settings["Show Moves"])
                    if self.setting_buttons[3].collidepoint(pos): self.settings["Flip Board"]=not(self.settings["Flip Board"])
                    if self.setting_buttons[4].collidepoint(pos): self.settings["debug"]=not(self.settings["debug"])
                    if self.setting_buttons[5].collidepoint(pos): self.settings["probs"]=not(self.settings["probs"])
                    if not self.over:
                        self.display_table()
                        self.draw_dice()
                        self.button_screen((215,85,45,200),1)
                    self.window.blit(self.display,(0,0))
                    pygame.draw.rect(self.btn_surf,(164,151,151,240),bg_rect,0,int(w/40))
                    self.draw_settings()
                    pygame.draw.circle(self.btn_surf,"black",center,width/2,int(width/10))
                    pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]-width/4),(center[0]+width/4,center[1]+width/4),int(bg_rect.width/150))
                    pygame.draw.line(self.btn_surf,"white",(center[0]-width/4,center[1]+width/4),(center[0]+width/4,center[1]-width/4),int(bg_rect.width/150))
                    self.window.blit(self.btn_surf,(0,0))
                pygame.display.update()
    def handle_events(self,event):
        self.random_dice()
        p1c=[(245,70,70),(200,55,55)]
        p2c=[(225,225,225),(190,190,190)]
        p1c_sel=[(255,120,120,220),(210,100,100,220)]
        p2c_sel=[(250,250,250,220),(120,210,210,220)]
        if event.type==MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.main_btn.collidepoint(pos):
                self.over=True
                self.button_screen((215,85,45,200),0)
                pygame.display.update()
                time.sleep(0.1)
                self.display_table()
                self.draw_dice()
                self.window.blit(self.display,(0,0))
                self.button_screen()
                pygame.display.update()
                time.sleep(0.3)
                self.display.fill("white")
                self.window.blit(self.display,(0,0))
                self.main_menu()
            if self.settings_btn.collidepoint(pos):
                self.settings_events()
            for j in range(26): #0,25
                if self.boxes[j].collidepoint(pos):
                    j=j-1 #-1,24
                    if self.flipped: j=23-j
                    if self.hit[str(self.turn-1)]!=0 and event.button==3:
                        if self.turn==1: j=j+1
                        if self.turn==2: j=24-j
                        if j in self.dice2:
                            self.place(self.turn,j-1)
                            break
                    if self.hit[str(self.turn-1)]!=0:
                        break
                    if j in range(24): #0,23
                        if self.table[j]["player"]!=self.turn and event.button==1:
                            self.select = [-1,-1]
                            self.display_table()
                            self.draw_dice()
                            self.move_dp=False
                            self.window.blit(self.display,(0,0))
                            self.button_screen()
                            break
                        if self.table[j]["player"]==self.turn and event.button==1:
                            k=j
                            disp_orientation=self.settings["Display Orientation"]
                            if self.flipped: 
                                disp_orientation="right" if disp_orientation=="left" else "left"
                            if disp_orientation == "right": 
                                if j<12: k=11-j
                                if j>=12: k=35-j
                            if self.select[0]!=j: 
                                self.move_dp=False
                                self.select[1]=0
                            self.select[0]=j
                            self.select[1]+=1
                            self.display_table(stones=False)
                            self.move_dp=False
                            for i in range(24): self.draw_stones(p1c,p2c,i)
                            if self.flipped: k=23-k
                            self.draw_stones(p1c_sel,p2c_sel,k,self.select[1])
                            self.draw_dice()
                            self.window.blit(self.display,(0,0))
                            self.button_screen()
                            break
                    if event.button==3 and self.select[0]!=-1:
                        for i in range(self.select[1]):
                            if self.dice2==[]:
                                self.select=[-1,-1]
                                break
                            self.move(self.select[0],j)
                        break
        if self.hit[str(self.turn-1)]!=0 and self.dice2!=[]: #Gele kontrolü
            t =[]
            for d in self.dice2:
                if self.turn==1: d=d-1
                if self.turn==2: d=24-d
                t.append(bool(self.table[d]["player"]==3-self.turn and self.table[d]["count"]>1))
            if all(t):
                pygame.display.update()
                time.sleep(1.5)
                self.dice2=[]
                if self.settings["Flip Board"]:
                    self.display_table()
                    self.move_dp=False
                    self.window.blit(self.display,(0,0))
                    self.button_screen()
                    pygame.display.update()
                    time.sleep(0.5)
                    self.flipped=not(self.flipped)
                self.turn = 3-self.turn
                self.waiting = False
                self.move_dp=False
                self.display_table()
                self.random_dice()
                self.window.blit(self.display,(0,0))
                self.button_screen()
    def check_stuck(self):
        if self.hit[str(self.turn-1)]!=0: return False    
        tb = self.table
        positions = set()
        for point in range(24):
            pc = tb[point]
            if pc["player"] == self.turn and pc["count"] > 0:
                positions.add(point)
        moveable_slots=set()
        for p in positions:
            slots=self.moveable_slots(p)
            if slots!=-1:
                for el in slots: moveable_slots.add(el)
        if len(moveable_slots)==0: return True
        else: return False
    def table_preset(self):
        tb = self.table
        self.scores = {"0": 0, "1": 0}
        for i in range(24):
            tb.append({"player": 0,"count": 0})
        # self.hit["0"]=1
        # tb[0]={"player": 1,"count": 2}
        # tb[6]={"player": 2,"count": 2}
        for i in range(6):
            tb[i]={"player":2, "count":2+i%2}
            tb[23-i]={"player":1, "count":2+i%2}
        for i in range(24):
            self.scores["1"]+=(24-i)*tb[i]["count"]
            self.scores["0"]+=(24-i)*tb[i]["count"]
        self.display_table()
    def play(self):
        if self.settings["custom board"]:
            self.table_preset()
        else:
            self.reset_table()
        global start
        start=False
        while self.waiting==False:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.starting_screen(event)
                pygame.display.update()
        self.waiting=False
        self.move_dp=False
        self.over=False
        while not(self.over):
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events(event)
                if self.settings["Show Moves"]:
                    if self.hit[str(self.turn-1)]==0:
                        sel=self.select[0]
                    elif self.turn==1: sel=-1
                    elif self.turn==2: sel=24
                    if self.flipped: sel=23-sel
                    moves=self.moveable_slots(sel)
                    if self.move_dp==False and moves!=-1 and (self.select[0]!=-1 or self.hit[str(self.turn-1)]!=0):
                        moves=list(moves)
                        for j in moves:
                            dist=abs(sel-j)
                            if self.check_all_in(self.turn)==-1 or j in range(24):
                                if not(dist in self.dice2):
                                    if self.hit[str(self.turn-1)]<2:
                                        pygame.draw.rect(self.display,(255,55,160,140),self.boxes[j+1])
                                    else: continue
                                else: pygame.draw.rect(self.display,(120,210,210,140),self.boxes[j+1])
                            elif dist in self.dice2:
                                pygame.draw.rect(self.display,(120,210,210,140),self.boxes[j+1])
                            elif dist==sum(self.dice2):
                                pygame.draw.rect(self.display,(255,55,160,140),self.boxes[j+1])
                            elif self.turn==1 and self.check_all_in(self.turn)[1]==24-self.select[0] and max(self.dice2)>self.check_all_in(self.turn)[1]:
                                pygame.draw.rect(self.display,(120,210,210,140),self.boxes[j+1])
                            elif self.turn==2 and self.check_all_in(self.turn)[1]==1+self.select[0] and max(self.dice2)>self.check_all_in(self.turn)[1]:
                                pygame.draw.rect(self.display,(120,210,210,140),self.boxes[j+1])
                        self.window.blit(self.display,(0,0))
                        self.button_screen()
                        self.move_dp=True                   
                pygame.display.update()
                if self.dice2!=[] and self.check_stuck():
                    time.sleep(1)
                    self.waiting = False
                    if self.settings["Flip Board"]:
                        self.display_table()
                        self.draw_dice()
                        self.move_dp=False
                        self.window.blit(self.display,(0,0))
                        self.button_screen()
                        pygame.display.update()
                        self.flipped=not(self.flipped)
                    self.turn = 3-self.turn
    def starting_screen(self,event):
        def reset_screen(self):
            self.display_table()
            pygame.draw.rect(start_surf,(164,151,151,240),bg,0,int(w/40))
            pygame.draw.rect(start_surf,"white",btn1,0,int(pad/2))
            pygame.draw.rect(start_surf,"white",btn2,0,int(pad/2))
            pygame.draw.rect(start_surf,"white",btnd,0,int(pad/2))
            start_surf.blit(txtitle,(bg.centerx-txtitle.get_width()/2,bg.top+pad))
            start_surf.blit(tx1,(btn1.left+pad,btn1.top+pad))
            start_surf.blit(tx2,(btn2.left+pad,btn2.top+pad))
            start_surf.blit(txd,(btnd.left+txd.get_width()/20,btnd.top+txd.get_height()/20))
        global start
        width=self.display.get_width()
        height=self.display.get_height()
        start_surf=pygame.Surface((width,height), pygame.SRCALPHA)
        bg=pygame.Rect(width/2-w*2/5,4*pt+h/3,w*4/5,h/3)
        txtitle=self.font.render("Who Will Start?",True,"black")
        tx1=self.font.render("Player 1",True,"black")
        tx2=self.font.render("Player 2",True,"black")
        txd=self.font.render("Random",True,"black")
        btn1=pygame.Surface.get_rect(tx1)
        btn2=pygame.Surface.get_rect(tx2)
        btnd=pygame.Rect(bg.center[0]-txd.get_width()*11/20,bg.center[1]-txd.get_height()*8/5,txd.get_width()*11/10,txd.get_height()*11/10)
        x,y=btn1.width,btn1.height
        pad=x/20
        btn1.left=bg.left+bg.width/2-x*8/5-pad; btn1.top=bg.top+bg.height*7/10-y-pad
        btn1.width+=2*pad; btn1.height+=2*pad;
        btn2.left=bg.left+bg.width/2+x*3/5-pad; btn2.top=bg.top+bg.height*7/10-y-pad
        btn2.width+=2*pad; btn2.height+=2*pad;
        select_color=(215,85,45,200)
        if not start: 
            pygame.draw.rect(start_surf,(164,151,151,240),bg,0,int(w/40))
            start_surf.blit(txtitle,(bg.centerx-txtitle.get_width()/2,bg.top+pad))
            start=True
        pygame.draw.rect(start_surf,"white",btn1,0,int(pad/2))
        pygame.draw.rect(start_surf,"white",btn2,0,int(pad/2))
        pygame.draw.rect(start_surf,"white",btnd,0,int(pad/2))
        start_surf.blit(tx1,(btn1.left+pad,btn1.top+pad))
        start_surf.blit(tx2,(btn2.left+pad,btn2.top+pad))
        start_surf.blit(txd,(btnd.left+txd.get_width()/20,btnd.top+txd.get_height()/20))
        if event.type==MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            if btn1.collidepoint(pos):
                pygame.draw.rect(start_surf,select_color,btn1,0,int(pad/2))
                self.window.blit(start_surf,(0,0))
                pygame.display.update()
                time.sleep(0.1)
                reset_screen(self)
                self.window.blit(start_surf,(0,0))
                pygame.display.update()
                time.sleep(0.3)
                self.turn=1
                self.display_table()
                self.waiting=True
            if btn2.collidepoint(pos):
                pygame.draw.rect(start_surf,select_color,btn2,0,int(pad/2))
                self.window.blit(start_surf,(0,0))
                pygame.display.update()
                time.sleep(0.1)
                reset_screen(self)
                self.window.blit(start_surf,(0,0))
                pygame.display.update()
                time.sleep(0.3)
                self.turn=2
                self.flipped=True
                self.display_table()
                self.waiting=True
            if btnd.collidepoint(pos):
                st_dice=[randint(1,6),randint(1,6)]
                ft = pygame.font.SysFont("serif", width//40)
                txd1=ft.render(str(st_dice[0]),True,"black")
                txd2=ft.render(str(st_dice[1]),True,"black")
                start_surf.blit(txd1,(btn1.left+(btn1.width-txd1.get_width())/2,btn1.top-txd1.get_height()*11/10))
                start_surf.blit(txd2,(btn2.left+(btn2.width-txd2.get_width())/2,btn2.top-txd2.get_height()*11/10))
                pygame.draw.rect(start_surf,select_color,btnd,0,int(pad/2))
                self.window.blit(start_surf,(0,0))
                pygame.display.update()
                time.sleep(0.1)
                reset_screen(self)
                start_surf.blit(txd1,(btn1.left+(btn1.width-txd1.get_width())/2,btn1.top-txd1.get_height()*11/10))
                start_surf.blit(txd2,(btn2.left+(btn2.width-txd2.get_width())/2,btn2.top-txd2.get_height()*11/10))
                self.window.blit(start_surf,(0,0))
                pygame.display.update()
                time.sleep(0.9)
                if st_dice[0]==st_dice[1]:
                    self.display_table()
                    start=False
                    return -1
                self.turn=1 if st_dice[0]>st_dice[1] else 2
                if self.turn==2: self.flipped=True
                self.display_table()
                self.waiting=True
        self.window.blit(start_surf,(0,0))
    def button_screen(self,col=0,button=-1):
        width=self.display.get_width()
        height=self.display.get_height()
        self.btn_surf=pygame.Surface((width,height), pygame.SRCALPHA)
        settings_btn=pygame.Rect(width-(width-w)/8,height/2-h/2,3*pt,3*pt)
        self.settings_btn=settings_btn
        main_text=self.font.render("Main Menu",True,"black")
        main_btn=main_text.get_rect(bottomleft=(width-main_text.get_width()-4*pt,height-5*pt+bar_width/2))
        main_btn.width+=pt; main_btn.height+=pt
        self.main_btn=main_btn
        if col!=0 and button==0:
            pygame.draw.rect(self.btn_surf,col,main_btn)
        if col!=0 and button==1:
            pygame.draw.rect(self.btn_surf,col,(settings_btn.left+settings_btn.width/10,settings_btn.top+settings_btn.width/10,settings_btn.width*0.9,settings_btn.width*0.9))
        center=settings_btn.center
        r=settings_btn.width/4
        icon_rect=pygame.Rect(center[0]-r,center[1]-r,r,r)
        self.btn_surf.blit(main_text,(main_btn.left+pt/2,main_btn.top+pt/2))
        pygame.draw.rect(self.btn_surf,"black",main_btn,2)
        pygame.draw.rect(self.btn_surf,"black",settings_btn,int(settings_btn.width/10))
        pygame.draw.circle(self.btn_surf,"black",center,r,int(r/2))
        tl=(center[0]-r/4,icon_rect.top-r/3)
        tr=(center[0]+r/4,icon_rect.top-r/3)
        bl=(center[0]-r/4,center[1]-r/2)
        br=(center[0]+r/4,center[1]-r/2)
        n,phi=8,math.pi/8
        def rotate(coord,center,angle):
            z=complex(coord[0]-center[0],coord[1]-center[1])*complex(math.cos(angle),math.sin(angle))
            return (z.real+center[0],z.imag+center[1])
        for i in range(n):
            x=i*2*math.pi/n+phi
            pygame.draw.polygon(self.btn_surf,"black",[rotate(tl,center,x),rotate(bl,center,x),rotate(br,center,x),rotate(tr,center,x)])
        self.window.blit(self.btn_surf,(0,0))
    def draw_settings(self):
        global pt, bar_width, h, w
        sc_size=self.display.get_size()
        topleft=[(sc_size[0]-bar_width-w)/2,sc_size[1]/2-h/4]
        bottomright=[(sc_size[0]+bar_width+w)/2,sc_size[1]/2+h/4]
        font = pygame.font.SysFont("serif", sc_size[0]//65)
        title=pygame.font.SysFont("serif",sc_size[0]//45).render("Settings",True,"black")
        tx1=font.render("Display Orientation:",True,"black")
        tx2=font.render("Show Scores:",True,"black")
        tx3=font.render("Show Moveable Points:",True,"black")
        tx4=font.render("Flip Board:",True,"black")
        tx5=font.render("Show Hitboxes:",True,"black")
        tx6=font.render("Show Probabilities:",True,"black")
        # tx7=font.render("Settings 7:",True,"black")
        height=tx1.get_height()
        mid=topleft[0]+2*pt+tx3.get_width()
        wd_height=bottomright[1]-topleft[1]
        sp=(wd_height-(7*height+6*pt))/2
        self.setting_buttons=[0 for _ in range(7)]
        for j in range(1,7): self.setting_buttons[j]=pygame.Rect(mid+pt,topleft[1]+sp+j*(height+pt),height,height)
        pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[1],int(height/10))
        pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[2],int(height/10))
        pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[3],int(height/10))
        pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[4],int(height/10))
        pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[5],int(height/10))
        # pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[6],int(height/10))
        if self.settings["Display Orientation"]=="left":
            tx=font.render("Left",True,"black")
            self.btn_surf.blit(tx,(mid+pt,topleft[1]+sp))
            self.setting_buttons[0]=pygame.Rect(mid+pt,topleft[1]+sp,tx.get_width(),tx.get_height())
        if self.settings["Display Orientation"]=="right":
            tx=font.render("Right",True,"black")
            self.btn_surf.blit(tx,(mid+pt,topleft[1]+sp))
            self.setting_buttons[0]=pygame.Rect(mid+pt,topleft[1]+sp,tx.get_width(),tx.get_height())
        if self.settings["Show Scores"]:
            pygame.draw.lines(self.btn_surf,(35,225,25),False,[(mid+pt+height*0.2,topleft[1]+sp+height+pt+height/2),(mid+pt+height/2,topleft[1]+sp+height+pt+height*0.8),(mid+pt+height*0.8,topleft[1]+sp+height+pt+height*0.2)],int(height/5))
        if self.settings["Show Moves"]:
            pygame.draw.lines(self.btn_surf,(35,225,25),False,[(mid+pt+height*0.2,topleft[1]+sp+2*(height+pt)+height/2),(mid+pt+height/2,topleft[1]+sp+2*(height+pt)+height*0.8),(mid+pt+height*0.8,topleft[1]+sp+2*(height+pt)+height*0.2)],int(height/5))
        if self.settings["Flip Board"]:
            pygame.draw.lines(self.btn_surf,(35,225,25),False,[(mid+pt+height*0.2,topleft[1]+sp+3*(height+pt)+height/2),(mid+pt+height/2,topleft[1]+sp+3*(height+pt)+height*0.8),(mid+pt+height*0.8,topleft[1]+sp+3*(height+pt)+height*0.2)],int(height/5))
        if self.settings["debug"]:
            pygame.draw.lines(self.btn_surf,(35,225,25),False,[(mid+pt+height*0.2,topleft[1]+sp+4*(height+pt)+height/2),(mid+pt+height/2,topleft[1]+sp+4*(height+pt)+height*0.8),(mid+pt+height*0.8,topleft[1]+sp+4*(height+pt)+height*0.2)],int(height/5))
        if self.settings["probs"]:
            pygame.draw.lines(self.btn_surf,(35,225,25),False,[(mid+pt+height*0.2,topleft[1]+sp+5*(height+pt)+height/2),(mid+pt+height/2,topleft[1]+sp+5*(height+pt)+height*0.8),(mid+pt+height*0.8,topleft[1]+sp+5*(height+pt)+height*0.2)],int(height/5))
        self.btn_surf.blit(title,((bottomright[0]+topleft[0]-title.get_width())/2,topleft[1]))
        self.btn_surf.blit(tx1,(mid-tx1.get_width(),topleft[1]+sp))
        self.btn_surf.blit(tx2,(mid-tx2.get_width(),topleft[1]+sp+height+pt))
        self.btn_surf.blit(tx3,(mid-tx3.get_width(),topleft[1]+sp+2*(height+pt)))
        self.btn_surf.blit(tx4,(mid-tx4.get_width(),topleft[1]+sp+3*(height+pt)))
        self.btn_surf.blit(tx5,(mid-tx5.get_width(),topleft[1]+sp+4*(height+pt)))
        self.btn_surf.blit(tx6,(mid-tx6.get_width(),topleft[1]+sp+5*(height+pt)))
        # self.btn_surf.blit(tx7,(mid-tx7.get_width(),topleft[1]+sp+6*(height+pt)))
        if self.settings["debug"]: pygame.draw.rect(self.btn_surf,"black",self.setting_buttons[0],2)
    def disp_main(self):
        size=self.display.get_size()
        sc_rect=pygame.Rect(size[0]*0.35,size[1]/5,size[0]*0.3,size[1]*3/5)
        title=pygame.font.SysFont("serif",size[0]//40).render("Backgammon",True,"black")
        play_text=pygame.font.SysFont("serif",size[0]//45).render("Play",True,"black")
        play_btn=play_text.get_rect(center=(sc_rect.centerx,sc_rect.top+4*title.get_height()))
        play_btn=pygame.Rect(play_btn.left-size[0]/200,play_btn.top-size[0]/200,play_btn.width+size[0]/100,play_btn.height+size[0]/100)
        settings_text=pygame.font.SysFont("serif",size[0]//45).render("Settings",True,"black")
        settings_btn=settings_text.get_rect(center=(sc_rect.centerx,sc_rect.top+4*title.get_height()+1.5*play_btn.height))
        settings_btn=pygame.Rect(settings_btn.left-size[0]/200,settings_btn.top-size[0]/200,settings_btn.width+size[0]/100,settings_btn.height+size[0]/100)
        pygame.draw.rect(self.display,(164,151,151,240),sc_rect)
        pygame.draw.rect(self.display,"black",sc_rect,int(size[0]/250))
        self.display.blit(title,(sc_rect.centerx-title.get_width()/2,sc_rect.top+sc_rect.height/50))
        pygame.draw.rect(self.display,"white",play_btn,0,10)
        pygame.draw.rect(self.display,"white",settings_btn,0,10)
        self.display.blit(play_text,(play_btn.left+size[0]/200,play_btn.top+size[0]/200))
        self.display.blit(settings_text,(settings_btn.left+size[0]/200,settings_btn.top+size[0]/200))
        self.window.blit(self.display,(0,0))
    def main_menu(self):
        size=self.display.get_size()
        sc_rect=pygame.Rect(size[0]*0.35,size[1]/5,size[0]*0.3,size[1]*3/5)
        title=pygame.font.SysFont("serif",size[0]//40).render("Backgammon",True,"black")
        play_text=pygame.font.SysFont("serif",size[0]//45).render("Play",True,"black")
        play_btn=play_text.get_rect(center=(sc_rect.centerx,sc_rect.top+4*title.get_height()))
        play_btn=pygame.Rect(play_btn.left-size[0]/200,play_btn.top-size[0]/200,play_btn.width+size[0]/100,play_btn.height+size[0]/100)
        settings_text=pygame.font.SysFont("serif",size[0]//45).render("Settings",True,"black")
        settings_btn=settings_text.get_rect(center=(sc_rect.centerx,sc_rect.top+4*title.get_height()+1.5*play_btn.height))
        settings_btn=pygame.Rect(settings_btn.left-size[0]/200,settings_btn.top-size[0]/200,settings_btn.width+size[0]/100,settings_btn.height+size[0]/100)
        pygame.draw.rect(self.display,(164,151,151,240),sc_rect)
        pygame.draw.rect(self.display,"black",sc_rect,int(size[0]/250))
        self.display.blit(title,(sc_rect.centerx-title.get_width()/2,sc_rect.top+sc_rect.height/50))
        pygame.draw.rect(self.display,"white",play_btn,0,10)
        pygame.draw.rect(self.display,"white",settings_btn,0,10)
        self.display.blit(play_text,(play_btn.left+size[0]/200,play_btn.top+size[0]/200))
        self.display.blit(settings_text,(settings_btn.left+size[0]/200,settings_btn.top+size[0]/200))
        self.window.blit(self.display,(0,0))
        while True:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==MOUSEBUTTONDOWN:
                    pos=pygame.mouse.get_pos()
                    if play_btn.collidepoint(pos):
                        pygame.draw.rect(self.display,(215,85,45),play_btn,0,10)
                        self.display.blit(play_text,(play_btn.left+size[0]/200,play_btn.top+size[0]/200))
                        self.window.blit(self.display,(0,0))
                        pygame.display.update()
                        time.sleep(0.1)
                        pygame.draw.rect(self.display,"white",play_btn,0,10)
                        self.display.blit(play_text,(play_btn.left+size[0]/200,play_btn.top+size[0]/200))
                        self.window.blit(self.display,(0,0))
                        pygame.display.update()
                        time.sleep(0.3)
                        self.play()
                    if settings_btn.collidepoint(pos):
                        pygame.draw.rect(self.display,(215,85,45),settings_btn,0,10)
                        self.display.blit(settings_text,(settings_btn.left+size[0]/200,settings_btn.top+size[0]/200))
                        self.window.blit(self.display,(0,0))
                        pygame.display.update()
                        time.sleep(0.1)
                        pygame.draw.rect(self.display,"white",settings_btn,0,10)
                        self.display.blit(settings_text,(settings_btn.left+size[0]/200,settings_btn.top+size[0]/200))
                        self.window.blit(self.display,(0,0))
                        pygame.display.update()
                        time.sleep(0.3)
                        self.btn_surf.fill("white")
                        self.display.fill("white")
                        self.window.blit(self.display,(0,0))
                        pygame.display.update()
                        self.settings_events()
                pygame.display.update()
if __name__=="__main__":
    Game().main_menu()