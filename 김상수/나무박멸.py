import sys
input = sys.stdin.readline



n, m, k, c = map(int, input().split())
dx = [-1,1,0,0]
dy = [0,0,-1,1]
Dx = [-1,-1,1,1]
Dy = [-1,1,-1,1]
forest = []
for i in range(n):
    forest.append(list(map(int, input().split())))
answer = 0
painkiller = [[0]*n for _ in range(n)]

def get_empty_space(x,y):
    empty_space = []
    for u in range(4):
        nx = x +dx[u]
        ny = y +dy[u]
        if 0<= nx <n and 0<= ny <n and not forest[nx][ny] and not painkiller[nx][ny]:
            empty_space.append(u)

    return empty_space

def near_tree_num(x,y):
    tree_num = 0
    for o in range(4):
        nx = x +dx[o]
        ny = y +dy[o]
        if 0<= nx <n and 0<= ny <n and forest[nx][ny] > 0:
            tree_num += 1

    return tree_num


# 살충제 뿌릴 곳 찾기
def get_painkiller_space():
    can_kill_trees = [[0]*n for _ in range(n)]
    max_trees = 0
    painkiller_space = (0,0)
    for i in range(n):
        for j in range(n):
            if forest[i][j]>0:
                can_kill_trees[i][j] += forest[i][j]
                for p in range(4):
                    for q in range(k):
                        ni = i + Dx[p] *(q+1)
                        nj = j + Dy[p] *(q+1)
                        if 0<= ni <n and 0<= nj <n and forest[ni][nj] > 0:
                            can_kill_trees[i][j] += forest[ni][nj]
                        else:
                            break
    # print(can_kill_trees)

    for i in range(n):
        for j in range(n):
            if can_kill_trees[i][j] > max_trees:
                painkiller_space = (i,j)
                max_trees = can_kill_trees[i][j]
    
    return painkiller_space, max_trees

def tree_growth():
    new_trees = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if forest[i][j] > 0:
                forest[i][j] += near_tree_num(i,j)
                empty_space = get_empty_space(i,j)
                s = len(empty_space)
                for p in empty_space:
                    ni = i +dx[p]
                    nj = j +dy[p]
                    if 0<= ni <n and 0<= nj <n and not painkiller[ni][nj]:
                        new_trees[ni][nj] +=forest[i][j]//s
    for i in range(n):
        for j in range(n):
            forest[i][j] += new_trees[i][j]
    
    return

for _ in range(m):
    # print(forest)
    tree_growth()
    # print(forest)
    result = get_painkiller_space()
    # print(result)
    a,b = result[0]
    answer += result[1]
    for i in range(n):
        for j in range(n):
            if painkiller[i][j] >0:
                painkiller[i][j] -= 1
    
    painkiller[a][b] = c
    forest[a][b] = 0
    for p in range(4):
        for q in range(k):
            nx = a +Dx[p]*(q+1)
            ny = b +Dy[p]*(q+1)
            if 0<= nx <n and 0<= ny <n:
                if forest[nx][ny] > 0:
                    painkiller[nx][ny] = c
                    forest[nx][ny] = 0
                else:
                    painkiller[nx][ny] = c
                    break
    # print(forest)
    # print(painkiller)

print(answer)
    

