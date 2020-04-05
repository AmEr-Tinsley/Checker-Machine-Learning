
import sqlite3

"""conn = p.connect('Driver={SQL Server};'
                 'Server=LAPTOP-MP8CPB9L;'
                 'Database=checkers;'
                 'Trusted_Connection=yes;')"""

conn2 = sqlite3.connect("training.db")
c=conn2.cursor()

#cursor = conn.cursor()

board = []

for x in range(8):
    board.append([])

dx = [1,1,-1,-1]
dy = [1,-1,1,-1]

cnt = 0

def init():
    cnt = 32
    for x in range(8):
        board[x] = []
        for y in range(8):
            if ((x+y)%2 == 1):
                if cnt>=21:
                    board[x].append('b')
                elif cnt>=13:
                    board[x].append('e')
                else:
                    board[x].append('w')
                cnt-=1
            else:
                board[x].append('e')

def hash():
    ret = ""
    for x in range(8):
        for y in range(8):
            if ((x+y) % 2 == 1):
                ret+=board[x][y]
    return ret

def get(p):
    rem = 0
    if ((p-1)//4) % 2  == 1:
        rem=1
    p*=2
    p-=1
    x = 7 - (p//8)
    y = 7 + rem - (p%8)
    return x,y

def modify(x1,y1,x2,y2):
    if (x2 == 7 and board[x1][y1] == 'b'):
        board[x1][y1]='B'
    if (x2 == 0 and board[x1][y1] == 'w'):
        board[x1][y1]='W'

def update(x1,y1,x2,y2):
    modify(x1,y1,x2,y2)
    board[x1][y1],board[x2][y2] = board[x2][y2],board[x1][y1]

def push(state,move,res):
    c.execute("""SELECT * FROM visited WHERE state=? AND move=?""",(state,move))
    row=c.fetchone()
    if (row==None):
        c.execute("""INSERT INTO visited VALUES(?,?,0)""",(state,move))
        c.execute("""SELECT * FROM visited WHERE state=? AND move=?""",(state,move))
        row=c.fetchone()
    gain = int(row[2])+res
    c.execute("""UPDATE visited SET gain=? WHERE state=? AND move=?""",(gain,state,move))  

def eat(x,y):
    x1,y1 = get(x)
    x2,y2 = get(y)
    modify(x1,y1,x2,y2)
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = 'e'
    mn = 10000
    for d in range(4):
        xx = x1+dx[d]
        yy = y1+dy[d]
        dist = abs(xx-x2)+abs(yy-y2)
        if (dist<mn):
            i,j,mn=xx,yy,dist
    board[i][j]= 'e'

def move(s,gain):
    if ('x' in s):
        col = s.split('x')
        for i in range (1,len(col)):
            state = hash()
            #show(state)
            move  =  col[i-1] + 'x' + col[i]
            push(state,move,gain)
            eat(int(col[i-1]),int(col[i]))

    else:
        col = s.split('_')
        x1,y1 = get (int(col[0]))
        x2,y2 = get (int(col[1]))
        state = hash()
        #show(state)
        push(state,s,gain)
        update(x1,y1,x2,y2)

def get_gain(idp,idj):
    c = cursor.execute("SELECT resultat FROM checkers.dbo.joueurpartie WHERE idp=? AND idj=?",idp,idj)
    res = c.fetchone()
    return int(res[0])

def show(s):
    grid = []
    cnt=0
    for x in range(8):
        grid.append([])
        for y in range(8):
            if ((x+y)%2 == 1):
                if (s[cnt]=='e'):
                    grid[x].append('.')
                else:
                    grid[x].append(s[cnt])
                cnt+=1
            else:
                grid[x].append('.')
        print(grid[x])
    print()
    print()

show('bbbbbbbbbbbbeeeeeweewewwwwwwwwww')
"""
lines = cursor.execute("SELECT * FROM checkers.dbo.mouvement").fetchall()

idp = 0

for row in lines:
    
    game = int(row[2])
    if (game!=idp):
        #print("#######################################################")
        init()
        idp=game
        gain = get_gain(int(row[2]),int(row[3]))
    move(row[1],gain)
    gain*=-1


conn2.commit()
conn.close()
conn2.close()
"""
