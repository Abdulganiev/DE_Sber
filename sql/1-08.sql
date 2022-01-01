/*
8. Отмена рейсов[1]
Исследуется распределение отмененных рейсов по аэропортам. 
Необходимо вывести три аэропорта, рейсы из которых отменяли чаще всего, а также количество отмен. 
Вхождения в выборку должны быть упорядочены по убыванию числа отмененных рейсов.
*/

select departure_airport as airport_code, 
       count(*) as cancelled_flights_number
from flights
where status='Cancelled'
group by airport_code
order by cancelled_flights_number desc
limit 3