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

