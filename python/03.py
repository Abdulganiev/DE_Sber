count = int(input(''))
for row in range(count):
    ticket_no, flight_id, boarding_no, seat_no = input().split(',')
    if ':' in boarding_no:
        boarding_no1, boarding_no2 = boarding_no.split(':')
        boarding_no = boarding_no2    
    if ';' not in seat_no:
        seat_no = str(int(seat_no[0:-1])) + ';' + seat_no[-1]
    else:
        seat_no1, seat_no2 = seat_no.split(';')
        seat_no = str(int(seat_no1)) + ';' + seat_no2
    print(ticket_no+','+flight_id+','+boarding_no+','+seat_no)