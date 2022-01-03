/*Задание: 31 (Serge I: 2002-10-22)
Для классов кораблей, калибр орудий которых не менее 16 дюймов, укажите класс и страну.*/

Select 
	class, 
	country
from Classes
where bore >= 16

/*Одной из характеристик корабля является половина куба калибра его главных орудий (mw). 
С точностью до 2 десятичных знаков определите среднее значение mw для кораблей каждой страны, у которой есть корабли в базе данных.*/

Select 
	country, 
	cast(avg((power(bore,3)/2)) as numeric(6,2)) as weight
from 
 (select 
	t1.country, 
	t1.bore, 
	t2.name 
   from classes t1 left join ships t2
    on t1.class=t2.class
   union 
  select 
	distinct t1.country, 
	t1.bore, 
	t2.ship 
   from classes t1 left join outcomes t2 
	 on t1.class=t2.ship	 
 ) a
where name IS NOT NULL 
group by country

/*Задание: 33 (Serge I: 2002-11-02)
Укажите корабли, потопленные в сражениях в Северной Атлантике (North Atlantic). Вывод: ship.*/

Select ship
from Outcomes 
where battle = 'North Atlantic' and result='sunk'

/*Задание: 34 (Serge I: 2002-11-04)
По Вашингтонскому международному договору от начала 1922 г. 
запрещалось строить линейные корабли водоизмещением более 35 тыс.тонн. 
Укажите корабли, нарушившие этот договор (учитывать только корабли c известным годом спуска на воду). Вывести названия кораблей.*/

select t1.name
from Battles t1
	left join Ships t2
	on DATEPART(year, t1.date)=t2.launched 
where t2.launched is null

select distinct t2.name
from Classes t1 inner join Ships t2
	on t1.class=t2.class and t1.displacement>35000 
	and t2.launched >= 1922  and type='bb'
	
/*Задание: 35 (qwrqwr: 2012-11-23)
В таблице Product найти модели, которые состоят только из цифр или только из латинских букв (A-Z, без учета регистра).
Вывод: номер модели, тип модели.*/

SELECT 
	model, 
	type 
FROM Product
WHERE model NOT LIKE '%[^0-9]%' OR model NOT LIKE '%[^a-zA-Z]%'

/*Задание: 36 (Serge I: 2003-02-17)
Перечислите названия головных кораблей, имеющихся в базе данных (учесть корабли в Outcomes).*/

select distinct name 
from 
(select t1.class, t2.name 
   from classes t1 left join ships t2
    on t1.class=t2.class
   union 
 select t1.class, t2.ship 
   from classes t1 left join outcomes t2 
    on t1.class=t2.ship) a
where class=name

/*Задание: 37 (Serge I: 2003-02-17)
Найдите классы, в которые входит только один корабль из базы данных (учесть также корабли в Outcomes).*/

select class 
from
(select t1.class, t2.name 
   from classes t1 left join ships t2
    on t1.class=t2.class
   union 
 select t1.class, t2.ship 
   from classes t1 left join outcomes t2 
    on t1.class=t2.ship) a
where name is not null
group by class
having count(name)=1

/*Задание: 38 (Serge I: 2003-02-19)
Найдите страны, имевшие когда-либо классы обычных боевых кораблей ('bb') и имевшие когда-либо классы крейсеров ('bc').*/

Select distinct t1.country  
from Classes t1
	inner join Classes t2
	on t1.country=t2.country and t1.type='bb' and t2.type='bc'
	
/*Задание: 39 (Serge I: 2003-02-14)
Найдите корабли, `сохранившиеся для будущих сражений`; т.е. выведенные из строя в одной битве (damaged), они участвовали в другой, произошедшей позже.*/

select distinct t1.ship
   from outcomes t1 inner join outcomes t2
   on t1.ship=t2.ship and t1.result='damaged' and t1.battle != t2.battle
   inner join battles t3 
   on t1.battle=t3.name 
   inner join battles t4
   on t2.battle=t4.name
where t4.date>t3.date

/*Задание: 40 (Serge I: 2012-04-20)
Найти производителей, которые выпускают более одной модели, при этом все выпускаемые производителем модели являются продуктами одного типа.
Вывести: maker, type*/

select distinct maker, type
from Product
where maker in
(select c2.maker
  from
   (select maker
     from
      (Select distinct maker, type
        from Product) a
    group by maker
    having count(type)=1) c1
   inner join Product c2 on c1.maker=c2.maker
 group by c2.maker
 having count(c2.model)>1)
 
/*Задание: 41 (Serge I: 2019-05-31)
Для каждого производителя, у которого присутствуют модели хотя бы в одной из таблиц PC, Laptop или Printer, определить максимальную цену на его продукцию.
Вывод: имя производителя, если среди цен на продукцию данного производителя присутствует NULL, то выводить для этого производителя NULL,
иначе максимальную цену.*/

select maker,
	(case when ch=0 then max_price else null end) as price
from
(select maker, max(price) as max_price, 
	max(case when price is null then 1 else 0 end) as ch
from
(Select t1.maker, t2.price
  from Product t1
   inner join PC t2 on t1.model=t2.model
  union all
 Select t1.maker, t2.price
   from Product t1
    inner join Laptop t2 on t1.model=t2.model
  union all
 Select t1.maker, t2.price
   from Product t1
    inner join Printer t2 on t1.model=t2.model) a
group by maker) a

/*Задание: 42 (Serge I: 2002-11-05)
Найдите названия кораблей, потопленных в сражениях, и название сражения, в котором они были потоплены.*/

Select t1.ship, t1.battle
from Outcomes t1
	inner join Battles t2 
	on t1.battle=t2.name and t1.result='sunk'
	
/*Задание: 43 (qwrqwr: 2011-10-28)
Укажите сражения, которые произошли в годы, не совпадающие ни с одним из годов спуска кораблей на воду.*/	

select distinct t1.name
from Battles t1
    left join ships t2
on DATEPART(YEAR, t1.date)=t2.launched
where t2.launched is null

/*Задание: 44 (Serge I: 2002-12-04)
Найдите названия всех кораблей в базе данных, начинающихся с буквы R.*/

select distinct a.name
from
(select name 
   from ships t2
   union all 
 select ship 
   from outcomes) a
where a.name like ('R%')

/*Задание: 45 (Serge I: 2002-12-04)
Найдите названия всех кораблей в базе данных, состоящие из трех и более слов (например, King George V).
Считать, что слова в названиях разделяются единичными пробелами, и нет концевых пробелов.*/

select distinct a.name
from
(select name 
   from ships t2
   union all 
 select ship 
   from outcomes) a
where a.name like ('% % %')

/*Задание: 46 (Serge I: 2003-02-14)
Для каждого корабля, участвовавшего в сражении при Гвадалканале (Guadalcanal), вывести название, водоизмещение и число орудий.*/

select t2.ship, t3.displacement, t3.numGuns
   from outcomes t2 
        left join Ships t1 
      on t1.name=t2.ship
        left join Classes t3
      on t1.class=t3.class or t2.ship=t3.class 
   where t2.battle='Guadalcanal'


/*Задание: 47 (Serge I: 2019-06-07)
Определить страны, которые потеряли в сражениях все свои корабли.*/




   /*Задание: 151 (Serge I: 2009-04-17)
Для каждого корабля из таблицы Ships указать название первого по времени сражения из таблицы Battles,
в котором корабль мог бы участвовать после спуска на воду. Если год спуска на воду неизвестен, взять последнее по времени сражение.
Если нет сражения, произошедшего после спуска на воду корабля, вывести NULL вместо названия сражения.
Считать, что корабль может участвовать во всех сражениях, которые произошли в год спуска на воду корабля.
Вывод: имя корабля, год спуска на воду, название сражения

Замечание: считать, что не существует двух битв, произошедших в один и тот же день.*/

with ship_battle as
(select 
  t1.name,
  t1.launched,
  min(t2.date) as min_date
 from Ships t1
  left join 
     Battles t2
   on t1.launched <= DATEPART(YEAR, t2.date) 
group by t1.name, t1.launched),
max_battle as 
(select name from Battles where date =
   (select max(date) as max_date from Battles))

select t1.name, t1.launched, 
(case 
   when t1.launched > (select max(date) from Battles)
    then null
   when t1.launched is null
    then (select name from max_battle)
   else t2.name end) as name

from ship_battle t1
 left join Battles t2
on t1.min_date=t2.date