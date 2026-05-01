n = int(input("Number of processes: "))
d = dict()

for i in range(n):
    k = "P"+str(i+1)
    a = int(input("Arrival"))
    b = int(input("Burst"))
    l = []
    l.append(a)
    l.append(b)
    d[k] = l

d = sorted(d.items(), key=lambda items: items[1][0])

ET = []
for i in range(len(d)):
    if i == 0:
        ET.append(d[i][1][1])
    else:
        ET.append(ET[i-1] + d[i][1][1])

TAT = []
for i in range(len(d)):
    TAT.append(ET[i] - d[i][1][0])

WT = []
for i in range(len(d)):
    WT.append(TAT[i] - d[i][1][1])

av = sum(WT)/len(WT)

for i in range(n):
    print(d[i][0]," ", d[i][1][0]," ", d[i][1][1]," ",ET[i], " ", TAT[i], " ", WT[i])

print("==", d[i][1][0],"==", end=" ")
for i in range(n):
    print(d[i][0], "==", ET[i],"==", end="")