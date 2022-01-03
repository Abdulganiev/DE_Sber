/*Задание: 1 (Serge I: 2002-09-30)
Найдите номер модели, скорость и размер жесткого диска для всех ПК стоимостью менее 500 дол. Вывести: model, speed и hd*/

select
   model,
   speed,
   hd
from PC
where price < 500;

/*Задание: 2 (Serge I: 2002-09-21)
Найдите производителей принтеров. Вывести: maker*/

select 
	distinct maker
from Product
where type = 'Printer';

/*Задание: 3 (Serge I: 2002-09-30)
Найдите номер модели, объем памяти и размеры экранов ПК-блокнотов, цена которых превышает 1000 дол.*/

select 
	model, 
	ram, 
	screen
from Laptop
where price > 1000;

/*Задание: 4 (Serge I: 2002-09-21)
Найдите все записи таблицы Printer для цветных принтеров.*/

select *
from Printer
where color = 'y';

/*Задание: 5 (Serge I: 2002-09-30)
Найдите номер модели, скорость и размер жесткого диска ПК, имеющих 12x или 24x CD и цену менее 600 дол.*/

select 
	model, 
	speed, 
	hd
from PC
where cd in ('12x', '24x') and price < 600;

/*Задание: 6 (Serge I: 2002-10-28)
Для каждого производителя, выпускающего ПК-блокноты c объёмом жесткого диска не менее 10 Гбайт, найти скорости таких ПК-блокнотов. Вывод: производитель, скорость.*/

select 
	distinct maker, 
	speed
from Product p
	inner join Laptop l on p.model=l.model and l.hd>=10;

/*Задание: 7 (Serge I: 2002-11-02)
Найдите номера моделей и цены всех имеющихся в продаже продуктов (любого типа) производителя B (латинская буква).*/

select 
	distinct t1.model, 
	t2.price
from Product t1
inner join
(select model, price from pc
  union all
 select model, price from Laptop
  union all
 select model, price from Printer) t2
  on t1.model=t2.model and t1.maker='B';

select 
  t1.model, 
	t2.price
from Product t1
inner join
(select model, price from pc
  union
 select model, price from Laptop
  union
 select model, price from Printer) t2
  on t1.model=t2.model and t1.maker='B';

/*Задание: 8 (Serge I: 2003-02-03)
Найдите производителя, выпускающего ПК, но не ПК-блокноты.*/

select maker
from Product t1
where type = 'PC'
 EXCEPT
select maker
from Product t1
where type = 'Laptop'

select distinct
 t1.maker
from (
 select 
  maker
 from product t1
 where type = 'PC'
) t1
left join (
 select 
  maker
 from product t1
 where type = 'laptop'
) t2
on t1.maker = t2.maker
where t2.maker is null


select distinct 
 maker 
from Product
where type = 'PC' 
and maker not in (
 select 
  maker
 from Product 
 where type = 'laptop' 
)
/*Задание: 9 (Serge I: 2002-11-02)
Найдите производителей ПК с процессором не менее 450 Мгц. Вывести: Maker*/

select distinct maker
from Product t1
	inner join PC t2
		on t1.model=t2.model and t2.speed >= 450;
		
/*Задание: 10 (Serge I: 2002-09-23)
Найдите модели принтеров, имеющих самую высокую цену. Вывести: model, price*/		

select 
	model, 
	price
from Printer
where price = (select max(price) max_price from Printer)

/*Задание: 11 (Serge I: 2002-11-02)
Найдите среднюю скорость ПК.*/

select avg(speed)
from pc

/*Задание: 12 (Serge I: 2002-11-02)
Найдите среднюю скорость ПК-блокнотов, цена которых превышает 1000 дол.*/

Select avg(speed)
from Laptop
where price > 1000

/*Задание: 13 (Serge I: 2002-11-02)
Найдите среднюю скорость ПК, выпущенных производителем A.*/

Select avg(t1.speed)
from PC t1
	inner join Product t2 
	on t1.model=t2.model and t2.maker='A'
	
/*Задание: 14 (Serge I: 2002-11-05)
Найдите класс, имя и страну для кораблей из таблицы Ships, имеющих не менее 10 орудий.*/

Select 
	t1.class, 
	t1.name, 
	t2.country
from Ships t1 
	inner join Classes t2 
	 on t1.class=t2.class and t2.numGuns >= 1
	 
/*Задание: 15 (Serge I: 2003-02-03)
Найдите размеры жестких дисков, совпадающих у двух и более PC. Вывести: HD*/

Select hd
from pc
group by hd
having count(hd)>1

/*Задание: 16 (Serge I: 2003-02-03)
Найдите пары моделей PC, имеющих одинаковые скорость и RAM. В результате каждая пара указывается только один раз, 
т.е. (i,j), но не (j,i), Порядок вывода: модель с большим номером, модель с меньшим номером, скорость и RAM.*/
Select distinct t1.model, t2.model, t1.speed, t1.ram
from pc t1
inner join pc t2 
on t1.speed=t2.speed and t1.ram=t2.ram and t1.model > t2.model

/*Задание: 17 (Serge I: 2003-02-03)
Найдите модели ПК-блокнотов, скорость которых меньше скорости каждого из ПК.
Вывести: type, model, speed*/

Select 
	distinct t2.type, 
	t1.model, 
	t1.speed
from Laptop t1
	inner join Product t2 on t1.model=t2.model
   and t1.speed < (select min(speed) from pc)

select distinct
 'Laptop' as type,
 model,
 speed
from Laptop
where speed < (select min(speed) from pc)   

/*Задание: 18 (Serge I: 2003-02-03)
Найдите производителей самых дешевых цветных принтеров. Вывести: maker, price*/

Select 
	distinct t1.maker, 
	t2.price
from Product t1
	inner join Printer t2 
	 on t1.model=t2.model and t2.color='y'
where t2.price = (select min(price) from Printer where color='y')

/*Задание: 19 (Serge I: 2003-02-13)
Для каждого производителя, имеющего модели в таблице Laptop, найдите средний размер экрана выпускаемых им ПК-блокнотов.
Вывести: maker, средний размер экрана.*/

Select 
	t1.maker, 
	avg(t2.screen) as 'средний размер экрана'
from Product t1
	inner join Laptop t2 
		on t1.model=t2.model
group by t1.maker

/*Задание: 20 (Serge I: 2003-02-13)
Найдите производителей, выпускающих по меньшей мере три различных модели ПК. Вывести: Maker, число моделей ПК.*/

Select 
	Maker,
	count(model) as 'число моделей ПК'
from Product
where type='PC'
group by Maker
having count(model)>=3

/*Задание: 21 (Serge I: 2003-02-13)
Найдите максимальную цену ПК, выпускаемых каждым производителем, у которого есть модели в таблице PC.
Вывести: maker, максимальная цена.*/

Select 
	t1.maker, 
	max(t2.price) as 'максимальная цена'
from Product t1
	inner join pc t2 
		on t1.model=t2.model
group by t1.maker

/*Задание: 22 (Serge I: 2003-02-13)
Для каждого значения скорости ПК, превышающего 600 МГц, определите среднюю цену ПК с такой же скоростью. Вывести: speed, средняя цена.*/

select 
	speed, 
	avg(price) as 'средняя цена'
from pc
where speed > 600
group by speed

/*Задание: 23 (Serge I: 2003-02-14)
Найдите производителей, которые производили бы как ПК
со скоростью не менее 750 МГц, так и ПК-блокноты со скоростью не менее 750 МГц.
Вывести: Maker*/

Select t1.Maker
  from Product t1
   inner join pc t2 on t1.model=t2.model and t2.speed >= 750
INTERSECT
Select t1.Maker
  from Product t1
   inner join Laptop t3 on t1.model=t3.model and t3.speed >= 750
   
/*Задание: 24 (Serge I: 2003-02-03)
Перечислите номера моделей любых типов, имеющих самую высокую цену по всей имеющейся в базе данных продукции.*/

WITH all_product as
(select model, price from pc
  union all
 select model, price from Laptop
  union all
 select model, price from Printer
  ) 
select distinct model
from all_product
where price = (select max(price) from all_product)

/*Задание: 25 (Serge I: 2003-02-14)
Найдите производителей принтеров, которые производят ПК с наименьшим объемом RAM и с самым быстрым процессором среди всех ПК, имеющих наименьший объем RAM. Вывести: Maker*/

with 
 min_ram as
  (select model, speed 
    from pc where ram = (Select min(ram) from pc))
select maker
from Product where model in
  (select model
     from min_ram 
      where speed=(select max(speed) 
                      from min_ram))
 intersect
select distinct Maker from product where type='Printer'

/*Задание: 26 (Serge I: 2003-02-14)
Найдите среднюю цену ПК и ПК-блокнотов, выпущенных производителем A (латинская буква). Вывести: одна общая средняя цена.*/

with PC_Laptop as 
(select model, price
  from PC
  union all
 select model, price
  from Laptop)
select avg(price)
 from PC_Laptop t1 
  inner join Product t2 on t1.model=t2.model and t2.maker='A'
  
 /*Задание: 27 (Serge I: 2003-02-03)
Найдите средний размер диска ПК каждого из тех производителей, которые выпускают и принтеры. Вывести: maker, средний размер HD.*/

select 
	t1.maker, 
	avg(t2.hd)
 from Product t1
      inner join pc t2 
	  on t1.model=t2.model and
         t1.maker in (Select distinct maker
                       from Product
                        where type='Printer')
group by t1.maker

/*Задание: 28 (Serge I: 2012-05-04)
Используя таблицу Product, определить количество производителей, выпускающих по одной модели.*/

with count_model as
(select count(*) as qwe
  from product
 group by maker
 having count(*)=1)
select count(*) as qaz
from count_model

-- или

select count(*) as qaz
from 
(select count(*) as qwe
  from product
 group by maker
 having count(*)=1) t
 
/*Задание: 29 (Serge I: 2003-02-14)
В предположении, что приход и расход денег на каждом пункте приема фиксируется не чаще одного раза в день 
[т.е. первичный ключ (пункт, дата)], написать запрос с выходными данными (пункт, дата, приход, расход). Использовать таблицы Income_o и Outcome_o.*/

select 
 (case when t1.point is null then t2.point else t1.point end) as point,
 (case when t1.date is null then t2.date else t1.date end) as date,
 t1.inc,
 t2.out
from
(Select point, date, inc
 from Income_o) t1
 full join
(Select point, date, out
 from Outcome_o) t2
  on t1.point=t2.point and t1.date=t2.date
  
/*Задание: 30 (Serge I: 2003-02-14)
В предположении, что приход и расход денег на каждом пункте приема фиксируется произвольное число раз (первичным ключом в таблицах является столбец code), 
требуется получить таблицу, в которой каждому пункту за каждую дату выполнения операций будет соответствовать одна строка.
Вывод: point, date, суммарный расход пункта за день (out), суммарный приход пункта за день (inc). Отсутствующие значения считать неопределенными (NULL).*/

select point, date, sum(out), sum(inc)
from
(Select point, date, inc, null as out
 from Income
 union all
 Select point, date, null as inc, out
 from Outcome) t
group by point, date