import create_marking_series
import pygame
from data import *
print("""Choose type of Petri net: 
Press 0 to access patient net;
      1 to access specialist net;
      2 to access specialist transition system;
      3 to access merged net.
Or type the word "exit"(no quotation) to quit program.""")
get = input()
choice = 0
while True:
    try:
        choice = int(get)
    except ValueError:
        get = input(
            "Wrong input! Please type again or type \"exit\"(no quotation) to quit program: ")
        if get == "exit":
            quit()
        continue
    if choice < 0 or choice > 2:
        get = input(
            "Wrong input! Please type again or type \"exit\"(no quotation) to quit program: ")
        continue
    break
choice = int(get)
graph_chosen = []
name_chosen = []
if choice == 0 :
    graph_chosen = graph_patient
    name_chosen = name_patient
elif choice == 1 or choice==2:
    if choice==1:
        print("We will consider there is only one specialist.")
        graph_chosen = graph_spec
    else: 
        graph_chosen=graph_trans
    name_chosen = name_spec
else:
    graph_chosen = graph_merge
    name_chosen = name_merge
dataline=[]
mark_inp = input("Please input marking: ")
dataline = create_marking_series.check(mark_inp, choice)
while True:
    if dataline:
        break
    else:
        mark_inp = input("Wrong marking! Please input again or type \"exit\"(no quotation) to quit program: ")
        if mark_inp == "exit":
            quit()
        dataline = create_marking_series.check(mark_inp, choice)
create_marking_series.runmarking(graph_chosen, dataline, choice, name_chosen)
while True:
    if pygame.event.peek(pygame.QUIT):
        break
