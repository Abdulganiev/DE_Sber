select * from hr.jobs;
select * from hr.employees

select t1.FIRST_NAME, t1.LAST_NAME, t2.JOB_TITLE
from hr.jobs t1 inner join hr.employees t2
on t1.JOB_ID=t2.JOB_ID

select JOB_TITLE
from hr.jobs
minus
select t1.JOB_TITLE
from hr.jobs t1 inner join hr.employees t2
on t1.JOB_ID=t2.JOB_ID

select t1.JOB_TITLE
from hr.jobs t1 left join hr.employees t2
on t1.JOB_ID=t2.JOB_ID
where t2.EMPLOYEE_ID is null

select t1.JOB_TITLE
from hr.jobs t1 RIGHT  join hr.employees t2
on t1.JOB_ID=t2.JOB_ID
where t1.MIN_SALARY is null

-------------------------------------
select * from hr.jobs;
select * from hr.employees

select JOB_TITLE
from
(select t1.JOB_TITLE, 
       count(t2.EMPLOYEE_ID)
from hr.jobs t1 
     inner join hr.employees t2
on t1.JOB_ID=t2.JOB_ID
group by t1.JOB_TITLE
order by count(t2.EMPLOYEE_ID) desc)
where rownum=1

select JOB_TITLE 
  from hr.jobs 
  where JOB_ID in

(select t1.JOB_ID
from 
   (select JOB_ID, 
       count(*) as mx
        from hr.employees group by JOB_ID) t1
  inner join
  (select max(mx) as max_mx from
     (select count(*) as mx from hr.employees group by JOB_ID)
     ) t2 on t1.mx=t2.max_mx)
     
with mx_table as
(select JOB_ID, 
       count(*) as mx
        from hr.employees group by JOB_ID)
select JOB_TITLE 
  from hr.jobs 
  where JOB_ID in        
    (select JOB_ID
      from mx_table t1 inner join
           (select max(mx) as max_mx from mx_table) t2
          on t1.mx=t2.max_mx)


select * from oe.customers
select * from oe.orders

select t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME, t2.* --ORDER_ID
from oe.customers t1 left join oe.orders t2
on t1.CUSTOMER_ID=t2.CUSTOMER_ID
order by t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME, t2.ORDER_ID

select t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME, sum(t2.ORDER_TOTAL)
from oe.customers t1 left join oe.orders t2
on t1.CUSTOMER_ID=t2.CUSTOMER_ID
group by t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME
having SUM(T2.ORDER_TOTAL) is not null
order by /*t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME,*/ sum(t2.ORDER_TOTAL) desc

select t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME, NVL(sum(t2.ORDER_TOTAL), 0) as mx1, coalesce(sum(t2.ORDER_TOTAL), 0) as mx1
from oe.customers t1 left join oe.orders t2
on t1.CUSTOMER_ID=t2.CUSTOMER_ID
group by t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME
order by /*t1.CUST_FIRST_NAME, t1.CUST_LAST_NAME,*/ sum(t2.ORDER_TOTAL) desc



select *
 from hr.employees where length(EMAIL)=(select max(length(EMAIL)) from hr.employees)
 
select * from hr.jobs;

select JOB_ID,
substr(JOB_ID, instr(JOB_ID, '_')+1) as v2,
substr(JOB_TITLE,1 , length(substr(JOB_ID, instr(JOB_ID, '_')+1))) as v1
from hr.jobs
where lower(substr(JOB_ID, instr(JOB_ID, '_')+1))=lower(substr(JOB_TITLE,1 , length(substr(JOB_ID, instr(JOB_ID, '_')+1))))




create table dataSource (
	first_name varchar(255),
	last_name varchar(255),
	email varchar(255),
	gender varchar(255)
);


insert into dataSource (first_name, last_name, email, gender) values 
		(null,                      'Hilda Sodo',           'hsodo1o@surveymonkey.com',                       'F');
insert into dataSource (first_name, last_name, email, gender) values 
		('Torin Cardus',             null,                  'tcardus21@ow.ly',                                'Male');
insert into dataSource (first_name, last_name, email, gender) values 
		(null,                      'Artur MacShane',       'amacshane2d@princeton.edu',                      'M');
insert into dataSource (first_name, last_name, email, gender) values 
		('Freedman Krause',          null,                  'fkrause5t@dagondesign.com',                      'Male');
insert into dataSource (first_name, last_name, email, gender) values 
		(null,                      'Lemmers Remington',    'rlemmers70@tripod.com',                          'Male');
insert into dataSource (first_name, last_name, email, gender) values 
		('Tucker',                  'Crauford',             'tcraufords@chicagotribune.com +7 9346553 221',   'M');
insert into dataSource (first_name, last_name, email, gender) values 
		('Winfield',                'Sharpe',               'wsharpe5k@amazon.co.jp +7-912-321-84-43',        'Male');
insert into dataSource (first_name, last_name, email, gender) values 
		('Caresa',                  'Symmers',              '+79824433556',                                   'F');
insert into dataSource (first_name, last_name, email, gender) values 
		('Rosita',                  'McGing',               'rmcging5@nps.gov 89235428443',                   'Female');
insert into dataSource (first_name, last_name, email, gender) values 
		('Elinor',                  'Barca',                'ebarca54@ning.com 89022338843',                  'Female');
insert into dataSource (first_name, last_name, email, gender) values 
		('Paxon',                   'Rimington',            '89094235643',                   				  'Male');
insert into dataSource (first_name, last_name, email, gender) values 
		('Truda',                   'Biffin',               'tbiffin89@wired.com',                            'F');
insert into dataSource (first_name, last_name, email, gender) values 
		('Noland',                  'Buesden',              '893265432 85',                                   'Male');
insert into dataSource (first_name, last_name, email, gender) values 
		('Brana Champion',           null,                  'bchampiondv@csmonitor.com',                      'Female');
		
		
select * from dataSource;

select distinct GENDER from dataSource;

select GENDER, 
(case GENDER
  when 'F' then 0
  when 'M' then 1
  when 'Male' then 1
  when 'Female' then 0
  end) as GENDER_2,
  instr(gender, 'M') as gender_1
from dataSource

select * from dataSource;

/*
1) в FIRST_NAME имя, оставляем как есть
2) в FIRST_NAME null, забрать первое слово из lastname
2) в FIRST_NAME 2 слова, забрать первое слово из FIRST_NAME*/

select FIRST_NAME ,
(case 
  when FIRST_NAME is null then LAST_NAME
  when FIRST_NAME is not null then '2'
  else FIRST_NAME
 end) as v2
from dataSource