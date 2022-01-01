count = int(input(''))
id_set = set()
for row in range(count):
    id = input().split(',')
    if row==0:
        id_set = set(list(map(int, id)))
    id_set = id_set.intersection(set(list(map(int, id))))
itog = list(id_set)
itog.sort()
print(*itog, sep=',')