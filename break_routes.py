from flight import getRes, getConn
from haversine import haversine

def breakPath(fid, row, db):
	br_time=row[0]
	new_fid=fid+chr(ord('a')+path_ctr)
	qry="update flight set fid='{0}' where fid='{1}' and rec_time<'{2}'".format(new_fid, fid, br_time);
	print('executing query: '+qry)
	getRes(qry, db)


db=getConn()
thresh=20*60
threshSpeed=0.05
# fid='AAL1078'
qry='select fid from journeys limit 1000;'
res=getRes(qry, db)
fids=['AAL1366']
for fid in fids:
	try:
		print('checking for fid: '+fid)
		qry="select * from flight where fid='{0}' order by rec_time asc;".format(fid)
		res=getRes(qry, db)
		path_ctr=0
		for i in range(1, len(res)):
			dtime=(res[i][0]-res[i-1][0]).total_seconds();
			ddist=haversine((res[i][4], res[i][5]), (res[i-1][4], res[i-1][5]))
			speed=ddist/dtime
			if(dtime>thresh and speed<threshSpeed):
				print(ddist/dtime)
				breakPath(fid, res[i], db)
				path_ctr+=1

		if(path_ctr>0):
			i=len(res)-1
			breakPath(fid, res[i], db)
		# db.commit()
	except ZeroDivisionError:
		print('ZeroDivisionError')