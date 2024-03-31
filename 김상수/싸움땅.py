import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
ground = [[[] for l in range(n+1)] for _ in range(n+1)]
for i in range(n):
    ground_line = list(map(int, input().split()))
    for j in range(n):
        gun = ground_line[j]
        ground[i+1][j+1].append(gun)
gun = [0] * m
x = [0] * m
y = [0] * m
d = [0] * m
s = [0] * m
for i in range(m):
    x[i],y[i],d[i],s[i] = map(int, input().split())

# print("n,m,k:", n,m,k)
# print("ground:", ground)
# print("x:", x)
# print("y:", y)
# print("d:", d)
# print("s:", s)

points = [0] * m
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def is_in_range(x,y):
    if 0<x<n+1 and 0<y<n+1:
        return 1
    else:
        return 0

def fight(a,b):
    a_attack = s[a]+gun[a]
    b_attack = s[b]+gun[b]
    if a_attack>b_attack:
        return a,b,a_attack-b_attack
    elif a_attack<b_attack:
        return b,a,b_attack-a_attack
    else:
        if s[a] >= s[b]:
            return a,b,0
        else:
            return b,a,0



def move_player(i):
    nx = x[i]+dx[d[i]]
    ny = y[i]+dy[d[i]]
    if not is_in_range(nx, ny):
        nx = x[i]-dx[d[i]]
        ny = y[i]-dy[d[i]]
        d[i] = (d[i]+2)%4
    x[i] = nx
    y[i] = ny
    fight_player = 0
    for p in range(m):
        if p==i:
            continue
        if nx==x[p] and ny==y[p]:
            fight_player =1
            winner, loser, point = fight(i,p)
            # print("winner, loser", winner, loser)
            points[winner] += point
            # print("winner point", winner, point)
            # 패자 이동
            for u in range(4):
                if u:
                    d[loser] = (d[loser]+1)%4
                lx = nx+dx[d[loser]]
                ly = ny+dy[d[loser]]
                find_player = 0
                if is_in_range(lx, ly):
                    for q in range(m):
                        if loser == q:
                            continue
                        if lx==x[q] and ly==y[q]:
                            find_player =1
                            break
                    if not find_player:
                        if gun[loser]:
                            ground[nx][ny].append(gun[loser])
                            gun[loser] = 0
                        if ground[lx][ly]:
                            get_gun = max(ground[lx][ly])
                            gun[loser] = get_gun
                            ground[lx][ly].remove(get_gun)
                        x[loser] = lx
                        y[loser] = ly
                        break
            # 승자
            if gun[winner]:
                winner_gun = gun[winner]
                if ground[nx][ny]:
                    if max(ground[nx][ny]) > winner_gun:
                        ground[nx][ny].append(winner_gun)
                        winner_gun = max(ground[nx][ny])
                        ground[nx][ny].remove(winner_gun)
                        gun[winner] = winner_gun
            else:
                if ground[nx][ny]:
                    gun[winner] = max(ground[nx][ny])
                    ground[nx][ny].remove(gun[winner])
            # print("ground", ground)
    # 아무와도 싸우지 않고 빈칸에 도착
    if not fight_player:
        if gun[i]:
                player_gun = gun[i]
                if ground[nx][ny]:
                    if max(ground[nx][ny]) > player_gun:
                        ground[nx][ny].append(player_gun)
                        player_gun = max(ground[nx][ny])
                        ground[nx][ny].remove(player_gun)
                        gun[i] = player_gun
        else:
                if ground[nx][ny]:
                    gun[i] = max(ground[nx][ny])
                    ground[nx][ny].remove(gun[i])







#main 함수 시작
for _ in range(k):
    for i in range(m):
        move_player(i) 
print(" ".join(map(str,points)))
