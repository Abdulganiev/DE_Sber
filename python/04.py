count = int(input(''))
bilets = {}
for row in range(count):
    ticket_no, flight_id, boarding_no, seat_no = input().split(',')
    if (ticket_no + ',' + flight_id) not in bilets:
        bilets[ticket_no + ',' + flight_id] = boarding_no +',' + seat_no
for key, value in bilets.items():
    ticket_no, flight_id = key.split(',')
    boarding_no, seat_no = value.split(',')
    print(ticket_no+','+flight_id+','+boarding_no+','+seat_no)