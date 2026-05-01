n = int(input("number of processes : "))
d = dict()
for i in range(n):
    key = "P"+str(i+1)
    a = int(input("arrival "))
    b = int(input("burst "))
    l = []
    l.append(a)
    l.append(b)
    d[key] = l
keys = list(d.keys())
for k in keys:
    d[k].append(d[k][1])
ET = [0] * n
done = [False] * n
time = 0
finished = 0
while finished < n:
    shortest = -1
    for i in range(n):
        if d[keys[i]][0] <= time and not done[i]:
            if shortest == -1 or d[keys[i]][2] < d[keys[shortest]][2]:
                shortest = i
    if shortest == -1:
        time += 1
    else:
        d[keys[shortest]][2] -= 1
        time += 1
        if d[keys[shortest]][2] == 0:
            done[shortest] = True
            ET[shortest] = time
            finished += 1
TAT = []
for i in range(n):
    TAT.append(ET[i] - d[keys[i]][0])
WT = []
for i in range(n):
    WT.append(TAT[i] - d[keys[i]][1])

for i in range(n):
    print(" ",keys[i]," | ",d[keys[i]][0]," | ",d[keys[i]][1]," | ",ET[i]," | ",TAT[i]," | ",WT[i]," | ")