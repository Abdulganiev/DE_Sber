drop view books;
create view books as
select 
    SUBSTR(value, 
           instr(value, '<p>') + LENGTH('<p>'), 
           instr(value, '</p>') - instr(value, '<p>')-LENGTH('<p>')) as ID,
   
    SUBSTR(value, 
           instr(value, '<h1>') + LENGTH('<h1>'), 
           instr(value, '</h1>') - instr(value, '<h1>')-4) as Categorys,
   
    coalesce(
    SUBSTR(value, 
           instr(value, '<p class="title">') + LENGTH('<p class="title">'), 
           (case 
              when instr(value, '<p class="author">') = 0
               then instr(value, '<p class="price">')
             else instr(value, '<p class="author">') end) - instr(value, '<p class="title">')-LENGTH('<p class="author">')-5),
    TRIM(
    SUBSTR(value, 
           instr(value, '<p class="author">') + LENGTH('<p class="author">'), 
           instr(value, '<p class="price">') - instr(value, '<p class="author">')-LENGTH('<p class="price">')-7))
           ) as TITLE,
   
    (case when value like ('%<p class="author">%') then
    TRIM(
    SUBSTR(value, 
           instr(value, '<p class="author">') + LENGTH('<p class="author">'), 
           instr(value, '<p class="price">') - instr(value, '<p class="author">')-LENGTH('<p class="price">')-7))
    else null end) as Author,
   
    cast(TRIM(SUBSTR(value, 
                     instr(value, '<p class="price">') + LENGTH('<p class="price">'), 
                     instr(value, ' ₽</p>') - instr(value, '<p class="price">')-LENGTH('<p class="price">'))) as numeric(*,2)) as Price
   
from data;

select 
 cast((case 
        when t.ID like '%<%' /*если в поле ID есть < */
          then SUBSTR(ID, 1, instr(ID, '<')-1) /*то в поле ID осталяем, то что до < */
        else ID /* иначе поле ID нормальное*/
       end)
      as int) /*меняем тип поля на int*/ as ID,

 CATEGORYS as "Категория",
 
 (case
   when TITLE like '%:%' /*если в поле TITLE есть : */
    then UPPER(SUBSTR(SUBSTR(TITLE, instr(TITLE, ':')+2), /*то в поле осталяем, то что после и первая буква большая : */
                      1, 1)) || SUBSTR(SUBSTR(TITLE, instr(TITLE, ':')+2), 2)
   else null /* иначе поле TITLE нормальное*/
  end) as "Жанр",
 
 (case
   when TITLE like '%:%' /*если в поле TITLE есть : */
    then SUBSTR(TITLE, 1, instr(TITLE, ':')-2) /*то в поле TITLE оставляем, то что до : */
   else TITLE /* иначе поле TITLE нормальное*/
  end) as "Название книги",
 
 (case
   when TITLE = AUTHOR  /*если поля Названия и Автор равны между собой */
    then null /*то автор пустое*/
   else
  (case 
    when AUTHOR like '%</p>%' /*если в поле Автор есть </p>*/
     then SUBSTR(AUTHOR, 1, instr(AUTHOR, '</p>') -1) /*то в поле Автор осталяем, то что до </p> */
    else AUTHOR end) /* иначе поле Автор нормальное*/
     end) as "Автор",
 
 (case /*предполагаю, что в книга не может стоит более 1000 рублей, скорее всего забыли (пропустили) поставить точку*/
   when LENGTH(PRICE)>4 then PRICE/100 /*если книга стоит более 10000 рублей, то её стоимость умньшить в 100 раз*/
   else PRICE /*иначе оставить как есть*/
  end) as "Цена книги"

from books;

