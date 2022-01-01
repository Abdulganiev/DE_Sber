select a.flight_id_1,
       b.flight_id_2,
       (a.amount_1+b.amount_2) as total_amount
from
(select arrival_airport,
       f.flight_id as flight_id_1,
       scheduled_arrival,
       min(amount) as amount_1
 from flights f inner join ticket_flights tf on f.flight_id=tf.flight_id and f.departure_airport='SVO' and f.arrival_airport!='HMA'
 group by arrival_airport, f.flight_id, scheduled_departure) a,

(select departure_airport,
       f.flight_id as flight_id_2,
       scheduled_departure,
       min(amount) as amount_2
 from flights f inner join ticket_flights tf on f.flight_id=tf.flight_id and f.arrival_airport='HMA' and departure_airport!='SVO'
 group by departure_airport, f.flight_id, scheduled_departure) b
 
where a.arrival_airport=b.departure_airport and a.scheduled_arrival<b.scheduled_departure
group by a.flight_id_1, b.flight_id_2, total_amount
order by total_amount asc