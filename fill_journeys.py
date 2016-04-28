from haversine import haversine
from flight import getConn, getRes
from location_search import getAirport,buildTree

if __name__=="__main__":
	db = getConn();
	query='delete from journeys where 1;'
	csr=db.cursor()
	csr.execute(query)
	query='select fid, min(rec_time) as s_time, max(rec_time) as e_time from flight group by fid order by fid limit 1000;'
	csr.execute(query)
	r=csr.fetchone()
	tree=buildTree()
	values=[]
	ctr=0
	while r is not None:
		ctr+=1
		try:
			fid= r[0]
			dtime=int((r[2]-r[1]).total_seconds())
			# print(dtime)
			query=('select fid,lat,lon from flight where fid="{0}" AND rec_time="{1}"').format(r[0], r[1])
			res1=getRes(query, db)[0]
			spos= (float(res1[1]), float(res1[2]));

			query=('select fid,lat,lon from flight where fid="{0}" AND rec_time="{1}"').format(r[0], r[2])
			res1=getRes(query, db)[0]
			epos= (float(res1[1]), float(res1[2]));
			
			s_air=getAirport(spos, tree, db)
			e_air=getAirport(epos, tree, db)
			
			dist = haversine(spos,epos)
			print(ctr,fid,dtime,spos,epos,s_air,e_air,dist)
			# query = ('insert into journeys values ("{0}",{1},{2},{3},{4})').format(fid,s_air,e_air,dtime,dist)
			query = """insert into journeys values (%s,%s,%s,%s,%s)"""
			values.append((fid,s_air,e_air,dtime,dist))
		except IndexError:
			print('index error')
		r=csr.fetchone()
	csr2=db.cursor()
	csr2.executemany(query, values)
	db.commit()