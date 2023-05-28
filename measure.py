from graphGen import *
import time
import sys

sys.setrecursionlimit(100000000)

d = 50
testSizes = [int(d*x) for x in range(1, 11)]

timeArray07 = []
timeArray03 = []

for p in [0.7]:
    for n in testSizes:
        done = False
        while not done:
            sum = 0
            adjList1 = graphGen(n, p, "h")
            for k, v in adjList1.items():
                sum += len(v)
            if abs(sum - (n*(n-1))*p) <= 4:
                done = True
        print(n, p)
        start = time.time()
        backTrackHam(adjList1)
        end = time.time()
        if p == 0.7:
            timeArray07.append(end-start)
        elif p == 0.3:
            timeArray03.append(end-start)


print("0.7")
print(*timeArray07)
print("0.3")
print(*timeArray03)
print(testSizes)

# -- for more relaible backtracking measuring -- #

# n, p = 9, 0.5
# done = False
# while not done:
#     sum = 0
#     adjList1 = graphGen(n, p, "nh")
#     for k, v in adjList1.items():
#         sum += len(v)
#     if abs(sum - (n*(n-1))*p) <= 4:
#         done = True


# start = time.time()
# backTrackHam(adjList1)
# end = time.time()

# print(end-start)
