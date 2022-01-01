/*6. Рейсы из Москвы[1]
Необходимо для каждого дня недели найти суммарное количество рейсов из аэропортов Москвы. 
Вхождения в выборку должны быть упорядочены по убыванию числа рейсов.
Примечание
airport_code московских аэропортов это SVO, VKO, DME.
День недели - это число, где 0 - это воскресенье, 1 - это понедельник и т.д.
Возможно, для решения задачи понадобится инструкция по работе с датами из введения.
Считать нужно все рейсы вне зависимости от их статуса.*/

select cast(strftime('%w',scheduled_departure) as integer) as day_of_week, 
       count(departure_airport) as flights 
from flights
where departure_airport in ('SVO', 'VKO', 'DME')
group by day_of_week
order by flights desc