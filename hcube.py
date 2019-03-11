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
    if (False):
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

import random
for node in range(nodes):
    data.append([])
    for i in range (nodes):
        #data[node].append(i)
        data[node].append(random.randint(1,10))
    recloc.append(0)
    senloc.append(0)
    reclocs.append([])
    senlocs.append([])

print "Initial"
print data

# calculate the answer ahead of time (we will check it later)
answer = []
for i in range (nodes):
    answer.append(0)
for node in range (nodes):
    for element in range (nodes):
        answer[element] += data[node][element]
print "Correct Answer"
print answer



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

print ">> Correct Answer <<"
print answer

print ">> Final Answer (per node) <<"
print data

print ">> Checking Answer <<"
for node in range (0, nodes):
    if (answer == data[node]):
        print "Node %d Pass"%node
    else:
        print "Node %d Fail"%node

