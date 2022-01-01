SELECT model,
	   range
FROM aircrafts
WHERE range between 1300 and 5800
order by range asc;