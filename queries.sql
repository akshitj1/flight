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
ALTER TABLE flight ADD INDEX fidx (fid);
ALTER TABLE flight ADD INDEX rectimeidx (rec_time);

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


CREATE TABLE airports
(
	id int,
	name varchar(255),
	city varchar(100),
	country varchar(100),
	lat decimal(11,8),
	lon decimal(11,8)
);

LOAD DATA LOCAL INFILE '~/Desktop/sohban/flight/airports.dat.csv' INTO TABLE airports
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'  
(@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8,@col9,@col10,@col11,@col12) set id=@col1, name=@col2, city=@col3, country=@col4, lat=@col7, lon=@col8;

CREATE TABLE journeys
(
	fid varchar(12),
	src int,
	dest int,
	ttime int,
	dist int
);

select * from (select fid,floor(dist*1000/ttime) as speed from journeys)as t where t.speed=max(t.speed);

#flights bw same airports
select * from (select src, dest,count(*) as num from journeys group by src, dest) as t where t.src!=t.dest order by t.num desc limit 20;
select fid, ttime from journeys where src=8890 and dest=3576;