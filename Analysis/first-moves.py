r = open("move1.csv","r")
w = open("out.csv","w")

lines = r.readlines()

for row in lines:
    col = row.split(',')
    id = int(col[1])
    if (id>8):
        continue
    w.write(row)

r.close()

r = open("move2.csv","r")

lines = r.readlines()

for row in lines:
    col = row.split(',')
    id = int(col[1])
    if (id>8):
        continue
    w.write(row)

r.close()
w.close()
