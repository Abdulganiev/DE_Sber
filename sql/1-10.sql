/*
10. Отмена рейсов[3]
Исследуется распределение отмененных рейсов по городам. 
Необходимо вывести пять городов, рейсы из которых отменяли чаще всего, а также количество отмен. 
Вхождения в выборку должны быть упорядочены по убыванию числа отмененных рейсов.
*/

select a.city, 
       count(*) as cancelled_flights_number
from flights f inner join airports a on
        f.departure_airport=a.airport_code
        and f.status='Cancelled'
group by a.city
order by cancelled_flights_number desc
limit 5