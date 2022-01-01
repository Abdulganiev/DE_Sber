import datetime
count = int(input(''))
for row in range(count):
    scheduled_departure, scheduled_arrival, actual_departure, actual_arrival = input().split(',')
    
    scheduled_departure = datetime.datetime.strptime(scheduled_departure, '%Y-%m-%dT%H:%M')
    scheduled_arrival = datetime.datetime.strptime(scheduled_arrival, '%Y-%m-%dT%H:%M')
    actual_departure = datetime.datetime.strptime(actual_departure, '%Y-%m-%dT%H:%M')
    actual_arrival = datetime.datetime.strptime(actual_arrival, '%Y-%m-%dT%H:%M')
    
    delta_departure = actual_departure - scheduled_departure
    delta_arrival = actual_arrival -scheduled_arrival
    
    if (delta_departure.seconds < 1800) and (delta_arrival.seconds < 1800):
        print('Yes')
    else:
        print('No')