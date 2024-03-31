#싸움땅
# NbyN map
# 무기 없는 빈 격자.
# 각 플레이어는 각기 다른 초기 능력치를 가짐.

# 라운드 :



# 해당 과정을 1~N플레이어까지 순차 진행.

# 2 ≤ n ≤ 20
# 1 ≤ m ≤ min(n 
# 2
#  ,30)
# 1 ≤ k ≤ 500
# 1 ≤ 총의 공격력 ≤ 100,000
# 1 ≤ s ≤ 100
# 1 ≤ x, y ≤ n


#n,m,k : 격자크기 / 플레이어 수 / 라운드 수.
N,M,K = map(int,input().split())
# 지도 입력받기
board=[[0 for _ in range(N+1)] for _ in range(N+1)]
for row in range(1,N+1):
    board[row] = [0] + list(map(int,input().split()))
# 플레이어 입력받기

gunmap = [[[] for c in range(N+1)] for r in range(N+1)] # 3차원 배열.
for row in range(N+1):
    for col in range(N+1):
        gunmap[row][col].append(board[row][col]) # 빈 총 = 0으로 status 유지.
# print("gunmap")
# print(gunmap)
# print(gunmap[3][3])
# (gunmap[3][3]).append(1)
# print(gunmap)

x = [0 for _ in range(M+1)]
y = [0 for _ in range(M+1)]
d = [0 for _ in range(M+1)]
s = [0 for _ in range(M+1)]
nx = [0 for _ in range(M+1)]
ny = [0 for _ in range(M+1)]

for idx in range(1,M+1):
    y[idx],x[idx],d[idx],s[idx] = map(int,input().split())


# 추가 정의사항 : 총 보유, 현재 포인트.
guns   = [0 for _ in range(M+1)]
points = [0 for _ in range(M+1)]

## 입력확인
# print(board)
# print(x)
# print(y)
# print(d)
# print(s)

def out_of_range(yy,xx):
    if yy<1 or yy>N or xx<1 or xx>N: 
        return 1
    return 0

def reverse(dir):
    if dir==0: 
        dir = 2
    elif dir==1: 
        dir =3
    elif dir==2: 
        dir = 0
    else: 
        dir=1 # dir 3>1
    return dir

#상/우/하/좌 순
dy = [-1,0,1,0]
dx = [0,1,0,-1]

# 1-1 : 향하는 방향으로 한 칸씩 이동. 범위밖 > 방향 반전.
def move(idx):
    #좌표 받아오기
    # global y,x,d 

    direction = d[idx]
    ny,nx =y[idx]+dy[direction],x[idx]+dx[direction]
    
    if out_of_range(ny,nx):
        d[idx] = reverse(d[idx])
        direction = d[idx]
        ny,nx =y[idx]+dy[direction],x[idx]+dx[direction]
    
    # print("player # {} : {},{} > {},{}".format(idx, y[idx],x[idx],ny,nx))
    y[idx],x[idx]= ny,nx

    
def encounter(idx):
    for i in range(1,M+1):
        if i==idx: 
            continue # 본인
        elif y[idx]==y[i] and x[idx]==x[i]:
            return i
    return 0


# 2-1 : 플레이어 없으면 총 있는지 확인.
# - 총 있으면 총 획득
# - 총 이미 갖고 있으면 더 쎈 총 획득하고 나머지 총은 격자에 둠.

# 2-2-1 : 플레이어 있으면 배틀.
#     - 비교 스탯 = 초기능력치 + 총의 공격력 합 
#     - 큰 애가 생존.
#     - 이긴 플레이어가 스탯 차이만큼 포인트 획득.

# 2-2-2 : 진 플레이어는 
#     - 총을 내려놓고
#     - 원래 가진 방향으로 한 칸 이동.
#     - 해당 칸에 다른 플에이어 있거나, 격자 밖이면 우회전하여 빈칸 보이는 순간 이동.
#     - 해당 칸에 총 있으면 가장 공격력 높은 총을 획득.
# 2-2-3 : 이긴 플레이어는 슬이한 칸에 떨어져 있던 총과 원래 총 중 
#     - 센 총 줍고 나머지 내려 놓음.

def pickgun(idx):
    ## 구version = 2차원 배열
    # if board[y[idx]][x[idx]]==0: # 해당 자리에 총 없음
    #     return
    
    # if guns[idx]==0: # no gun.
    #     guns[idx],board[y[idx]][x[idx]]=board[y[idx]][x[idx]],guns[idx] # 줍줍
    
    # else:
    #     if guns[idx] < board[y[idx]][x[idx]]: # 본인 총보다 좋을때만 줍고 버리기.
    #         guns[idx],board[y[idx]][x[idx]]=board[y[idx]][x[idx]],guns[idx]
    strongest_gun = max(gunmap[ y[idx] ][ x[idx] ])
    if guns[idx] < strongest_gun:
        # 총 떨구기
        (gunmap[ y[idx] ][ x[idx] ]).append(guns[idx]) 
        # 총 줍기
        guns[idx] = strongest_gun
        (gunmap[ y[idx] ][ x[idx] ]).remove(strongest_gun)

    return 

def step2_battle(p1,p2):
    p1stat = guns[p1]+s[p1]
    p2stat = guns[p2]+s[p2]
    # print("{} stat : gun {} + {}".format(p1,guns[p1],s[p1]))
    # print("{} stat : gun {} + {}".format(p2,guns[p2],s[p2]))
    
    # winner / loser 순 리턴.
    if p1stat>p2stat: # p1 win
        # print("{} win, {} lose".format(p1,p2))
        points[p1] += (p1stat-p2stat) # 점수반영
        return (p1,p2)
    elif p1stat<p2stat: # p2 win
        # print("{} win, {} lose".format(p2,p1))
        points[p2] += (p2stat-p1stat)
        return (p2,p1)
    
    else: #draw > 순수 스탯 s[p]로 비교.
        if s[p1]>s[p2]:
            # print("{} win, {} lose".format(p1,p2))
            return (p1,p2)
        else:
            # print("{} win, {} lose".format(p2,p1))
            return (p2,p1)
    
def check_human(idx, ny,nx):
    for i in range(1,M+1):
        if idx==i: 
            continue
        if x[i]==nx and y[i]==ny: #본인 아니며, 좌표가 (ny,nx)와 같음 > 다음지점에 사람 있음.
            return 1
    return 0

def turn_right(idx):
    d[idx] = (d[idx]+1)%4 # 우회전.
    return

def step2_result(p1,p2):
    # 패자액션
    # 총내려놓기
    gunmap[ y[idx] ][ x[idx] ].append(guns[p2])
    guns[p2]=0

    for _ in range(4):
        direction = d[p2]
        ny,nx =y[p2]+dy[direction],x[p2]+dx[direction]
        if out_of_range(ny,nx) or check_human(p2,ny,nx):
            turn_right(p2)
            # print("{} turn right".format(p2))
        else:
            move(p2)
            pickgun(p2)
            break

    # 승자액션 : 총교체.
    pickgun(p1)
    
    return




# ############ Solve
    
for round in range(1,K+1):
    # print("round{} start".format(round))
    for idx in range(1,M+1):
        move(idx)
        #step2
        if encounter(idx)==0:# 사람 없으면 총줍기
            pickgun(idx) # 정상 동작 확인
        
        else: # 사람있으면 배틀.
            enemy=encounter(idx)
            # print("encounter : {},{}".format(idx,enemy))
            winner,loser = step2_battle(idx,enemy)

            step2_result(winner,loser)


#     print("round{} done".format(round))
#     print("y : ",y[1:])
#     print("x : ",x[1:])
#     print("d : ",d[1:])
#     print("guns : ",guns[1:])
#     print("points : ",points[1:])
#     print("")


## 정답출력
print(*points[1:])

