/*
9. Отмена рейсов[2]
Исследуется распределение отмененных рейсов по месяцам. 
Необходимо для каждого месяца найти количество отмененных рейсов, вылет которых был запланирован на один из дней данного месяца. 
Вхождения в выборку должны быть упорядочены по возрастанию номера месяца.
*/

select cast(strftime('%m',scheduled_departure) as integer) as month, 
       count(*) as cancelled_flights_number
from flights
where status='Cancelled'
group by month
order by month asc