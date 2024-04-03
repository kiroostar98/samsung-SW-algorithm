#################################입력
from collections import deque

N,M,P,C,D = map(int,input().split())
board = [[0 for c in range(N+1)] for r in range(N+1)]
rudolph = tuple(map(int,input().split())) # rudolph
board[rudolph[0]][rudolph[1]] = -1
for _ in range(P):
    idx,r,c = map(int,input().split())
    board[r][c] = idx
score = [0 for _ in range(P+1)]
dead = [0 for _ in range(P+1)]
stun = [0 for _ in range(P+1)]

# 산타 : 상우하좌
dy=[-1,0,1,0]
dx=[0,1,0,-1]

#산타위치 / 루돌프 위치를 맵으로 관리? 리스트로 관리?
# 리스트. O(N)
# 맵 X O(N^2) > 맵이 이동 관리에 더 편할것.
def print_board(board):
    print("board:")
    for r in range(1,N+1):
        print(board[r][1:])
    return

def out_of_range(y,x):
    if y<1 or y>N or x<1 or x>N:
        return 1
    return 0

def dist(y,x,ny,nx):
    return (y-ny)**2 + (x-nx)**2


def get_santa_coord(idx):
    for y in range(1,N+1):
        for x in range(1,N+1):
            if board[y][x]==idx:
                santa=(y,x)
                return santa
    #맵 안에 없으면 0,0
    return (0,0)

def find_rudolph():
    for y in range(1,N+1):
        for x in range(1,N+1):
            if board[y][x]==-1:
                rudolph=(y,x)
                return

def step1_move_rudolph():
    global rudolph
    # find_rudolph()
    min_dist = 9999
    min_idx = 0
    miny,minx=0,0
    (ry,rx) = rudolph
    for y in range(N,0,-1):
        for x in range(N,0,-1):
            if board[y][x]>0:
                idx = board[y][x]
                distance = dist(ry,rx,y,x) # 루돌프와의 거리.
                if distance <min_dist:
                    min_idx=idx
                    min_dist=distance
                    miny,minx=y,x
    
    # 좌표기준으로 이동방향 설정.
    if miny>ry: dry = 1
    elif miny==ry: dry=0
    else: dry=-1

    if minx>rx: drx=1
    elif minx==rx: drx=0
    else: drx = -1
    
    # print("miny,minx= ({},{})   dry,drx =({},{})".format(miny,minx,dry,drx))
    # 이동 수행.
    board[ry][rx] = 0
    ry,rx=ry+dry, rx+drx
    rudolph=(ry,rx)
    if board[ry][rx] == 0:
        board[ry][rx]=-1
    elif board[ry][rx]>0:
        collision(ry,rx,dry,drx,board[ry][rx],C)

    return

def step2_move_santa():
    for idx in range(1,P+1):
        if dead[idx]: 
            continue

        santa = get_santa_coord(idx)
        
        if santa==(0,0): # 사망.
            dead[idx]=1
            continue
        if stun[idx]: # 스턴상태
            continue
        (ry,rx)=rudolph
        (sy,sx)=santa
        # print("santa{} : {},{}".format(idx,sy,sx))
        min_dist = dist(sy,sx,ry,rx)
        miny,minx=sy,sx
        mindir = 0
        for dir in range(4):
            ny,nx=sy+dy[dir], sx+dx[dir]
            if out_of_range(ny,nx): # 범위 밖
                continue
            if board[ny][nx]>0: # 다른산타 있는 칸
                continue
            if dist(ny,nx,ry,rx)<min_dist:
                min_dist=dist(ny,nx,ry,rx)
                miny,minx=ny,nx
                mindir = dir
        # 이동.
        board[sy][sx]=0
        # print(" > ", (miny,minx))
        if board[miny][minx]<0: # 루돌프와 마주침 > 충돌. 역방향
            collision(ry,rx,-dy[mindir],-dx[mindir],idx,D)
        else: # 빈칸
            board[miny][minx]=idx
        
    return
    
def interaction(y,x, a, b,dry,drx):
    # a: 밀려온
    # b: 기존에 있던.
    # print("interaction! y {} x {} a {} b {} dry {} drx {}".format(y,x, a, b,dry,drx))
    board[y][x] = a
    q = deque()
    q.append((b,y+dry,x+drx))
    while q:
        (idx, ny,nx) = q.popleft()
        if out_of_range(ny,nx):
            return
        
        if board[ny][nx]>0:
            nextidx = board[ny][nx] # 기존에 있던 산타 번호
            board[ny][nx]=idx # 지금의 내가 자리차지
            nny,nnx = ny+dry,nx+drx # 다음 좌표
            q.append((nextidx,nny,nnx))
        else:
            board[ny][nx]=idx
            return

def collision(ry,rx,dry,drx,idx,power): 
    # print("\ncollision ! ry {} rx {} dry {} drx{} idx {} power {}".format(ry,rx,dry,drx,idx,power))
    # 루돌프 : rx,ry
    board[ry][rx] = -1
    #산타의 다음좌표.
    ny,nx = ry+dry*power, rx+drx*power
    stun[idx]=2
    score[idx]+=power # 밀려난 거리만큼 좌표 추가.
    if out_of_range(ny,nx):
        # print(ny,nx," > dead")
        dead[idx]=1
        return
    
    elif board[ny][nx]!=0:
        interaction(ny,nx,idx,board[ny][nx],dry,drx)
        return
    
    else: # 충돌자리에 루돌프, 밀려난 자리에 산타
        board[ny][nx] = idx
        return
    return


    # Interaction
    # stun


####debug
# print("")
# print(N,M,P,C,D)
# print("rudolph : ", rudolph)
# print_board(board)
# print("score : ", score)
# print("dead : ", dead)



def check_finish(board): # 모두 죽었으면 finish
    # for y in range(1,N+1):
    #     for x in range(1,N+1):
    #         if board[y][x]>0:
    #             return 0
    if sum(dead[1:])==len(dead[1:]):
        return 1
    return 0


# ####### Solve()
for turn in range(1,M+1):
    for idx in range(1,P+1):
        if stun[idx]>0:
            stun[idx]-=1 
            
    step1_move_rudolph()
    step2_move_santa()


    # 턴종료
    # for idx in range(1,P+1):
    #     if dead[idx]==0:
    #         score[idx]+=1
    for y in range(1,N+1):
        for x in range(1,N+1):
            if board[y][x]>0:
                idx = board[y][x]
                score[idx]+=1


    # print("")
    # print("turn ",turn)
    # print("rudolph : ", rudolph)
    # print_board(board)
    # print("score : ", score[1:])
    # print("dead : ", dead[1:])
    # print("stun : ",stun[1:])
    # print("")

    if check_finish(board):
        break

print(*score[1:])