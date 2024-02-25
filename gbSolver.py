from pulp import *

'''
minimise ∑ [ Cij(1 - Hij) + (1 - Cij)Hij + Xi + Yj] 
where Cij represents the state of the light at position ij (1 if on, 0 if off)
      Hij represents whether the state of the light at position ij has changed, Hij = |Xi - Yj|
      Xi = 1 if row i switch is turned on, 0 otherwise
      Yj = 1 if column j switch is turned on, 0 otherwise
      Hij = 1 if state of light has changed (ie either row i turned on or column j turned on), 0 otherwise (both turned on or both not turned on)

For light ij, if its state has changed (Hij = 1), then we record down the new state of light (1 - Cij)
              if its state did not change (Hij = 0), then we record down the original state of light (Cij)

Hij = |Xi - Yj| is not a linear equation, add a dummy boolean (take 0 or 1 only) variable Zij to make it linear

becomes...
Hij <= Xi - Yj + 2 Zij
Hij >= Xi - Yj - 2 Zij 
Xi - Yj + 1 <= 2 (1 - Zij)
Hij >= Yj - Xi

Case Zij = 0, Xi >= Yj
              Hij = Xi - Yj = |Xi - Yj|

Case Zij = 1, Xi < Yj (ie Xi = 0 and Yj = 1)
              Hij = 1 = Yj - Xi = |Xi - Yj|

We have 4 decision variables:
H being an n * n matrix (Hij)
X being an n vector (Xi)
Y being an n vector (Yj)
Z being an n * n matrix (Zij)
'''

def GB_Solver (lightGrid : list , columnSwitch : list , rowSwitch : list, n : int) -> int :

    prob = LpProblem("GB_Problem", LpMinimize)

    # Decision Variables
    H = LpVariable.dicts("H", [(i,j) for i in range(n) for j in range(n)], cat="Binary")
    X = LpVariable.dicts("X", [i     for i in range(n) ], cat="Binary")
    Y = LpVariable.dicts("Y", [j     for j in range(n)], cat="Binary")
    Z = LpVariable.dicts("Z", [(i,j) for i in range(n) for j in range(n)], cat="Binary")

    # Objective Function
    prob += (
    sum( [lightGrid[i][j] * (1 - H[(i,j)]) for i in range(n) for j in range(n)] )          # Cij(1 - Hij)
        + sum( [(1 - lightGrid[i][j]) * H[(i,j)] for i in range(n) for j in range(n)] )    # (1 - Cij)Hij
        + sum(X[i] for i in range(n))                                                       # minimize row switches
        + sum(Y[j] for j in range(n))                                                       # minimize column switches
    ), "Number_LIT_Bulbs"


    # Constraints
    for i in range(n):
        for j in range(n):
            prob += H[(i,j)] <= X[i] - Y[j] + 2*Z[(i,j)] ,   "Type_1_{}_{}".format(i,j)
            prob += H[(i,j)] >= X[i] - Y[j] - 2*Z[(i,j)] ,   "Type_2_{}_{}".format(i,j)
            prob += X[i] - Y[j] + 1 <= 2*(1 - Z[(i,j)]) ,    "Type_3_{}_{}".format(i,j)
            prob += H[(i,j)] >= Y[j] - X[i] ,                "Type_4_{}_{}".format(i,j)

    #print(prob)

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    # print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    for i in range(n):
        print(f"Row {i} = {'Turned on' if X[i].varValue == 1 else 'Still off'} ({rowSwitch[i]} -> {(rowSwitch[i] + int(X[i].varValue)) % 2 })")
    print()

    for j in range(n):
        print(f"Col {j} = {'Turned on' if Y[j].varValue == 1 else 'Still off'} ({columnSwitch[j]} -> {(columnSwitch[j] + int(Y[j].varValue)) % 2})")
    print()

    print ("Original Marix:")
    for i in range(-2 , n):

        for j in range(-1 , n) :

            if (i == -2 and j == -1) :
                print (" " , end = "|")

            elif (i == -2) :
                print (columnSwitch[j] , end = " ")

            elif (i == -1) :
                print ("--" , end = "")

            elif (j == -1) :
                print (rowSwitch[i] , end = "|")

            else :
                print (lightGrid[i][j] , end = " ")

        print()
    print()

    print ("New Marix:")
    for i in range(-2 , n):

        for j in range(-1 , n) :

            if (i == -2 and j == -1) :
                print (" " , end = "|")

            elif (i == -2) :
                print ((columnSwitch[j] + int(Y[j].varValue)) % 2 , end = " ")

            elif (i == -1) :
                print ("--" , end = "")

            elif (j == -1) :
                print ((rowSwitch[i] + int(X[i].varValue)) % 2 , end = "|")

            else :
                print (int(lightGrid[i][j] * (1 - H[(i,j)].varValue) + (1 - lightGrid[i][j]) * H[(i,j)].varValue) , end = " ")

        print()
    print()

    optimizedMatrix = []

    for i in range (0 , n + 1) :
        optimizedMatrix.append([])
        for j in range (0 , n + 1) :

            if i == 0 and j == 0 :
                optimizedMatrix[0].append (-1)

            elif i == 0:
                optimizedMatrix[0].append((columnSwitch[j-1] + int(Y[j-1].varValue)) % 2)

            elif j == 0 :
                optimizedMatrix[i].append((rowSwitch[i-1] + int(X[i-1].varValue)) % 2)

            else :
                optimizedMatrix[i].append(int(lightGrid[i-1][j-1] * (1 - H[(i-1, j-1)].varValue) + (1 - lightGrid[i-1][j-1]) * H[(i-1, j-1)].varValue))

    return optimizedMatrix, value(prob.objective)
