import random
import math
import sys
import copy
from scipy.sparse.csgraph import laplacian
import numpy as np
from szynkowane import *

sys.setrecursionlimit(1000000)


def graphGen(n, p, h):
    edgeNum = math.ceil((n * (n - 1) // 2) * p)
    vetrices = [x for x in range(1, n+1)]
    adjList = {v: [] for v in vetrices}
    random.shuffle(vetrices)

    for x in range(len(vetrices)):
        if x != n-1:
            adjList[vetrices[x]].append(vetrices[x+1])
            adjList[vetrices[x+1]].append(vetrices[x])
        elif h == "h":
            adjList[vetrices[x]].append(vetrices[0])
            adjList[vetrices[0]].append(vetrices[x])
        elif h != "h":
            rm = adjList[vetrices[x]].pop()
            adjList[rm].remove(vetrices[x])
            vetrices.pop()
        edgeNum -= 1

    while edgeNum > 0:
        # print(edgeNum)
        if edgeNum > n-2:
            length = random.randint(3, n-2)
        elif edgeNum >= 3:
            length = random.randint(3, edgeNum)
        elif edgeNum == 1:
            length = 2
        else:
            edgeNum = 0
        # outVert = random.sample(vetrices, length)

        fail = False
        outVert = random.sample(vetrices, 1)
        while len(outVert) < length:
            if len(outVert) == length-1:
                vetricesEx = vetrices[:]
                for x in outVert:
                    vetricesEx.remove(x)
                nexter = [x for x in vetricesEx if x not in adjList[outVert[-1]]]
                exiter = []
                for y in nexter:
                    if outVert[0] not in adjList[y]:
                        exiter.append(y)
                if len(exiter) == 0:
                    fail = True
                    break
                else:
                    outVert.append(*random.sample(exiter, 1))
            else:
                vetricesEx = vetrices[:]
                for x in outVert:
                    vetricesEx.remove(x)
                nexter = [x for x in vetricesEx if x not in adjList[outVert[-1]]]

                if len(nexter) == 0:
                    fail = True
                    break
                else:
                    outVert.append(*random.sample(nexter, 1))

        if fail:
            continue

        for v in range(len(outVert)):
            if v != len(outVert)-1:
                adjList[outVert[v]].append(outVert[v+1])
                adjList[outVert[v+1]].append(outVert[v])
            else:
                adjList[outVert[v]].append(outVert[0])
                adjList[outVert[0]].append(outVert[v])
            edgeNum -= 1

    return adjList


def intoMatrix(adjList):
    adjMat = [[0 for j in range(len(adjList))] for i in range(len(adjList))]

    for x in range(1, len(adjList)+1):
        for y in adjList[x]:
            adjMat[x-1][y-1] = 1
            adjMat[y-1][x-1] = 1
    return adjMat


def intoAdjList(adjMat):
    adjList = {}
    for v in range(len(adjMat)):
        adjList[v+1] = []
        for w in range(len(adjMat[v])):
            if adjMat[v][w] == 1:
                adjList[v+1].append(w+1)
    return adjList


def isEulerian(adjList, connected):
    # --- Ustalanie stopni wierzchołków --- #
    uneven = 0
    loop = 0
    for k, v in adjList.items():
        if len(v) % 2 != 0:
            uneven += 1
        if k in v:
            loop += 1

    if uneven == 0 and connected:
        print("Ten graf ma cykl Eulera (graf eulerowski)")
        return 1
    elif uneven == 2 and connected:
        print("Ten graf ma tylko ścieżkę Eulera (graf półeulerowski)")
        return 1
    else:
        if loop != 0:
            print("Ten graf posiada pętlę własną !!!")
        print("Ten graf nie jest Eulerowski")
        return 0


def isValidGraph(adjMat):
    for v in range(len(adjMat)):
        for w in range(len(adjMat[v])):
            if adjMat[v][w] != adjMat[w][v]:
                return 0
    return 1
# -- Hierholz euler cycle finder --- #


def hierholzEulerFinder(adjList):
    adjList1 = copy.deepcopy(adjList)
    ranks = {}
    check = 0
    for k, v in adjList1.items():
        ranks[k] = len(v)
        if len(v) % 2 != 0:
            check += 1
            unEvenVert = k

    currPath = []  # 1 is a starting point, which doesn't matter
    circuit = []

    if check == 0:
        curr = 1
    elif check == 2:
        curr = unEvenVert

    currPath.append(curr)

    while len(currPath):

        if ranks[curr]:

            ranks[curr] -= 1
            last_curr = curr
            curr = adjList1[curr].pop()
            currPath.append(curr)
            adjList1[curr].remove(last_curr)
            ranks[curr] -= 1

        else:
            circuit.append(currPath.pop())

    # -- printing circuit -- #
    if check == 0:
        print("Cykl Eulera: ", end="")
        for x in range(0, len(circuit)):
            if x != len(circuit)-1:
                print(circuit[x], end=" -> ")
            else:
                print(circuit[x])
    elif check == 2:
        print("Scieżka Eulera: ", end="")
        for x in range(0, len(circuit)):
            if x != len(circuit)-1:
                print(circuit[x], end=" -> ")
            else:
                print(circuit[x])
    return


# --- backtracking Hamiltonian circuit finder --- #


def backTrackHam(adjList, first=True, root=0, xArray=[], kArray=[]):
    if first:
        # kArray is for keeping changes done in xArray.
        # It keeps track of which vertex was chosen last.
        kArray = [1 for x in range(len(adjList))]
        xArray = [0 for x in range(len(adjList))]
        xArray[root] = 1

    # -- #
    # root is the index of the xArray List which starts from 0,
    # but in AdjList indexes are the vertice numbers which are indexed
    # from 1. When referencing successors of a vertex use adjList[root+1]
    # -- #

    check = nextVertex(adjList, xArray, root, kArray)
    print(root)
    if 0 not in xArray and check == 1:
        if xArray[0] in adjList[xArray[-1]]:
            print(xArray + [xArray[0]])
            return
        else:
            xArray[-1] = 0
            backTrackHam(adjList, False, root-1, xArray, kArray)
    elif root < len(adjList)-1 and check == 1:
        backTrackHam(adjList, False, root+1, xArray, kArray)
    elif root > 0 and check == 0:
        backTrackHam(adjList, False, root-1, xArray, kArray)
    return "No cycle to Be Found"


def nextVertex(adjList, xArray, root, kArray):

    # 1. there shouldn't be duplicate vertices in xArray,
    # 2. there should exist an edge between xArray[k] and xArray[k+1]
    # 3. if xArray doesn't have a 0 check if xArray[last] connects with xArray[0]

    while True:
        nextRoot = kArray[root+1] % (len(adjList) + 1)
        if (nextRoot not in xArray) and (nextRoot in adjList[xArray[root]]):
            xArray[root+1] = nextRoot
            kArray[root+1] += 1
            break
        if nextRoot == 0:
            xArray[root+1] = nextRoot
            kArray[root+1] += 1

            # 0 -> backtrack
            return 0
        kArray[root+1] += 1
    # 1 -> do not backtrack
    return 1
    ...


# --- "h" dla grafu hamiltonowskiego cokolwiek innego dla niehamiltonowskiego ---#

# TESTING

adjList1 = graphGen(10, 0.5, "h")

sum = 0
for k, v in adjList1.items():
    sum += len(v)
    print(f"{k}: {v} -> {len(v)} == {sum}")

adjMat = intoMatrix(adjList1)

graph = open("graphStorage", "w")

for x in range(len(adjMat)):
    print(*adjMat[x])
    for i in adjMat[x]:
        graph.write(str(i) + " ")
    graph.write("\n")

# print("\n")
ch = hierholzEulerFinder(adjList1)
# print(ch)

# adjList1 = graphGen(10, 0.5, "h")

# sum = 0
# for k, v in adjList1.items():
#     sum += len(v)
#     print(f"{k}: {v} -> {len(v)} == {sum}")

# adjMat = intoMatrix(adjList1)
# print("\n")
# for x in range(len(adjMat)):
#     print(*adjMat[x])

# unconnected = [[0, 1, 1, 0, 0, 0, 0], [1, 0, 1, 1, 0, 0, 0,], [1, 1, 0, 0, 1, 0, 0], [
#     0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0]]

# laplac = laplacian(np.array(unconnected))
# fiedlers, v = np.linalg.eig(laplac)
# fiedlers.sort()
# print(laplac)
# print(fiedlers[1])
