/*7. Рейсы из Москвы[2]
Необходимо для каждого аэропорта Москвы найти суммарное количество пассажиров на всех рейсах из данного аэропорта. 
Вхождения в выборку должны быть упорядочены по убыванию числа пассажиров.
Примечание
Под количеством пассажиров имеется в виду не количество уникальных клиентов, а сумма числа пассажиров на рейсах. 
Соответственно, если один человек пользовался услугами данной авиакомпании дважды и оба раза вылетал из аэропорта Шереметьево, то его вклад в сумму пассажиров на рейсах из этого аэропорта равен двум.
Примечание
airport_code московских аэропортов это SVO, VKO, DME.
День недели - это число, где 0 - это воскресенье, 1 - это понедельник и т.д.
Возможно, для решения задачи понадобится инструкция по работе с датами из введения.
Считать нужно все рейсы вне зависимости от их статуса.*/

select departure_airport as airport_code,
       count(ticket_no) as passengers
from flights f
     inner join ticket_flights tf on 
       f.flight_id=tf.flight_id
       and f.departure_airport in ('SVO', 'VKO', 'DME')
group by airport_code
order by passengers desc