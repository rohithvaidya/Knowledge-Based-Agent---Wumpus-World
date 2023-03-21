from logic import *
from utils import *
import random


def WalkSAT(clauses, p=0.5, max_flips=10000):
    """Checks for satisfiability of all clauses by randomly flipping values of variables
    """
    # Set of all symbols in all clauses
    symbols = {sym for clause in clauses for sym in prop_symbols(clause)}
    # model is a random assignment of true/false to the symbols in clauses
    model = {s: random.choice([True, False]) for s in symbols}
    for i in range(max_flips):
        satisfied, unsatisfied = [], []
        for clause in clauses:
            (satisfied if pl_true(clause, model) else unsatisfied).append(clause)
        if not unsatisfied:  # if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(list(prop_symbols(clause)))
        else:
            # Flip the symbol in clause that maximizes number of sat. clauses
            def sat_count(sym):
                # Return the the number of clauses satisfied after flipping the symbol.
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause, model)])
                model[sym] = not model[sym]
                return count
            sym = argmax(prop_symbols(clause), key=sat_count)
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None


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


cnf_clauses = []

for i in wumpus_kb.clauses:
    cnf_clauses.append(to_cnf(i))


print(WalkSAT(cnf_clauses))