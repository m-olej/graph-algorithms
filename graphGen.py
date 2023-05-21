import random
import math
import sys
import copy

sys.setrecursionlimit(10000000)


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
        outVert = [random.randint(1, n)]
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


def isEulerian(adjList):
    # --- Ustalanie stopni wierzchołków --- #
    uneven = []
    for k, v in adjList.items():
        if v % 2 != 0:
            uneven.append(k)
    # --- check for error --- #
    if len(uneven) == 2:
        start = uneven[random.randint(0, 1)]
        return start
    elif len(uneven) == 0:
        start = adjList[random.randint(1, len(adjList))]
        return start
    else:
        return False


# -- Hierholz euler cycle finder --- #

def hierholzEulerFinder(adjList):
    adjList1 = copy.deepcopy(adjList)
    ranks = {}
    check = 0
    for k, v in adjList1.items():
        ranks[k] = len(v)
        if len(v) % 2 != 0:
            check += 1

    currPath = []  # 1 is a starting point, which doesn't matter
    circuit = []

    curr = 1

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
        print("The Eulerian circuit: ", end="")
        for x in range(0, len(circuit)):
            if x != len(circuit)-1:
                print(circuit[x], end=" -> ")
            else:
                print(circuit[x])
    elif check == 2:
        print("The Eulerian Path: ", end="")
        for x in range(0, len(circuit)):
            if x != len(circuit)-1:
                print(circuit[x], end=" -> ")
            else:
                print(circuit[x])
    return

# - Robert's Fleury's algorithm for Euler's circuits - #

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

    if 0 not in xArray and check == 1:
        if xArray[0] in adjList[xArray[-1]]:
            print(xArray + [xArray[0]])
            return
        else:
            xArray[-1] = 0
            backTrackHam(adjList, False, root-1, xArray, kArray)
    elif root < len(adjList)-1 and check == 1:
        backTrackHam(adjList, False, root+1, xArray, kArray)
    elif root < len(adjList)-1 and check == 0:
        backTrackHam(adjList, False, root-1, xArray, kArray)


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

print("\n")
hierholzEulerFinder(adjList1)

sum = 0
for k, v in adjList1.items():
    sum += len(v)
    print(f"{k}: {v} -> {len(v)} == {sum}")
