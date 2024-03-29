import sys
from collections import deque
input = sys.stdin.readline

l, n, q = map(int, input().split())
chess = [[0] * (l+1) for _ in range(l+1)]
r = [0] * (n+1)
c = [0] * (n+1)
h = [0] * (n+1)
w = [0] * (n+1)
k = [0] * (n+1)
nr = [0] * (n+1)
nc = [0] * (n+1)
moved = [0] * (n+1)
damage = [0] * (n+1)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
for i in range(l):
    chess_list = list(map(int, input().split()))
    for j in range(l):
        chess[i+1][j+1] = chess_list[j]

for i in range(n):
    r[i+1], c[i+1], h[i+1], w[i+1], k[i+1] = map(int, input().split())

orders = []
for i in range(q):
    a, b = map(int, input().split())
    orders.append((a,b))

initial_k = k[:]

def is_not_range(x,y):
    if 0<x<=l and 0<y<=l:
        return 0
    else:
        return 1

        
def try_to_move(i,d):
    global moved, damage,r,nr,c,nc
    moved = [0] * (n+1)
    damage = [0] * (n+1)
    nr = r[:]
    nc = c[:]
    moved[i] = 1
    pushed_knights = deque()
    pushed_knights.append(i)
    while pushed_knights:
        pk = pushed_knights.popleft()
        nr[pk] += dx[d]
        nc[pk] += dy[d]
        for x in range(nr[pk], nr[pk]+h[pk]):
            for y in range(nc[pk], nc[pk]+w[pk]):
                if is_not_range(x,y):
                    return 0
                if chess[x][y] == 2:
                    return 0
                if chess[x][y] == 1:
                    damage[pk] += 1
        for next in range(1, n+1):
            if moved[next]:
                continue
            if k[next] <= 0:
                continue
            if r[next] > nr[pk]+h[pk]-1 or r[next]+h[next]-1< nr[pk] or c[next] > nc[pk]+w[pk]-1 or c[next]+w[next]-1< nc[pk]:

                continue
            pushed_knights.append(next)
            moved[next] = 1
    return 1

def do_order(i,d):
    global r,c,nr,nc,k
    if k[i]<=0: # 이미사망
        return
    if try_to_move(i,d) != 0:
        r = nr[:]
        c = nc[:]
        for dm in range(1, n+1):
            if dm != i:
                k[dm] -= damage[dm]



for order in orders:
    i, d = order
    do_order(i,d)
answer = 0
for r in range(1, n+1):
    if k[r]>0:
        answer += initial_k[r] - k[r]
        
print(answer)
#hp 계산


