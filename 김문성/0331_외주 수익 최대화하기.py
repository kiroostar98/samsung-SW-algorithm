# O(2^N)

N=int(input())
work = [(0,0,0)]


for idx in range(1,N+1):
    t,p = map(int,input().split())
    # start / end / pay
    work.append((idx,idx+t,p))


ans = 0 
def tracking(idx,workqueue):
    global ans
    if idx == N+1: # 끝까지 순회 완.
        total_cost = 0
        for w in workqueue:
            total_cost += w[2]
        # print("done : {}, workqueue : {}".format(total_cost,workqueue))
        # 전체 페이와 비교.
        ans = max(ans,total_cost)
        return
    
    # idx 넣을 수 있는가?
    (last_start,last_end,last_pay) = workqueue[-1]
    (cur_start,cur_end,cur_pay) = work[idx]
    
    if last_end > cur_start or cur_end > N+1: # 가장 뒷 작업이 끝나지 않음. > 작업 불가.
        next = workqueue[:]
        tracking(idx+1,next)
        return
    
    else: # 해당 작ㅇ버을 추가할 수 있다면.
        next = workqueue[:]
        tracking(idx+1,next) # 해당 작업 수행 않는 경우.
        next.append((cur_start,cur_end,cur_pay))
        tracking(idx+1,next) # 해당 작업 수행하는 경우.
        return 

tracking(1,[(0,0,0)])
print(ans)
    