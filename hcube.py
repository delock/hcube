#/use/bin/python

import sys

data = []
recloc = []
senloc = []
d= 3
nodes = 2**d
senlocs = []
reclocs = []

print "All to All Reduce for %d dimensional hcube"%(d)

def a2a_src_dest(my_id, i):
    global d
    global recloc
    j = my_id & (2**i)
    k = (my_id ^ (2**i)) & (2**i)
    senloc[my_id] = recloc[my_id] + k
    recloc[my_id] = recloc[my_id] + j

    # prepare for reverse
    reclocs[my_id].append(senloc[my_id])
    senlocs[my_id].append(recloc[my_id])

def a2a_transfer(my_id, i, inc=True):
    target = my_id ^ (2**i)
    # twisted hypercube
    if (True):
        if ((my_id, target) == (2,6)): 
            target = 7
        if ((my_id, target) == (6,2)): 
            target = 3
        if ((my_id, target) == (3,7)): 
            target = 6
        if ((my_id, target) == (7,3)): 
            target = 2
    print "Iter %d, Node %d [%d] -> %d [%d] : %s"%(i, my_id, senloc[my_id], target, recloc[target], data[my_id][senloc[my_id]:senloc[my_id] + 2**i])
    for j in range(0, 2**i):
        if (inc):
            data[target][recloc[target]+j] += data[my_id][senloc[my_id]+j]
        else:
            data[target][recloc[target]+j] = data[my_id][senloc[my_id]+j]

for node in range(nodes):
    data.append([])
    for i in range (nodes):
        data[node].append(i)
    recloc.append(0)
    senloc.append(0)
    reclocs.append([])
    senlocs.append([])

print "Initial"
print data

print "Gather Reduce"
for i in range(d-1, -1, -1):
    for n in range(nodes):
        a2a_src_dest(n, i)
    for n in range(nodes):
        a2a_transfer(n, i)
    print data

print ">> Final Reduction <<"
print data
result = []
for i in range(nodes):
    result.append(data[i][i])
print result

print ">> Scatter <<"
for i in range(0, d):
    for n in range(nodes):
        senloc[n] = senlocs[n].pop()
        recloc[n] = reclocs[n].pop()
    for n in range(nodes):
        a2a_transfer(n, i, False)
    print data
