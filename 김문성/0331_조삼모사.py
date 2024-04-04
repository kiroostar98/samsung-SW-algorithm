#모든 조합에 대하여, 오전/오후 강도 차이의 최솟값.
# 차이 적게. > 모두해봐야.
# 4<=n<=20, 짝수.
# P <=100, Pii = 0



N=int(input())
property=[list(map(int,input().split())) for _ in range(N)]
#ans 최대차이 : 20*20 > 200개 200개 > 200_P_2 * 100 = 4000000
ans = 4000000

AM=[]
PM=[]

def grouping(idx): # 2개 group으로 분할.
    global ans
    if idx == N: # 0~N-1 끝. > 판별.
        stress_diff = abs(group_stress(AM) - group_stress(PM))
        # print(group_stress(AM), group_stress(PM))
        # print("AM : {}, PM : {}, stress_diff : {}".format(AM,PM,stress_diff))
        if stress_diff < ans:
            ans=stress_diff
        return

    # 해당 일을 오전에
    # 절반 넘으면 안됨.
    if len(AM) < N//2:
        AM.append(idx)
        grouping(idx+1)
        AM.pop()
    if len(PM) < N//2:
        PM.append(idx)
        grouping(idx+1)
        PM.pop()

    return

def group_stress(shift): #nP2 : n*(n-1)
    stress_level=0
    for a in shift:
        for b in shift: # a==b : 0
            stress_level+=property[a][b]
            


    return stress_level


grouping(0)
print(ans)