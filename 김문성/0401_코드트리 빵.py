
# #1분간 행동 수행.
# 1) 원하는 편의점 향해 1칸 이동. 최단거리로 움직이는 방법 여러가지면
# 상 좌 우 하
# 순으로.

# 2) 편의점에 도착하면 멈춤. 이때부터 다른 사람들은 해당 칸을 못지나감.
# - 이건 모두이동한 뒤에 적용됨.

# 3) t분, t<=m: t번은 가고싶은 편의점과 가장 가까운 베이스캠프로 이동.
#  가장 가까운 베이스캠프 이동.
# # 시간소모 X
# 좌상단부터.


# 유의사항 : 베이스캠프, 편의점 도착하면 이동 불가.

# 입력받기
# board : N*N
# m명, m분에 출발,

from collections import deque

N,M=map(int,input().split())
board=[[0 for _ in range(N+1)] for _ in range(N+1)]
for row in range(1,N+1):
    board[row] = [0]+list(map(int,input().split()))

conv=[(0,0)] # 1~M
for p in range(M):
    conv.append(tuple(map(int,input().split())))

# 사람 위치는 리스트로 관리.
people =[(0,0) for _ in range(M+1)]
next = [(0,0) for _ in range(M+1)]
# base : 1
# 사람있는 base : -1
# 사람있는 편의점 : -2

# print(N,M)
# for r in range(1,N+1):
#     print(board[r][1:])
# print(conv)
##################################################

dy=[-1,0,0,1] # 상 좌 우 하 순.
dx=[0,-1,1,0]

def print_map(board):
    print("board")
    for row in range(1,N+1):
        print(board[row][1:])
    return

def out_of_range(y,x):
   if y<1 or y>N or x<1 or x>N: return 1
   return 0

# 갈 수 있는 최단거리.
def check_distance(y,x,goaly,goalx):
    if (y,x)==(goaly,goalx): # 그자리.
        return 0

    queue = deque([])
    queue.append((y,x,0)) # 거리.
    visited=[]
    global time
    while queue:
        (r,c,dis) = queue.popleft()
        if (r,c) in visited:
            continue
        visited.append((r,c))
        if (r,c)==(goaly,goalx):
            return dis

        for i in range(4):
            nr,nc,ndis = r+dy[i],c+dx[i],dis+1
            if out_of_range(nr,nc): # 범위밖 : 
                continue
                
            if board[nr][nc]<0: # 사람이 차 있는 자리.
                continue 
            else:
                queue.append((nr,nc,ndis))
    
    return 400 # 이동 불가능한 경우.

def move_one_step(idx): # step1
    if people[idx]==(0,0): # 출발 안했으면 그대로
        return 0
    if people[idx]==conv[idx]: #편의점 도착했으면 그대로
        return 0
    (y,x) = people[idx] # 해당 사람 좌표
    goaly,goalx = conv[idx]
    min_dist = 400
    miny,minx = 0,0
    for dir in range(4): # 해당인원
        ny,nx = y+dy[dir],x+dx[dir]
        if out_of_range(ny,nx): # 범위 밖.
            continue
        if board[ny][nx]<0: # 못가는 칸
            continue
        print
        dist = check_distance(ny,nx,goaly,goalx)
        # print("")
        if dist<min_dist:
            min_dist=dist
            miny,minx=ny,nx
    
    next[idx] = (miny,minx)
    if next[idx]==(0,0):
        print("Error! {} No way to convi".format(idx))
    return 1



def find_closest_base(time):
    goaly,goalx = conv[time]
    min_distance = 400 # N<=15
    closest_base = (0,0)
    for y in range(1,N+1):
      for x in range(1,N+1):
         if board[y][x] == 1: # base.
            distance = check_distance(y,x,goaly,goalx)
            if min_distance>distance:
               min_distance=distance
               closest_base = (y,x)
    next[time] = closest_base
    # print("find_closest {} > {}".format(time,closest_base))
    # print("goal = ", conv[time])
    return
    


def fill_map(time):
    # print("next : ",next)
    # for i in range(1,min(M+1,time+1)):
    for i in range(1,M+1):
        people[i] = next[i]
        py,px = people[i]
        # print(py,px)
        if board[py][px]==1: # 베이스캠프라면 1.
            board[py][px]=-1
        if (py,px) == conv[i]: # 목표 편의점일 경우:
            board[py][px]= -2

    return

def finished(): # 모든 person이 편의점에 도착.
    for idx in range(1,M+1):
       if people[idx] != conv[idx]: # 한명이라도 도착안했으면
          return 0
    return 1
############################Solve()
time=1
while 1:
   # 편의점으로부터 가장 가까운 베이스캠프로 이동.
   # t번째 편의점 설정.
   # 가장 가까운 베이스캠프에 넣기.
   # 시간+1
   # 이동.
    
    next = people[:] # next 배열 초기화.
    for idx in range(1,M+1):
        ret = move_one_step(idx) # 맵에 나온 사람 모두 한걸음씩.
        

    fill_map(time)
    next = people[:] # next 배열 초기화.
    if time <=M:
        # t 번째 사람 베이슬 출발
        # if time==4:
        #     print_map(board)
        find_closest_base(time)
    # 이동봉쇄.(움직임 반영.)
    fill_map(time)
    
    ##Debugging
    # print("time : ",time)
    # print_map(board)
    # print("people : ",people)
    # print("next : ", next)
    # print("conv : ", conv)
    # print("")    

    if finished(): # 모두 도착했다면 break
        break

    time+=1
    
print(time)   
   