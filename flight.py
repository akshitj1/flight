import csv
import MySQLdb
import time
import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pickle

def getRes(query, db):
	c=db.cursor()
	c.execute(query)
	return c.fetchall();

def getConn():
	db=MySQLdb.connect("localhost","root","","testdb" )
	return db

if __name__=="__main__":
	db = getConn();
	query='select fid, min(rec_time) as s_time, max(rec_time) as e_time from flight group by fid limit 100;'
	res=getRes(query, db)

	m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
	            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

	data=[]

	for r in res:
		fid= r[0]
		dtime=int((r[2]-r[1]).total_seconds())
		# print(dtime)
		query=('select fid,lat,lon from flight where fid="{0}" AND rec_time="{1}"').format(r[0], r[1])
		res1=getRes(query, db)[0]
		spos= (float(res1[1]), float(res1[2]));

		query=('select fid,lat,lon from flight where fid="{0}" AND rec_time="{1}"').format(r[0], r[2])
		res1=getRes(query, db)[0]
		epos= (float(res1[1]), float(res1[2]));
		
		data.append((fid,dtime, spos[0], spos[1], epos[0], epos[1]))
		# m.drawgreatcircle(spos[1],spos[0],epos[1],epos[0],linewidth=1,color='b')
		# break;

	with open('start_end.pickle', 'wb') as f:
		pickle.dump(data, f)
	# m.drawcoastlines()
	# m.fillcontinents()
	# plt.title('Great Circle from New York to London')
	# plt.show()