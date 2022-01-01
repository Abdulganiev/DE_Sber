/*
Необходимо вывести все модели самолетов, на которых был совершен хотя бы один рейс, с указанием количества рейсов, выполненных на каждой модели. 
Рейс считается выполненным, если самолет прибыл в пункт назначения. 
Элементы выборки должны быть упорядочены по убыванию числа рейсов.
*/
select model, 
      count(*) as flights_num
from aircrafts
     inner join flights using(aircraft_code)
where status='Arrived'
group by model
order by flights_num desc