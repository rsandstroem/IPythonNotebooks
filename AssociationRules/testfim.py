#!/usr/bin/python
#-----------------------------------------------------------------------
# File    : testfim.py
# Contents: examples how to use the pure fim functions of the fim module
# Author  : Christian Borgelt
# History : 2012.04.17 file created
#           2013.02.11 made compatible with Python 3
#-----------------------------------------------------------------------
from sys import argv
from fim import apriori, eclat, fpgrowth, fim

#-----------------------------------------------------------------------

tid = int(argv[1])
if   tid < -2:
    print(fpgrowth.__doc__)
elif tid < -1:
    print(eclat.__doc__)
elif tid <  0:
    print(apriori.__doc__)
else:
    tracts = [ [ 1, 2, 3 ],
               [ 1, 4, 5 ],
               [ 2, 3, 4 ],
               [ 1, 2, 3, 4 ],
               [ 2, 3 ],
               [ 1, 2, 4 ],
               [ 4, 5 ],
               [ 1, 2, 3, 4 ],
               [ 3, 4, 5 ],
               [ 1, 2, 3 ] ]
    print('transactions:')
    for t in tracts: print(t)
    if   tid < 1:
        print  ('apriori(tracts, supp=-3, zmin=2):')
        for r in apriori(tracts, supp=-3, zmin=2): print r
    elif tid < 2:
        print  ('eclat(tracts, supp=-3, zmin=2):')
        for r in eclat(tracts, supp=-3, zmin=2): print r
    elif tid < 3:
        print  ('fpgrowth(tracts, supp=-3, zmin=2):')
        for r in fpgrowth(tracts, supp=-3, zmin=2): print r
    else:
        print  ('fim(tracts, supp=-3, zmin=2, report=\'#\'):')
        for r in fim(tracts, supp=-3, zmin=2, report='#'): print r
