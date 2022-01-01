/*
2. Самый дорогой билет в бизнес-классе
Нужно найти максимальную стоимость билета в бизнес-классе для каждой модели самолета.
Выводить в порядке убывания стоимости.
*/
select a.model as model,
       max(tf.amount) as amount
from ticket_flights tf
     inner join flights f on tf.flight_id=f.flight_id
     inner join aircrafts a on f.aircraft_code=a.aircraft_code
where tf.fare_conditions='Business'
group by a.model 
order by amount desc