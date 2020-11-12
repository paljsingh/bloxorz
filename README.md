BLOXORZ
---

```
$ python3 ./bloxorz.py -h
usage: bloxorz.py [-h] [-s {bfs,dfs,a-star}] [-t {ascii,unicode}] [-o ORDER] [-c {euclidean,manhattan}]

Bloxorz python implementation.

optional arguments:
  -h, --help            show this help message and exit
  -s {bfs,dfs,a-star}, --search {bfs,dfs,a-star}
                        Search method. (default=a-star)
  -t {ascii,unicode}, --style {ascii,unicode}
                        World map display style. (default=unicode)
  -o ORDER, --order ORDER
                        Order of search directions. (default=LRUD)
  -c {euclidean,manhattan}, --cost-method {euclidean,manhattan}
                        Distance metrics for heuristic cost for A*. (default=euclidean)

Search order can be any permutation of the characters 'L', 'R', 'D', 'U'.
Some of the search algorithms (e.g. DFS) may work better with knowing the general direction of the target block.
```

#### A* Search
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

---
#### Search order

Default search order is LRUD (left, right, up, down).  
Any permutation of the above 4 letters can be specified to run the search in a specific order. For example:

```
$ python3 ./bloxorz.py -o DURL -s dfs
```

---

#### Unicode v/s ASCII display
 
The app assumes that the terminal is capable of displaying unicode characters. In case you are using an old or non utf-8 compatible terminal, you can change the display style as:

```
$ python3 ./bloxorz.py -t ascii 
``` 

---
