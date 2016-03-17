#!/usr/bin/python
#-----------------------------------------------------------------------
# File    : testacc.py
# Contents: examples how to use the fim module
# Author  : Christian Borgelt
# History : 2011.07.21 file created
#           2011.07.22 example with an external file added
#           2011.07.28 output of apriori documentation added
#           2011.08.03 apriacc call with minimum of p-values added
#           2013.02.11 made compatible with Python 3
#-----------------------------------------------------------------------
from sys import argv
from fim import accretion, apriacc, apriori

#-----------------------------------------------------------------------

def gdf_read (fname, sort = False):
    gdf = []                    # initialize the spike list
    with open(fname, 'rt') as inp:
        for line in inp:        # traverse the lines of the input file
            i,t = line.split()  # collect (neuron id, spike time) pairs
            gdf.append((int(float(i)), float(t)))
    if sort: gdf.sort(key = lambda k: k[1])
    return gdf                  # return (time-sorted) spike list

#-----------------------------------------------------------------------

def gdf_2tra (gdf, delta = 1, start = 0, end = ()):
    bag = []; ta = []           # initialize transaction and bag
    nxt = start +delta          # compute next time bin boundary
    for nid, time in gdf:       # traverse neuron id, spike time pairs
        if time < start: continue
        if time >= end:  break  # check for start and end time
        while time >= nxt:      # while spike is beyond current time bin
            bag.append(ta); ta = []
            nxt += delta        # add completed transaction to bag
        if nid > 0:             # if proper neuron identifier,
            ta.append(nid)      # add it to the transaction
        elif end == ():         # if end marker and no end time given
            end = time          # set end time from end marker
    if end == (): end = nxt +0.5*delta
    while nxt < end:            # while spike is beyond current time bin
        bag.append(ta); ta = [] # add completed transaction to bag
        nxt += delta            # compute next time bin boundary
    return bag                  # return the transaction bag

#-----------------------------------------------------------------------

def fim_reduce (res, agg = max):
    dic = dict([])
    for a,b in res:
        k = tuple(sorted(a))
        dic[k] = b if k not in dic \
            else [agg(x,y) for x,y in zip(dic[k],b)]
    return sorted([(k,tuple(dic[k])) for k in dic])

#-----------------------------------------------------------------------

if len(argv) < 2:
    print('usage: test.py testid')
    print('testid meaning')
    print('-3     print documentation of accretion')
    print('-2     print documentation of apriacc')
    print('-1     print documentation of apriori')
    print(' 0     execute accretion on mini database with integers')
    print(' 1     execute apriacc   on mini database with integers')
    print(' 2     execute accretion on mini database with strings')
    print(' 3     execute apriacc   on mini database with strings')
    print(' 4     execute accretion on external file \'test.gdf\'')
    print(' 5     execute apriacc   on external file \'test.gdf\'')
    print(' 6     execute accretion on external file \'test.gdf\'')
    print('       and reduce the output to unique sets')
    print(' 7     execute apriacc   on external file \'test.gdf\'')
    print('       but do weak   forward filtering with evaluation')
    print(' 8     execute apriacc   on external file \'test.gdf\'')
    print('       but do strong forward filtering with evaluation')
    exit()

tid = int(argv[1])

if   tid < -2:
    print(accretion.__doc__)
elif tid < -1:
    print(apriacc.__doc__)
elif tid <  0:
    print(apriori.__doc__)
elif tid <  4:
    if (tid & 2) != 0:
        tracts = [ [ 'a', 'b', 'c' ],
                   [ 'a', 'd', 'e' ],
                   [ 'b', 'c', 'd' ],
                   [ 'a', 'b', 'c', 'd' ],
                   [ 'b', 'c' ],
                   [ 'a', 'b', 'd' ],
                   [ 'd', 'e' ],
                   [ 'a', 'b', 'c', 'd' ],
                   [ 'c', 'd', 'e' ],
                   [ 'a', 'b', 'c' ] ]
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
    if (tid & 1) != 0:
        print  ('apriacc(tracts, siglvl=10):')
        for r in apriacc(tracts, siglvl=10): print r
    else:
        print  ('accretion(tracts, siglvl=10):')
        for r in accretion(tracts, siglvl=10): print r
else:
    if   tid > 7:
        print('apriacc(gdf_2tra(gdf_read(\'test.gdf\')),prune=+2):')
        for r in sorted(apriacc(gdf_2tra(gdf_read('test.gdf')),prune=+2)):
            print r
    elif tid > 6:
        print('apriacc(gdf_2tra(gdf_read(\'test.gdf\')),prune=-2):')
        for r in sorted(apriacc(gdf_2tra(gdf_read('test.gdf')),prune=-2)):
            print r
    elif tid > 5:
        print('fim_reduce(accretion(gdf_2tra(gdf_read(\'test.gdf\')))):')
        for r in fim_reduce(accretion(gdf_2tra(gdf_read('test.gdf')))):
            print r
    elif tid > 4:
        print('apriacc(gdf_2tra(gdf_read(\'test.gdf\'))):')
        for r in sorted(apriacc(gdf_2tra(gdf_read('test.gdf')))):
            print r
    else:
        print('accretion(gdf_2tra(gdf_read(\'test.gdf\'))):')
        for r in sorted(accretion(gdf_2tra(gdf_read('test.gdf')))):
            print r
