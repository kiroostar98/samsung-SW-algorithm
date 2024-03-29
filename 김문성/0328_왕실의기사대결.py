from collections import deque

# 이동방향: 상 우 하 좌
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]


# 입력값 받기
L,N,Q = map(int,input().split())
# L 지도크기 N 사람수 Q 쿼리수
# L<=40 N<=100, Q<=100
# k<=100
# 지도받기
board= [[0 for _ in range(L+1)] for _ in range(L+1)]
for i in range(1,L+1):
    board[i] = [0]+list(map(int,input().split()))


r= [0 for _ in range(N+1)]
c= [0 for _ in range(N+1)]
h= [0 for _ in range(N+1)]
w= [0 for _ in range(N+1)]
k= [0 for _ in range(N+1)]
nr=[0 for _ in range(N+1)]
nc=[0 for _ in range(N+1)]
# R,C : 위치. H : 세로길이. W : 가로길이. 초기체력 : K.

for i in range(1,N+1):
    r[i],c[i],h[i],w[i],k[i]=map(int,input().split())

damage=[0 for _ in range(N+1)]
moved =[0 for _ in range(N+1)]
initial_k=k[:]

def out_of_range(y,x):
    if y<1 or y>L or x<1 or x>L: 
        # print("out_of_range!")
        return 1
    return 0

def try_to_move(i,d):
    global damage,moved,nr,nc
    queue = deque([])
    damage=[0 for _ in range(N+1)]
    moved =[0 for _ in range(N+1)]
    nr = r[:]
    nc = c[:]

    
    queue.append(i)
    moved[i]+=1

    while queue:
        kn = queue.popleft()

        nr[kn]+=dy[d]
        nc[kn]+=dx[d]
        if out_of_range(nr[kn],nc[kn]) or out_of_range(nr[kn]+h[kn]-1,nc[kn]+w[kn]-1):
            return 0
        
        for y in range(nr[kn],nr[kn]+h[kn]):
            for x in range(nc[kn],nc[kn]+w[kn]):
                if board[y][x]==2: # 벽
                    # print("wall!")
                    return 0
                elif board[y][x]==1: # 함정
                    damage[kn]+=1

        for next in range(1,N+1): # 다른 충돌대상 확인.
            if moved[next]==1: # 이미 반영
                continue
            if k[next]<=0: #이미 사망
                continue
            if r[next]>nr[kn]+h[kn]-1 or c[next] > nc[kn]+w[kn]-1: # 오른쪽, 아래쪽
                continue
            if r[next]+h[next]-1 <nr[kn] or c[next]+w[next]-1 < nc[kn]: # 아예 왼쪽, 위쪽
                continue
            
            moved[next]=1
            queue.append(next) # 영향받는 애들은 큐에 넣어 확인.
    # print("damage: ", damage)
    #본인 이동은 노 대미지.
    damage[i]=0
    return 1

def Query(i,d):
    global k,r,c,nr,nc
    if k[i]<=0: # 이미사망
        return
    if try_to_move(i,d)!=0:
        r = nr[:]
        c = nc[:]
        for j in range(1,N+1):
            k[j]-=damage[j]


########### Solve
for q in range(Q):
    i,d=map(int,input().split())
    # print("round{}".format(q))
    Query(i,d)


ans = sum([initial_k[i]-k[i] for i in range(1,N+1) if k[i]>0])
# print(initial_k,k)
print(ans)