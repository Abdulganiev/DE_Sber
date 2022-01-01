/*
5. Убытки авиакомпании[2]
Необходимо найти недополученную из-за отмены рейсов выручку авиакомпании 
за период времени 
с 17 августа 2017 00:00:00 до 23 августа 2017 00:00:00 включительно.
Примечание
Под выручкой понимается сумма стоимостей перелета для всех отмененных рейсов. 
Например, если отменен единственный рейс с flight_id 13, а в таблице перелетов нашлось 30 вхождений, соответствующих данному рейсу, 
причем каждый перелет имеет amount равный 5000, то недополученная выручка авиакомпании равна 5000 * 30 = 150000.
*/

select sum(amount) as lost_profit
from flights f
     inner join ticket_flights tf on 
     f.flight_id=tf.flight_id 
     and f.status='Cancelled' 
     and scheduled_departure between '2017-08-17 00:00:00' and '2017-08-23 00:00:00'