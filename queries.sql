delete from flight where 1;

CREATE TABLE flight
(
	rec_time datetime,
	fid varchar(12),
	speed int,
	alt varchar(10),
	lat decimal(8,4),
	lon decimal(8,4)
);

LOAD DATA LOCAL INFILE '~/Desktop/fdata.csv' INTO TABLE flight
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'  
(@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8,@col9,@col10) set rec_time=STR_TO_DATE(@col1, '%c/%e/%Y %H:%i'),fid=@col5 , speed=@col6, alt=@col7, lat=@col8, lon=@col9;

select * from flight limit 5;

select * from flight order by fid limit 12;

select distinct fid from flight order by fid limit 10;

select * from flight where fid='AAH4404' order by rec_time;

select t1.fid, t1.entries
from(
	select fid, count(*) as entries from flight group by fid
) as t1
where t1.entries>10 limit 10;

select fid, min(rec_time) as s_time, max(rec_time) as e_time from flight group by fid limit 10;