BLOXORZ Game Search
---

Python implementation of BFS, DFS, UCS, Greedy best first and A\* search for first level of Bloxorz game.


```
$ python3 ./bloxorz.py -h
usage: bloxorz.py [-h] [-c {euclidean,manhattan}] [-o ORDER]
                  [-s {bfs,dfs,ucs,greedy_bfs,a-star}]
                  [-t {ascii,unicode}] [-v]

Bloxorz python implementation.

optional arguments:
  -h, --help            show this help message and exit
  -c {euclidean,manhattan}, --cost-method {euclidean,manhattan}
                        Distance metrics for heuristic cost for A*.
                        (default=euclidean)
  -o ORDER, --order ORDER
                        Order of search directions. (default=LRUD)
  -s {bfs,dfs,ucs,greedy_bfs,a-star}, --search {bfs,dfs,ucs,greedy_bfs,a-star}
                        Search method. (default=a-star)
  -t {ascii,unicode}, --style {ascii,unicode}
                        World map display style. (default=unicode)
  -v, --verbose         verbose output.

Search order can be any permutation of the characters 'L', 'R', 'U', 'D'.
Some of the search algorithms (e.g. DFS) may work better with knowing the general direction of the target block.
```

#### A\* Search
```
$ python3 ./bloxorz.py

or

$ python3 ./bloxorz.py -s a-star
```

#### DFS / BFS search
```
$ python3 ./bloxorz.py -s bfs

$ python3 ./bloxorz.py -s dfs
```

#### UCS search
```
$ python3 ./bloxorz.py -s ucs
```

#### greedy best first search 
```
$ python3 ./bloxorz.py -s greedy_bfs
```


---
#### Search order

Default search order is LRUD (left, right, up, down).  
Any permutation of the above 4 letters can be specified to run the search in a specific order. For example:

```
$ python3 ./bloxorz.py -o DURL -s dfs
```

---
#### Heuristic Cost Function

The default heuristic cost function for A\* search is based on Euclidean distance. It can be changed to Manhattan distance by specifying the same in command line arguments.
```
$ python3 ./bloxorz.py -c manhattan -s a-star
```

---
#### Verbose output

Extra information about the search decisions is printed if verbose option specified.
```
$ python3 ./bloxorz.py -v
```

---
#### Unicode v/s ASCII display
 
The app assumes that the terminal is capable of displaying unicode characters. In case you are using an old or non utf-8 compatible terminal, you can change the display style as:

```
$ python3 ./bloxorz.py -t ascii 
``` 

---
