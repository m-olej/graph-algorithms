from graphGen import *
from scipy.sparse.csgraph import laplacian
import numpy as np


while True:

    print("1. Generowanie grafu \n2. Podanie grafu")
    genDec = int(input())
    if genDec == 1:
        print("Generowanie grafu - podaj \n n - ilość wierzchołków, \n p - nasycenie grafu, \n Czy ma być grafem hamiltońskim? ")
        n = int(input())
        p = float(input())
        h = input()

        if (h == "Y" or h == "y"):
            h = "h"

        done = False
        while not done:

            adjList1 = graphGen(n, p, h)

            sum = 0
            for k, v in adjList1.items():
                sum += len(v)
            if h == "h" and abs(sum - (n*(n-1))*p) <= 1:
                for k, v in adjList1.items():
                    print(f"{k}: {v} -> {len(v)}")
                print(sum)
                done = True
            elif h != "h" and abs(sum - (n*(n-1))*p)-2 <= 1:
                for k, v in adjList1.items():
                    print(f"{k}: {v} -> {len(v)}")
                print(sum)
                done = True
    elif genDec == 2:

        print("Podaj ilość wierzchołków i macierz sąsiedztwa grafu")
        vertAmount = int(input())
        adjMat = []
        for v in range(vertAmount):
            adjMatRow = list(map(int, input().split(" ")))
            adjMat.append(adjMatRow)
        for w in range(len(adjMat)):
            print(*adjMat[w])
        # --- ustalanie czy graf jest spójny --- #
        laplac = laplacian(np.array(unconnected))
        fiedlers, v = np.linalg.eig(laplac)
        fiedlers.sort()
        fiedlerNum = fiedlers[1]
        adjList1 = intoAdjList(adjMat)
        proceed = isEulerian(adjList1, fiedlerNum)

        if proceed == 0:
            continue

    print("Chcesz znaleźć cykl Eulera czy Hamiltona? \n 1. Eulera \n 2. Hamiltona")
    corr = False
    while not corr:
        dec = int(input())

        if dec == 1:
            print("Jaki chcesz użyć algorytm? \n 1. Hierholz's algorithm \n")
            decA = int(input())
            if decA == 1:
                corr = True
                hierholzEulerFinder(adjList1)
        elif dec == 2:
            print("Jaki chcesz użyć algorytm? \n 1. Abdul Bari's algorithm \n")
            decB = int(input())
            if decB == 1:
                corr = True
                backTrackHam(adjList1)

    print("Czy chcesz wygenerować kolejny graf ?")
    again = input()
    if again == "Y" or again == "y":
        continue
    else:
        break
