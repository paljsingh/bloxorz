from itertools import permutations
from os import system

args = ['python3', './bloxorz.py', '-v']

# BFS, DFS
for perm in permutations(['L', 'U', 'R', 'D']):
    for algorithm in ['bfs', 'dfs']:
        opts = ['-o', ''.join(perm), '-s', algorithm]
        system(' '.join(args + opts))

        print("\n\nalgorithm: {}, order: {}".format(algorithm, ''.join(perm)))
        input("press ENTER to continue - ")

# A*
for perm in permutations(['L', 'U', 'R', 'D']):
    for cost_heuristic in ['euclidean', 'manhattan']:
        opts = ['-o', ''.join(perm), '-s', 'a-star', '-c', cost_heuristic]
        system(' '.join(args + opts))

        print("\n\nalgorithm: A*, order: {}, heuristic: {}".format(''.join(perm), cost_heuristic))
        input("press ENTER to continue - ")
