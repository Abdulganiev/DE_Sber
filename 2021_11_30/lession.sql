select * from dataSource;

select  
  FIRST_NAME||' '||LAST_NAME as wer,
  regexp_substr(FIRST_NAME||' '||LAST_NAME, '[a-zA-Z]+') as FIRST_NAME,
  regexp_substr(FIRST_NAME||' '||LAST_NAME, '[a-zA-Z]+( )?$') as LAST_NAME,
  regexp_substr(EMAIL, '\w+@\w+(\.[a-z]+)+', 1, 1, 'i') as mail2,
  regexp_substr(EMAIL, '[+]?\d[. -]?\d{2,3}[. -]?\d{2,3}[- .]?.]?\d{2,3}[- .]?\d{2,3}') as phone,
  REGEXP_REPLACE(EMAIL, '\w+@\w+(\.[a-z]+)+( )?', '') as ww,
  EMAIL,
GENDER,  
INSTR(GENDER, 'F')
from dataSource;

create view tmp as
select  
  FIRST_NAME||' '||LAST_NAME as wer,
  regexp_substr(FIRST_NAME||' '||LAST_NAME, '[a-zA-Z]+') as FIRST_NAME,
  regexp_substr(FIRST_NAME||' '||LAST_NAME, '[a-zA-Z]+( )?$') as LAST_NAME,
  regexp_substr(EMAIL, '\w+@\w+(\.[a-z]+)+', 1, 1, 'i') as mail2,
  regexp_substr(EMAIL, '[+]?\d[. -]?\d{2,3}[. -]?\d{2,3}[- .]?.]?\d{2,3}[- .]?\d{2,3}') as phone,
  REGEXP_REPLACE(EMAIL, '\w+@\w+(\.[a-z]+)+( )?', '') as phone2,
  EMAIL,
GENDER,  
INSTR(GENDER, 'F') as G
from dataSource;

select phone,
REGEXP_REPLACE(replace(replace(phone, ' ', ''), '-', ''), '^8', '+7') as phone_norm,
REGEXP_REPLACE(REGEXP_REPLACE(phone, '\W', ''), '^[78]', '+7') as phone_norm2,
REPLACE(REGEXP_REPLACE(phone, '\W', ''), '7%', '+7') as phone_norm3
from tmp

