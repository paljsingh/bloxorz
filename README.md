BLOXORZ
---

```
$ python3 ./bloxorz.py -h
usage: bloxorz.py [-h] [--search {bfs,dfs,astar}] [--style {ascii,utf8}]

Bloxorz python implementation.

optional arguments:
  -h, --help            show this help message and exit
  --search {bfs,dfs,astar}, -s {bfs,dfs,astar}
                        search method.
  --style {ascii,utf8}, -t {ascii,utf8}
                        world map display style.
```

#### A* Search
```
$ python3 ./bloxorz.py

or

$ python3 ./bloxorz.py -s astar
```

#### DFS / BFS search
```
$ python3 ./bloxorz.py -s bfs

$ python3 ./bloxorz.py -s dfs
```

The app assumes that the terminal is capable of displaying unicode characters. In case you are using an old or non utf-8 compatible terminal, you can change the display style as:

```
$ python3 ./bloxorz.py -t ascii 
``` 
  