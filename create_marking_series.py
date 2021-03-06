import pygame
import math
from pygame.constants import *
from data import *
from re import *
#functions to make a marking
def runtrans(graph,marking,namelist):
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    screen.fill(light_fill)  
    font = pygame.font.SysFont('Times New Roman', 20,True,False)
    build_edges(graph)
    ptr=0
    for n1, n2 in edges:
        if ptr%2==1:
            end=((graph[n1][0][0]*4/10+graph[n2][0][0]*6/10),(graph[n1][0][1]*4/10+graph[n2][0][1]*6/10))
            pygame.draw.line(screen, dark, graph[n1][0], end, 7)      
            rotation = math.degrees(math.atan2(graph[n1][0][1]-end[1], end[0]-graph[n1][0][0]))+90
            pygame.draw.polygon(screen, dark, ((end[0]+15*math.sin(math.radians(rotation)), end[1]+15*math.cos(math.radians(rotation))), (end[0]+15*math.sin(math.radians(rotation-120)), end[1]+15*math.cos(math.radians(rotation-120))), (end[0]+15*math.sin(math.radians(rotation+120)), end[1]+15*math.cos(math.radians(rotation+120))))) 
        else:
            start=((graph[n1][0][0]*27/35+graph[n2][0][0]*8/35),(graph[n1][0][1]*27/35+graph[n2][0][1]*8/35))
            pygame.draw.line(screen, dark, start, graph[n2][0], 7)  
        ptr=ptr+1
    ptr = 0
    # loop to draw node
    for centerxy in graph:
        name = font.render(namelist[ptr], False, black)
        if(centerxy[2] == 1):
            pygame.draw.circle(screen,
                               dark, centerxy[0], 30,7)
            screen.blit(name, (centerxy[0][0]-20, centerxy[0][1]-10))

        else:
            screen.blit(name, (centerxy[0][0]+5, centerxy[0][1]-20))
        ptr = ptr+1
    mark="Input state:("+ str(marking[0])+' '+str(marking[2])+' '+str(marking[4])+')'
    overflow="Too many states to be visualized! "
    if(marking[0]>=2 or marking[2]>=2or marking[4]>=2):
        mark=overflow+mark
    markul=font.render(mark,False,black)
    screen.blit(markul,(60,500))
    pygame.display.update()
    while True:
        if pygame.event.peek(pygame.QUIT):
            quit()

def run(graph, marking, namelist, executed,times):
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Petri net visualization')
    screen.fill(light_fill)  
    font = pygame.font.SysFont('Times New Roman', 20)
    build_edges(graph)
    for n1, n2 in edges:
        start=((graph[n1][0][0]*27/35+graph[n2][0][0]*8/35),(graph[n1][0][1]*27/35+graph[n2][0][1]*8/35))
        end=((graph[n1][0][0]*3/10+graph[n2][0][0]*7/10),(graph[n1][0][1]*3/10+graph[n2][0][1]*7/10))
        pygame.draw.line(screen, dark, start, end, 7)   
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(screen, dark, ((end[0]+20*math.sin(math.radians(rotation)), end[1]+20*math.cos(math.radians(rotation))), (end[0]+20*math.sin(math.radians(rotation-120)), end[1]+20*math.cos(math.radians(rotation-120))), (end[0]+20*math.sin(math.radians(rotation+120)), end[1]+20*math.cos(math.radians(rotation+120)))))    
    ptr = 0
    # loop to draw node
    for centerxy in graph:
        if(centerxy[2] == 1):
            pygame.draw.circle(screen,
                               dark, centerxy[0], radius,7)
            tokens(marking[ptr], centerxy[0], screen)
        else:
            if(marking[ptr] == 0):
                pygame.draw.rect(
                    screen, light_grey, (centerxy[0][0]-15, centerxy[0][1]-35, 30, 70))
            else:
                pygame.draw.rect(
                    screen, green, (centerxy[0][0]-15, centerxy[0][1]-35, 30, 70))
        name = font.render(namelist[ptr], False, black)
        screen.blit(name, (centerxy[0][0]-50, centerxy[0][1]+50))
        ptr = ptr+1
    font2 = pygame.font.SysFont('Times New Roman', 20)
    warn = "Press any key to pause\\unpause"
    outp = "Firings executed: " + str(executed)
    warnoutp = font2.render(warn, False, black)
    output = font2.render(outp, False, black)
    markul = makemark(marking, namelist)
    marked = font2.render("Curent marking: " + markul, False, black)
    screen.blit(output, (60, 500))
    screen.blit(marked, (60, 525))
    screen.blit(warnoutp, (60, 550))
    pause = True
    for ev in pygame.event.get():
        if ev.type == KEYDOWN or executed+times==0:
            pause = "Screen is paused"
            pausecall = font2.render(pause, False, black)
            screen.blit(pausecall, (60, 575))
            pygame.display.update()
            while pause:
                for ef in pygame.event.get():
                    if ef.type == KEYDOWN:
                        pause = False
                    elif ef.type==QUIT:
                        quit()
        elif ev.type==QUIT:
            quit()
        if pause == False:
            pause = True
            break
    pygame.display.update()
    pygame.time.delay(750)


def build_edges(graph):
    global edges
    edges = {}
    for n1, (_, adjacents, _) in enumerate(graph):
        for n2 in adjacents:
            eid = (n1,n2)
            if eid not in edges:
                edges[eid] = (n1, n2)


def tokens(number, center, screen):
    if(number == 0):
        pass
    elif(number == 1):
        pygame.draw.circle(screen, black, center, 7)
    elif(number == 2):
        pygame.draw.circle(screen, black, (center[0], center[1]-20), 7)
        pygame.draw.circle(screen, black, (center[0], center[1]+20), 7)
    elif(number == 3):
        pygame.draw.circle(screen, black, center, 7)
        pygame.draw.circle(screen, black, (center[0], center[1]-18), 7)
        pygame.draw.circle(screen, black, (center[0], center[1]+18), 7)
    elif(number == 4):
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-18), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-18), 7)
    elif(number == 5):
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-18), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-18), 7)
        pygame.draw.circle(screen, black, center, 7)
    elif(number == 6):
        pygame.draw.circle(screen, black, (center[0]-13, center[1]), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-18), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-18), 7)
    elif(number == 7):
        pygame.draw.circle(screen, black, (center[0]-13, center[1]), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-18), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+18), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-18), 7)
        pygame.draw.circle(screen, black, (center[0], center[1]-7), 7)
    elif(number == 8):
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+7), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+23), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-7), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-23), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+7), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+23), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-7), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-23), 7)
    elif(number == 9):
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+7), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]+23), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-7), 7)
        pygame.draw.circle(screen, black, (center[0]-13, center[1]-23), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+7), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]+23), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-7), 7)
        pygame.draw.circle(screen, black, (center[0]+13, center[1]-23), 7)
        pygame.draw.circle(screen, black, center, 7)
    else:
        font = pygame.font.SysFont('Times New Roman', 30)
        numbe = font.render(str(number), False, black)
        screen.blit(numbe, (center[0]-15, center[1]-15))

##fucntion to make series of markings


def runmarking(graph, mark, type, namelist):
    i = 0
    start_fire = 0  # 0 means turns on trans, 1 means changes place
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Petri net visualization')
    screen.fill(light_fill)
    font0 = pygame.font.SysFont('Times New Roman', 40,True,False)
    first = "Press any button to start"
    begin = font0.render(first, False, black)
    screen.blit(begin, (320, 280))
    pygame.display.update()
    ready = True
    while ready:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                pygame.time.delay(1000)
                ready = False
                break
            elif ev.type== QUIT:
                quit()
    if(type==2):
        runtrans(graph,mark,namelist)    
    run(graph, mark, namelist, i,start_fire)
    while True:
        if(type == 0):
            if(mark[0] > 0 and mark[2] == 0):
                if(start_fire == 0):
                    mark[1] = 1
                    start_fire = 1
                else:
                    mark[0] = mark[0]-1
                    if(mark[0] == 0):
                        mark[1] = 0
                    else:
                        mark[1] = 1
                    mark[2] = 1
                    i = i+1
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
            elif(mark[0] > 0 and mark[2] > 0):
                if(start_fire == 0):
                    mark[1] = 1
                    mark[3] = 1
                    start_fire = 1
                else:
                    mark[0] = mark[0]-1
                    if(mark[0] == 0):
                        mark[1] = 0
                    mark[4] = mark[4]+1
                    i = i+2
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
            elif(mark[0] == 0 and mark[2] > 0):
                if(start_fire == 0):
                    mark[3] = 1
                    start_fire = 1
                else:
                    mark[2] = mark[2]-1
                    mark[4] = mark[4]+1
                    if(mark[2] == 0):
                        mark[3] = 0
                    i = i+1
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
            else:
                break
        elif type == 1:
            if mark[0] == 1:
                if(start_fire == 0):
                    mark[1] = 1
                    start_fire = 1
                else:
                    mark[0] = 0
                    mark[1] = 0
                    mark[2] = 1
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
                    i = i+1
            elif mark[2] == 1:
                if(start_fire == 0):
                    mark[3] = 1
                    start_fire = 1
                else:
                    mark[4] = 1
                    mark[2] = 0
                    mark[3] = 0
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
                    i = i+1
            elif mark[4] == 1:
                if(start_fire == 0):
                    mark[5] = 1
                    start_fire = 1
                else:
                    mark[0] = 1
                    mark[5] = 0
                    mark[4] = 0
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
                    i = i+1
            else:
                break
        else:
            if(mark[6] == 1):
                if(mark[0] == 0 and start_fire != 1):
                    break
                if start_fire == 0:
                    mark[1] = 1
                    start_fire = 1
                elif start_fire == 1:
                    mark[0] = mark[0]-1
                    mark[2] = 1
                    mark[6] = 0
                    mark[7] = 1
                    mark[1] = 0
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
                    i = i+1
            elif(mark[7] == 1):
                if start_fire == 0:
                    mark[3] = 1
                    start_fire = 1
                elif start_fire == 1:
                    mark[8] = mark[8]+1
                    mark[2] = 0
                    mark[7] = 0
                    mark[4] = 1
                    mark[3] = 0
                    start_fire = 0
                    markul = makemark(mark, namelist)
                    print(markul)
                    i = i+1
                else:
                    break
            elif mark[4] == 1 and not mark[2] == 1:
                if(start_fire == 0):
                    start_fire = 1
                    mark[5] = 1
                else:
                    start_fire = 0
                    mark[5] = 0
                    mark[4] = 0
                    mark[6] = 1
                    i = i+1
                    markul = makemark(mark, namelist)
                    print(markul)
            else:
                break
        run(graph, mark, namelist, i,start_fire)

#function to check input


def check(stringg, which):
    type = []
    txt_patient = "\\[(((([2-9]|10).)?wait)|((([2-9]|[1-9][0-9]+).)?(inside|done)))(,(((([2-9]|10).)?wait)|((([2-9]|[1-9][0-9]+).)?(inside|done))))*\\]"
    txt_spec = "\\[(free|busy|docu)\\]"
    txt_trans="([0-9]|[1-9][0-9]+) ([0-9]|[1-9][0-9]+) ([0-9]|[1-9][0-9]+)"
    txt_merge = "\\[(((([2-9]|10).)?wait)|inside|free|busy|docu|(([2-9]|[1-9][0-9]+).)?done)(,(((([2-9]|10).)?wait)|inside|free|busy|docu|(([2-9]|[1-9][0-9]+).)?done))*\\]"
    if(which == 0 and fullmatch(txt_patient, stringg) != None):
        type = [0, 0, 0, 0, 0]
        strin = stringg[1:-1]
        x = split(",", strin)
        for mark in x:
            if(mark.count("wait") != 0 and type[0] == 0):
                if(mark == "wait"):
                    type[0] = 1
                else:
                    type[0] = int(mark[0:mark.find(".")])
            elif(mark.count("inside") != 0 and type[2] == 0):
                if(mark == "inside"):
                    type[2] = 1
                else:
                    type[2] = int(mark[0:mark.find(".")])
            elif(mark.count("done") != 0 and type[4] == 0):
                if(mark == "done"):
                    type[4] = 1
                else:
                    type[4] = int(mark[0:mark.find(".")])
            else:
                type = []
                return type
    elif(which == 1 and fullmatch(txt_spec, stringg) != None):
        type = [0, 0, 0, 0, 0, 0]
        strin = stringg[1:-1]
        if(strin == "free"):
            type[0] = 1
        elif(strin == "busy"):
            type[2] = 1
        elif(strin == "docu"):
            type[4] = 1
        else:
            type = []
            return type
    elif(which == 3 and fullmatch(txt_merge, stringg)):
        type = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        strin = stringg[1:-1]
        x = split(",", strin)
        for mark in x:
            if(mark.count("wait") != 0 and type[0] == 0):
                if(mark == "wait"):
                    type[0] = 1
                else:
                    type[0] = int(mark[0:mark.find(".")])
            elif mark == "inside" and type[2] == 0:
                type[2] = 1
            elif mark.count("done") and type[8] == 0:
                if(mark == "done"):
                    type[8] = 1
                else:
                    type[8] = int(mark[0:mark.find(".")])
            elif mark == "free" and type[6] == 0:
                type[6] = 1
            elif mark == "busy" and type[7] == 0:
                type[7] = 1
            elif mark == "docu" and type[4] == 0:
                type[4] = 1
            else:
                type = []
                return type
        if(not((type[2] == type[7])) or type[2]+type[6]+type[4] != 1):
            type = []
            return type
    elif(which==2 and fullmatch(txt_trans,stringg)):
        type=[0,0,0,0,0,0]
        x= split(' ',stringg)
        type[0]=int(x[0])
        type[2]=int(x[1])
        type[4]=int(x[2])
    return type

#function to make marking


def makemark(dataline, namelist):
    re = "["
    init = 0
    while(init < len(dataline)):
        wat = namelist[init]
        if(dataline[init] == 0):
            pass
        elif(dataline[init] == 1):
            re = re+wat.lower()+','
        else:
            re = re+str(dataline[init])+"."+wat.lower()+','
        if(init >= 6):
            init = init+1
        else:
            init = init+2
    re = re[:-1]
    re = re+"]"
    return re
