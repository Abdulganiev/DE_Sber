count = int(input())
lst = []
check_lst = []
final = []
for key in range(count):
    string=input().split(',')
    [lst.append(int(el)) for el in string]
    [check_lst.append(string)]
unique = sorted(list(set(lst)))
dubl=0
for el in unique:
    for row in check_lst:
        if str(el) in row:
            dubl += 1
        else:
            dubl = 0
            break
    if dubl == len(check_lst):
        final.append(el)
        dubl = 0
print(*final, sep=',')