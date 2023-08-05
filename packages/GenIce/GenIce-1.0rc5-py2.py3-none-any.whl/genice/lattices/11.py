# coding: utf-8
"""
Note: Due to the technical limitation in the GenIce algorithm, the minimum lattice size is larger than the crystallographic unit cell size.
"""
density = 0.92     #default density

bondlen = 3        #bond threshold	 
cell = """
7.84813412606925 7.37735062301457 9.06573834219084
"""

waters = """
1.328 1.802 3.38
5.267 4.524 1.109
6.58 5.442 3.365
5.267 4.542 5.629
2.623 0.877 5.644
2.667 5.488 5.625
5.241 1.756 1.12
5.241 1.774 5.64
1.354 4.588 7.888
1.354 4.57 3.369
2.667 5.47 1.105
2.623 0.858 1.124
6.537 0.831 3.384
6.537 0.849 7.903
6.581 5.461 7.884
1.328 1.82 7.899
"""

coord = "absolute"

fixed="""
4 7
4 5
11 6
11 10
12 0
12 2
13 15
13 14
8 14
8 15
9 2
9 0
1 10
1 6
3 5
3 7
5 8
5 9
10 8
10 9
2 1
2 3
14 1
14 3
6 12
6 13
7 12
7 13
0 4
0 11
15 4
15 11
"""

from genice.cell import cellvectors
cell = cellvectors(a=7.84813412606925,
                   b=7.37735062301457,
                   c=9.06573834219084)
