from logic import *
from utils import *


f = open("input.txt","r")
inp = f.readlines()
print(inp)

p = open("percepts.txt", "r")
percepts = p.readlines()

class box:
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self. status = 0

#Building the grid
env = []
l = []
percept_mat = []

for i in range(int(inp[0])):
    for j in range(int(inp[0])):
        ob = box(i+1,j+1)
        l.append(ob)
    env.append(l)
    l=[]


wumpus_kb = PropKB()

#Initial Knowledge

P11, P12, P21, P22, P31, B11, B21 = expr('P11, P12, P21, P22, P31, B11, B21') 

wumpus_kb.tell(~P11)
wumpus_kb.tell(B11 | '<=>' | ((P12 | P21)))
wumpus_kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))
wumpus_kb.tell(~B11)

print(wumpus_kb.clauses)

print(wumpus_kb.ask_if_true(~P12))
print(wumpus_kb.ask_if_true(~P21))
