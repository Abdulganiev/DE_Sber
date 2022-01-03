select 
   cast(TRIM(REPLACE(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p>.+</'), '<[^<>]*>', ''), '</', '')) as int) as ID, /*приводим поле "ИД" в нужный формат*/
   
   /*Категория*/
   TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<h1>.+</h1>'), '<[^<>]*>', '')) as "Категория",
   
   (case /*Жанр*/
     when INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ':')>0 /*Если в поле "Название" если разделитель, то */
      then /*то переносим в "Жанр" вторую часть*/
           INITCAP(SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')),
                          INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ':')+2))
     when INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')), ':')>0 /*Если в поле "Автор" если разделитель, то */
      then /*то переносим в "Жанр" вторую часть*/
           INITCAP(SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')),
                          INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')), ':')+2))
    
     end) as "Жанр",
   
   (case /*Название книги*/
     when INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ':')>0 /*Если в поле "Название" есть разделитель, то */
      then SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), 1, /*то оставляем до разделителя */
                  INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ':')-1) 
     when INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')), ':')>0 /*Если в поле "Автор" есть разделитель, то */
      then SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')), 1, /*переносим из поля "Автор" до разделителя*/
                  INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<!*[^<>]*>', '')), ':')-1)
     when TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')) is null /*Если в поле "Автор" пустое, то */
      then SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), 1, /*то оставляем до первого инициала (имя)*/
                  REGEXP_INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value,  '<p class="title">.+</p>'), '<[^<>]*>', '')), ' [А-Я]\.')-1)
     else TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')) /*иначе нормальное поле*/
    end) as "Название книги",
    
   (case /*Автор*/ 
     when INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')), ':')>0 /*если в в поле "Автор" имеется разделитель, то*/
      then /*удалем всё*/ REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '.+', '')
              
     when TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')) is null /*проверка на пустое поле "Автор", то берем автор из названия*/
      then /*проверяем на мальчик или девочка и соответственно меняем окночания*/
       (case when 
        SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')),
                    REGEXP_INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ' [А-Я]\.')+1)
                like ('%а') /*если окончание фамилии на А, то это мальчик*/
             then REGEXP_REPLACE( /*тогда удаляем последнию букву А*/
        SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')),
                    REGEXP_INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ' [А-Я]\.')+1),
                      'а$', '')
            else /*иначе это девочка*/
        REGEXP_REPLACE( /*тогда удаляем последние две буквы ОЙ*/
        SUBSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')),
                    REGEXP_INSTR(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="title">.+</p>'), '<[^<>]*>', '')), ' [А-Я]\.')+1),
                      'ой$', 'а')    
            end)
     else TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="author">.+</p>'), '<[^<>]*>', '')) /* иначе поле "Автор" нормальное*/
      end) as "Автор книги",
    
    (case /*предполагаю, что в книга не может стоит более 1000 рублей, скорее всего забыли (пропустили) поставить точку*/
      when LENGTH(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="price">\d+(\.\d+)?'), '<[^<>]*>', '')))>4 /*если книга стоит более 10000 рублей, то*/
       then cast(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="price">\d+(\.\d+)?'), '<[^<>]*>', ''))as int)/100 /*её стоимость умньшить в 100 раз*/
      else cast(TRIM(REGEXP_REPLACE(REGEXP_SUBSTR(value, '<p class="price">\d+(\.\d+)?'), '<[^<>]*>', '')) as numeric(*,2)) /*иначе оставить как есть*/
    end) as "Цена книги"
   
from data

