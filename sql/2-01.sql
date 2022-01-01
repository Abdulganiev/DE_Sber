/*
1. Разгрузка летного пространства
Необходимо найти аэропорты вылета, из которых рейсы летают во Внуково (VKO), но не в Шереметьево (SVO).
То есть был запланирован рейс из данного аэропорта во Внуково, но ни разу не был запланирован рейс в Шереметьево.
Все значения должны быть уникальны.
*/

select departure_airport
from flights
where arrival_airport in ('VKO') 
      and departure_airport not in 
(select departure_airport
 from flights
 where arrival_airport in ('SVO')
 group by departure_airport)
group by departure_airport