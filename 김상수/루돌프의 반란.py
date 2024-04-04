import sys
input = sys.stdin.readline
from collections import deque

n, m, p, c, d = map(int, input().split())
deer = list(map(int, input().split()))
santas = [[0,0] for _ in range(p)]
for _ in range(p):
    i, x, y = map(int, input().split())
    santas[i-1][0], santas[i-1][1] =x, y
failed = [0]*p
stunned = [0]*p
points = [0]*p
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def is_in_range(x,y):
    if 0< x <n+1 and 0< y <n+1:
        return 1
    else:
        return 0

def select_near_santa():
    i,x,y,r = 0,0,0,1000000
    for t in range(p):
        # 탈락 산타 제외
        if failed[t]:
            continue
        tr = (deer[0]-santas[t][0])**2 +(deer[1]-santas[t][1])**2
        if r > tr:
            i,x,y,r = t,santas[t][0],santas[t][1],tr
            # print("i,x,y,r", i,x,y,r)
            
        if r==tr:
            if x<santas[t][0]:
                i,x,y,r = t,santas[t][0],santas[t][1],tr
                # print("i,x,y,r", i,x,y,r)
            elif x==santas[t][0]:
                if y<santas[t][1]:
                    i,x,y,r = t,santas[t][0],santas[t][1],tr
                    # print("i,x,y,r", i,x,y,r)
    return i,x,y
            

def move_deer():
    global deer, santas, points, stunned, failed
    i, x, y = select_near_santa()
    # print("i,x,y", i,x,y)
    x_diff = x - deer[0]
    y_diff = y - deer[1]
    # 루돌프 이동
    if x_diff:
        deer[0] += x_diff//abs(x_diff)
    if y_diff:
        deer[1] += y_diff//abs(y_diff)
    # 충돌여부 확인
    if deer[0]==x and deer[1]==y:
        points[i] += c
        stunned[i] = 2
        if x_diff:
            santas[i][0] += (x_diff//abs(x_diff)) * c
        if y_diff:
            santas[i][1] += (y_diff//abs(y_diff)) * c
        if not is_in_range(santas[i][0], santas[i][1]):
            failed[i] =1
            return
        pushed_santa = deque()
        pushed_santa.append(i)
        # 상호 작용
        while pushed_santa:
            st = pushed_santa.popleft()
            for t in range(p):
                if st == t:
                    continue
                if santas[t][0] == santas[st][0] and santas[t][1] == santas[st][1]:
                    if x_diff:
                        santas[t][0] += x_diff//abs(x_diff)
                    if y_diff:
                        santas[t][1] += y_diff//abs(y_diff)
                    if not is_in_range(santas[t][0], santas[t][1]):
                        failed[t] = 1
                        return
                    pushed_santa.append(t)

def move_santa(i):
    global deer, santas, points, stunned, failed
    if stunned[i] or failed[i]:
        return
    x, y = santas[i][0], santas[i][1]
    dsx = x
    dsy = y
    r = (deer[0]-x)**2 +(deer[1]-y)**2
    for u in range(4):
        nx = x+dx[u]
        ny = y+dy[u]
        if [nx,ny] not in santas and r > (deer[0]-nx)**2 +(deer[1]-ny)**2:
            dsx = nx
            dsy = ny
            r = (deer[0]-nx)**2 +(deer[1]-ny)**2
        
    santas[i][0], santas[i][1] = dsx, dsy
    if deer[0]==dsx and deer[1]==dsy:
        points[i]+=d
        stunned[i] = 2
        santas[i][0] -=(dsx-x)*d
        santas[i][1] -=(dsy-y)*d
        pushed_santa = deque()
        if not is_in_range(santas[i][0], santas[i][1]):
            failed[i] = 1
            return
        pushed_santa.append(i)
        # 상호 작용
        while pushed_santa:
            st = pushed_santa.popleft()
            for t in range(p):
                if st == t:
                    continue
                if santas[t][0] == santas[st][0] and santas[t][1] == santas[st][1]:
                    santas[t][0] -=dsx-x
                    santas[t][1] -=dsy-y
                    if not is_in_range(santas[t][0], santas[t][1]):
                        failed[t] = 1
                        return
                    
                    pushed_santa.append(t)
    return

# main 함수
for _ in range(m):
    move_deer()
    # print(deer)
    for i in range(p):
        move_santa(i)
        # print("{i}번 산타 이동", santas[i])
        # print("santas", santas)
    for i in range(p):
        if stunned[i]:
            stunned[i] -= 1
        if not failed[i]:
            points[i]+= 1
    if not 0 in failed:
        break
    # print("failed", failed)
    
    
print(" ".join(map(str, points)))
