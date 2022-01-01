count = int(input(''))
ids = {}
for row in range(count):
    id = input().split(',')
    id = list(map(int, id))
    id = set(id)
    ids[row] = id
id_set = set()
for value in ids.values():
    id_set = value
    id_set.intersection(value)
itog = list(id_set)
itog.sort()
if count>1:
    print(*itog, sep=',')