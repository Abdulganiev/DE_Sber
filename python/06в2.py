st=input().split(',')
N=int(input())
for i in range(0, N):
    S=input().split(',')
    for j in st:
        #print(j)
        #print(S[1])
        if j==S[1]:
            print(','.join(S))