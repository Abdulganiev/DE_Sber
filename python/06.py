flight = input('').split(',')
count = int(input(''))
bilets = {}
for row in range(count):
    bilet = input()
    ticket_no, flight_id, boarding_no, seat_no = bilet.split(',')
    if flight.count(flight_id)>0 :
        bilets[row] = bilet
for value in bilets.values():
    print(value)