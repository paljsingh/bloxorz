# bloxorz

How to run:

 > $ python3 ./bloxorz.py
 
With no options specified, the application runs A* search alogorithm for round 1 map of bloxorz.


You can change the algorithm as:

 > $ python3 ./bloxorz.py -s bfs

or

 > $ python3 ./bloxorz.py -s dfs
 
 By default, the app assumes the terminal is capable of displaying utf-8 characters. If you see garbled characters, you may change the display style via:
 
  > python3 ./bloxorz.py -t ascii 
  
  The above will use lower ascii character set.
  