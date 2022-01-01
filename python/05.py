count = int(input(''))
flights = []
for row in range(count):
    ticket_no, flight_id, boarding_no, seat_no = input().split(',')
    flights.append(flight_id)
unique = dict(zip(list(flights),[list(flights).count(i) for i in list(flights)]))
max_ = 0
for key, value in unique.items():
    if max_ < value:
        max_ = int(value)
max_flights = []
for key, value in unique.items():
    if max_ == value:
        max_flights.append(int(key))
max_flights.sort()
for i in max_flights:
    print(i, end=' ')