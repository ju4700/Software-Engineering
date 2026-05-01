x=2
y=3
print(x)
print(y)

string = "i am jalal"
print(f'string + {x}')
print(f'string - {x}')
print(f'string * {x}')

if x == y:
    print('x is equal to y')
else:
    print('x is not equal to y')

i=1
for i in range(100):
    print(i)

lists = ['apple', 'jackfruit', 'banana']
for i in lists:
    print(i)

diction = {
    "name" : ["name", "a;skjd", "asjd"],
    "age" : 21
}

for k, v, in diction.items():
    if k == "name":
        print("\n")
    else:
        print(k, v)
        for w in v:
            print(w)