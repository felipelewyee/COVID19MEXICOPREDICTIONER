f = open("dias.csv",'r')

p = []

for line in f:
    p.append(line.split(',')[0])

print(p)
