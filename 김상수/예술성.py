import sys
input = sys.stdin.readline
from collections import deque
n = int(input())
dx = [-1, 1, 0 , 0]
dy = [0, 0, -1, 1]
picture = []
next_picture = [[0]*n for _ in range(n)]
ans = 0
group_num = 0
for i in range(n):
    picture.append(list(map(int, input().split())))

visited = [[0]*n for _ in range(n)]
group = [[0]*n for _ in range(n)]
group_cnt = [0] *(n * n + 1)


def bfs(p,q):
    global group_num
    queue = deque()
    queue.append((p,q))
    while queue:
        x, y = queue.popleft()
        print(x,y)
        group[x][y] = group_num
        group_cnt[group_num] += 1
        for o in range(4):
            nx = x + dx[o]
            ny = y + dy[o]
            if 0<= nx < n and 0<= ny < n and not visited[nx][ny] and picture[nx][ny] == picture[x][y]:
                queue.append((nx,ny))
                visited[nx][ny] = 1

    


def make_group():
    global group_num
    group_num =0
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                group_num += 1
                visited[i][j] = 1
                bfs(i,j)




def get_score():
    for i in range(n):
        for j in range(n):
            visited[i][j] = 0
    for i in range(n*n+1):
        group_cnt[i] = 0
    make_group()
    print(group_cnt)
    score = 0
    for i in range(n):
        for j in range(n):
            for k in range(4):
                nx = i +dx[k]
                ny = j +dy[k]
                if 0 <= nx <n and 0 <= ny <n and group[nx][ny] != group[i][j]:
                        score += (group_cnt[group[nx][ny]] +group_cnt[group[i][j]]) * picture[nx][ny] *picture[i][j]
                
    return score//2


def center_rotate():
    for i in range(n//2):
        next_picture[n//2][i] = picture[i][n//2]
    for i in range(n//2):
        next_picture[n-i-1][n//2] = picture[n//2][i]
    for i in range(n//2):
        next_picture[n//2][n-i-1] = picture[n-i-1][n//2]
    for i in range(n//2):
        next_picture[i][n//2] = picture[n//2][n-i-1]

def square_rotate(x,y):
    for i in range(n//2):
        for j in range(n//2):
            next_picture[x+j][y+ n//2 -i-1] = picture[x+i][y+j]







def rotate():
    for i in range(n):
        for j in range(n):
            next_picture[i][j] =0
    center_rotate()
    square_rotate(0,0)
    square_rotate(0, n//2+1)
    square_rotate(n//2+1, 0)
    square_rotate(n//2+1, n//2+1)
    next_picture[n//2][n//2] = picture[n//2][n//2]
    for i in range(n):
        for j in range(n):
            picture[i][j] = next_picture[i][j]




for _ in range(4):
    ans += get_score()
    print(ans)
    rotate()
    print(next_picture)
    print(picture)

print(ans)


# make_group()
# print(group)