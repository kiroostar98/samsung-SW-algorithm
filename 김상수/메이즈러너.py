import sys
import copy
input = sys.stdin.readline

#입력값 받기
n, m, k = map(int, input().split())
miro = [[0]*(n+1) for _ in range(n+1)]
for i in range(1, n+1):
    miro_line = list(map(int, input().split()))
    for j in range(1, n+1):
        miro[i][j] = miro_line[j-1]

men = []
for i in range(m):
    men.append(list(map(int, input().split())))

exit = list(map(int, input().split()))
answer = 0



def is_in_range(x,y):
    if 0<x<n+1 and 0<y<n+1:
        return 1
    else:
        return 0

def move_x(x, y, z):
    global men
    if is_in_range(x+z,y):
        if not miro[x+z][y]:
            return x+z

        return 0
    return 0

def move_y(x,y,z):
    if is_in_range(x,y+z):
        if not miro[x][y+z]:
            return y+z

        return 0
    return 0

def move_men():
    global men, answer
    for i, man in enumerate(men):
        diff_x = exit[0] - man[0]
        diff_y = exit[1] - man[1]
        if diff_x:
            result_x = move_x(man[0], man[1], diff_x//abs(diff_x))
            if not result_x:
                if diff_y:
                    result_y = move_y(man[0], man[1], diff_y//abs(diff_y))
                    if result_y:
                        man[1] = result_y
                        answer += 1
            else:
                man[0] = result_x
                answer += 1

        else:
            if diff_y:
                    result_y = move_y(man[0], man[1], diff_y//abs(diff_y))
                    if result_y:
                        man[1] = result_y
                        answer += 1

        
    new_list = [x for x in men if x != exit]
    men = new_list[:]





def get_min_square():
    nx,ny,nr = 0 ,0, 100
    for man in men:
        diff_x = exit[0] - man[0]
        diff_y = exit[1] - man[1]
        if abs(diff_x) >= abs(diff_y):
            x = min(exit[0], man[0])
            r = abs(diff_x)
            if max(exit[1], man[1]) - r <= 0:
                y = 1
            else:
                y = max(exit[1], man[1]) - r

        else:
            y = min(exit[1], man[1])
            r = abs(diff_y)
            if max(exit[0], man[0]) - r <= 0:
                x = 1
            else:
                x = max(exit[0], man[0]) - r

        if nr > r:
            nx, ny, nr = x, y, r
        elif nr == r:
            if nx > x:
                nx, ny, nr = x, y, r
            elif nx == x:
                if ny > y:
                    nx, ny, nr = x, y, r

    return (nx, ny, nr)

def rotate(x, y, r):
    global miro, men, exit
    miro_temp = copy.deepcopy(miro)
    men_temp = copy.deepcopy(men)
    new_exit = copy.deepcopy(exit)
    for i in range(x, x+r+1):
        for j in range(y, y+r+1):
            if miro[i][j]:
                miro[i][j] -= 1
            for k, man in enumerate(men):
                if i == man[0] and j == man[1]:
                    men_temp[k][0] = j-y+x
                    men_temp[k][1] = r-i+x+y
            if i == exit[0] and j == exit[1]:
                new_exit[0] = j-y+x
                new_exit[1] = r-i+x+y

            miro_temp[j-y+x][r-i+x+y] = miro[i][j]
    men = copy.deepcopy(men_temp)
    miro = copy.deepcopy(miro_temp) 
    exit = copy.deepcopy(new_exit)











#메인 로직 실행
for p in range(k):
    # print(p+1, "초입니다")
    # print("miro:",miro)
    move_men()
    # print("men:", men)
    if not men:
        print(answer)
        print(" ".join(map(str, exit)))
        break
    x,y,r = get_min_square()
    # print("x,y,r", x,y,r)
    rotate(x,y,r)
    # print("rotate 후", men)
    # print("rotate후 exit:", exit )
    if p==k-1:
        print(answer)
        print(" ".join(map(str, exit)))



    