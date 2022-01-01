select departure_airport,
       arrival_airport,
       count(flight_id) as amount
from flights
where DATE(scheduled_departure)='2017-08-24'
group by departure_airport, arrival_airport
having count(flight_id)>1
order by amount desc, departure_airport asc, arrival_airport asc