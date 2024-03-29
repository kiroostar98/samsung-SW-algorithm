# 바이러스 검사.
# Greedy.
# O(N).
N=int(input())
store = list(map(int,input().split()))
chief, assist = map(int,input().split())

ans = 0
chief_req = 1
assist_req = 0

# 각 가게 별 최소. > 그 중 최대값
max_req = 1

def how_many_req(cus, chief, assist):
    ans = 1
    if chief >= cus: # 모든 고객을 팀장 혼자 충당 가능
        return ans
    else:
        cus-=chief
        ans += cus//assist
        if cus%assist!=0:
            ans+=1 # assist 한명 더 필요.
        return ans

ans=0
for idx in range(N):
    customer = store[idx]
    ans += how_many_req(customer, chief, assist)

print(ans)