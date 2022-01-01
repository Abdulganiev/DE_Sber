/* 3. Поиск дешевых авиабилетов
   Требуется найти все рейсы, для которых средняя стоимость перелета более 3300, но менее 5000 рублей.
   Вхождения в выборку должны быть упорядочены по возрастанию flight_id.
   Необходимо усреднять стоимость по всем билетам для данного рейса*/

select flight_id,
       avg(amount) avg_amount
from ticket_flights       
group by flight_id
having avg_amount>3300 and avg_amount<5000
order by flight_id asc