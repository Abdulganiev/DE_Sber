count = int(input(''))
ids = []
for row in range(count):
    id = input().split(',')
    ids += id
ids = list(map(int, ids))
unique = dict(zip(list(ids),[list(ids).count(i) for i in list(ids)]))
duplicates = []
for key, value in unique.items():
    if int(value)>1:
        duplicates.append(int(key))
duplicates.sort()
print(','.join(map(str, duplicates)))