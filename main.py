import create_marking_series
import pygame
from data import *
callout = """Choose type of Petri net: 
Press 0 to access patient net;
      1 to access specialist net;
      2 to access merge net
Or type the word "exit"(no quotation) to quit program."""
print(callout)
choice=-999
get=input()
choice=0
while True:
    try:
        choice=int(get)
    except ValueError :
        get=input("Wrong input! Please type again or type \"exit\"(no quotation) to quit program: ")
        if(get=="exit"):
            quit() 
        continue
    if(choice<0 or choice>2):
        get=input("Wrong input! Please type again or type \"exit\"(no quotation) to quit program: ")
        continue
    break          
choice=int(get)
get=input("Input number of desired firings(min value will be 0): ")
fires= 0
while True:
    try:
        fires=int(get)
    except ValueError:
        get=input("Wrong input! Please type again or type \"exit\"(no quotation) to quit program: ")
        if(get=="exit"):
            quit() 
        continue
    break          
fires=int(get)

if(fires<0):
    fires=0
graph_chosen=[]
name_chosen=[]
if(choice==0):
    graph_chosen=graph_patient
    name_chosen=name_patient
elif(choice==1):
    print("We will consider there is only one specialist.")
    graph_chosen=graph_spec
    name_chosen=name_spec
else:
    graph_chosen=graph_merge
    name_chosen=name_merge
string=input("Please input marking: ")
dataline=create_marking_series.check(string,choice)
while True:
    if(dataline):
        break
    else:
        string=input("Wrong marking! Please input again or type \"exit\" to quit program: ")
        if(string=="exit"):
            quit()
        dataline=create_marking_series.check(string, choice)
create_marking_series.runmarking(graph_chosen,fires,dataline,choice,name_chosen)
while 1:  
    if pygame.event.peek(pygame.QUIT):
        break