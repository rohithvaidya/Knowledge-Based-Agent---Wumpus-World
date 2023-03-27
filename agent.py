from dpll_solver import *

grid= []
graph = {}       

def build_grid_adjacency_list():
    #Building the grid
    l=[]
    ctr = 0
    
    for i in range(4):
        for j in range(4):
            ob = box()
            ob.id = ctr
            if((str(env[i][j]).isalpha()) and ("," not in env[i][j])):
                ob.percept.append(env[i][j])
            elif("," in str(env[i][j])):
                ob.percept.extend(env[i][j].split(",")) 
            else:
                pass
            l.append(ob)
            ctr+=1
        grid.append(l)
        l=[]

    #Building Adjancency List
    
    l = []
    for i in range(4):
        for j in range(4):
            if(j+1 < 4):
                l.append(grid[i][j+1])
                graph[grid[i][j]] = l
            if(i+1 < 4):
                l.append(grid[i+1][j])
                graph[grid[i][j]] = l
            if(i-1>=0):
                l.append(grid[i-1][j])
                graph[grid[i][j]] = l
            if(j-1>=0):
                l.append(grid[i][j-1])
                graph[grid[i][j]] = l
            l = []


def check_all_literals():
    all_lit = []
    for i in KB:
        for j in i:
            all_lit.append(j[0])      
    for i in all_lit:
        if i not in assignments.keys():
            return 0
    return 1

KB = []

p = open("percepts.txt", "r")
percepts = p.readlines()

start_pos = 0

"""env = [[0, "b", "P", "b"],
        ["s", 5, "b", 7],
        ["W", "b,s", "P", "b"],
        ["s", 13, "b", "G"]]"""

env = [[0, "b", "P", "b"],
        ["s", 5, "b", 7],
        ["W", "s,shoot", 10, 11],
        ["s", 13, 14, "G"]]



class box:
    def __init__(self):
        self.id = 0
        self. ok = 0
        self.percept = []
        self.parent = None

build_grid_adjacency_list()

#Intial Conditions for KB - Literals are P, W
KB.append({("P0", False)})
KB.append({("W0", False)})
#KB.append({("W1", False)})
#KB.append({("P1", False)})
#KB.append({("W4", False)})
#KB.append({("P4", False)})


visited = set() 
stack = [grid[0][0]]
#visited.add(0)

sat = None
assignments = None

while(stack!=[]):
    top = stack.pop()
    
    if(top.id not in visited):
        #Visiting the Cell
        print(top.id)
        top.ok = 1
        formula = set()
        #Getting Percept
        print("Percept", top.percept)
        if("s" not in top.percept):
            for i in graph[top]:
                if(i.id not in visited):
                    formula.add(("W{}".format(i.id), False))
                    KB.append(formula)
                    formula = set()

        if("b" not in top.percept):
            for i in graph[top]:
                if(i.id not in visited):
                    formula.add(("P{}".format(i.id), False))
                    KB.append(formula)
                    formula = set()

        if("s" in top.percept):
            for i in graph[top]:
                
                if(i.id not in visited):
                    formula.add(("W{}".format(i.id), True))
            KB.append(formula)
            formula = set()

        if("b" in top.percept):
            for i in graph[top]:
                if(i.id not in visited):
                    formula.add(("P{}".format(i.id), True))
            KB.append(formula)
            formula = set()
        
        #Death Conditions
        if("P" in top.percept):
            formula.add(("P{}".format(top.id), True))
            KB.append(formula)
            formula = set()

            formula.add(("W{}".format(top.id), False))
            KB.append(formula)
            formula = set()
            
            print("Reset")
            visited = set()
            stack = [grid[0][0]]

        if("W" in top.percept):
            formula.add(("W{}".format(top.id), True))
            KB.append(formula)
            formula = set()

            formula.add(("P{}".format(top.id), False))
            KB.append(formula)
            formula = set()

            print("Agent Killed by Wumpus")
            

        if("G" in top.percept):
            print("Gold Found")
            exit()

        if("shoot" in top.percept):
            curr = top.id
            cnt = 0
            for m in range(len(env)):
                for n in range(len(env)):
                    if(top.id == cnt):
                        for temp in range(len(env)):
                            if(env[m][temp] == "W"):
                                env[m][temp] = ""
                                if(env[m-1][temp] == "s"):
                                    env[m-1][temp] = ""
                                if(env[m+1][temp] == "s"):
                                    env[m+1][temp] = ""
                                if(env[m][temp+1] == "s"):
                                    env[m][temp+1] = ""
                                build_grid_adjacency_list()

                            if(env[temp][n] == "W"):
                                env[temp][n] = ""
                                if(env[temp-1][n] == "s"):
                                    env[temp-1][n] = ""
                                if(env[temp+1][n] == "s"):
                                    env[temp+1][n] = ""
                                if(env[temp][n+1] == "s"):
                                    env[temp][n+1] = ""
                                build_grid_adjacency_list()   
                                
                        break
                         
        
        for i in graph[top]:
            i.parent = top
            sat, assignments = dpll(KB)
            #print(assignments)
            print(assignments)

            if(assignments == None):
                print(KB)
                exit()

            try:
                if((not assignments["W{}".format(i.id)]) and (not assignments["P{}".format(i.id)])):
                    stack.append(i)
                else:
                    pass
            except:
                stack.append(i)

    else:
        pass

    
    visited.add(top.id)

