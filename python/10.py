count = int(input(''))
stat = {
    'Scheduled' : 0,
    'On Time' : 0,
    'Delayed' : 0,
    'Departed' : 0,
    'Arrived' : 0,
    'Cancelled' : 0
    }
for row in range(count):
    flight_id, status = input().split(',')
    for key, value in stat.items():
        if key == status:
            stat[key] += 1
for value in stat.values():
    print(value)