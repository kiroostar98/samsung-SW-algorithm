n, m, k = tuple(map(int, input().split()))
# 모든 벽들의 상태를 기록해줍니다.
board = [[0 for _ in range(n+1)] for _ in range(n+1)]
for i in range(1, n + 1):
    board[i] = [0] + list(map(int, input().split()))
next_board = [[0 for _ in range(n+1)] for _ in range(n+1)]

# 참가자의 위치 정보를 기록해줍니다.
traveler = [(-1, -1)] + [tuple(map(int, input().split())) for _ in range(m)]
exits = tuple(map(int, input().split()))
ans = 0
# 정사각형 spec
sx, sy, square_size = 0, 0, 0

def out_of_range(y,x):
    if y>n or y<1 or x>n or x<1: return 1
    return 0
def distance(y1,x1,y2,x2):
    return abs(y1-y2)+abs(x1-x2)
def move():
    global ans
    dy=[1,-1,0,0]
    dx=[0,0,1,-1]
    for p in range(1,m+1): #이미 탈출
        if traveler[p]==exits:
            continue
        (py,px) = traveler[p]
        for idx in range(4):
            ny,nx = py+dy[idx],px+dx[idx]
            if out_of_range(ny,nx) or board[ny][nx]:continue # 범위밖 or 벽
            if distance(ny,nx,exits[0],exits[1]) >= distance(py,px,exits[0],exits[1]):continue # 더 멀경우
            traveler[p]=ny,nx
            ans+=1
            break
    return


def find_square():
    global exits, sy, sx, square_size
    ey, ex = exits
    for sz in range(2, n + 1):
        for y1 in range(1, n +1):
            for x1 in range(1, n +1):
                y2, x2 = y1 + sz - 1, x1 + sz - 1
                if out_of_range(y2,x2):
                    continue
                if not (y1 <= ey <= y2 and x1 <= ex <= x2):
                    continue
                for t in range(1, m + 1): # 사람 있으면
                    ty, tx = traveler[t]
                    if (y1 <= ty <= y2 and x1 <= tx <= x2) and not (ty == ey and tx == ex):
                        sy,sx,square_size=y1,x1,sz
                        return

# 정사각형 회전
def rotate_square():
    global sy,sx,square_size
    for c in range(sy,sy+square_size): # 회전 
        for d in range(sx,sx+square_size):
            next_board[c][d]=board[sy+square_size-1 -(d-sx)][sx + (c-sy)]
            if next_board[c][d]>0:
                next_board[c][d]-=1
    for c in range(sy,sy+square_size): # 대입
        for d in range(sx,sx+square_size):
            board[c][d]=next_board[c][d]


#내부 점 회전
def rotate_point():
    global exits,sy,sx
    for idx in range(1,m+1):
        (ty,tx) = traveler[idx]
        if  sy<=ty<sy+square_size and sx<=tx<sx+square_size: # 범위내 사람 : 이동
            ty,tx  = sy+(tx-sx), sx + (sy+square_size-1 - ty)
            traveler[idx]=(ty,tx)

    (ey,ex) = exits
    newey,newex = sy+(ex-sx), sx + (sy+square_size-1 - ey)
    exits = (newey,newex)
    return 

def empty():
    for idx in range(1,m+1):
        if traveler[idx]!=exits: return 0
    return 1
    

for _ in range(k):
    move()
    if empty(): break
    find_square()
    rotate_square()
    rotate_point()

print(ans)

ey, ex = exits
print(ey, ex)