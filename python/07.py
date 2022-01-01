count = int(input(''))
flights = []
bilets = {}
for row in range(count):
    ticket_no, flight_id, boarding_no, seat_no = input().split(',')
    flights.append(int(flight_id))
    bilets[row] = ticket_no  + ',' + flight_id + ',' + boarding_no + ',' + seat_no
flights.sort()
unique = dict(zip(list(flights),[list(flights).count(i) for i in list(flights)]))
for i in unique:
    seat = []
    print(i)
    for value in bilets.values():
        ticket_no, flight_id, boarding_no, seat_no = value.split(',')
        if i == int(flight_id):
            seat.append(seat_no)
    print(','.join(seat))