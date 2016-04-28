from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from flight import getRes, getConn
import matplotlib.lines as mlines
import sys

def addRoute(fid, clr, db, m):
	query=("select lat, lon from flight where fid='{0}' order by rec_time;").format(fid)	
	res=getRes(query, db)
	# print(res)
	for i in range(0, len(res)-1):
		a=[float(x) for x in res[i]]
		b=[float(x) for x in res[i+1]]
		# print(i)
		m.drawgreatcircle(a[1],a[0],b[1],b[0],linewidth=1,color=clr, label=fid)
	print('plotted route of '+fid+' with color '+clr)

def getFidsBwStations(src, dest, db):
	qry=("select fid, ttime from journeys where src={0} and dest={1} order by ttime asc;").format(src, dest)
	res=getRes(qry, db)
	fids= [x[0] for x in res]
	ttimes= [x[1] for x in res]
	
	print(fids)
	return fids, ttimes
if __name__=="__main__":
	db=getConn()
	m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
	            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
	argv=sys.argv
	fids=[]
	if(argv[1]=='srcdest'):
		fids, ttimes =getFidsBwStations(int(argv[2]), int(argv[3]), db)
	elif (argv[1]=='fids'):
		for i in range(2, len(argv)):
			fids.append(argv[i])
	else:
		print('invalid arguments')
		exit()
	clrs=['b', 'g', 'r', 'c', 'm', 'y', 'k'];
	# print(res)
	handles=[]
	for i in range(0, len(fids)):
		addRoute(fids[i], clrs[i%len(clrs)], db, m);
		# handles.append(mlines.Line2D([], [], color=clrs[i%len(clrs)], label=fids[i]+' '+str(ttimes[i])))
		# break
	m.drawcoastlines()
	m.fillcontinents()
	# plt.legend([mlines.Line2D([], [], color='green', label='line1')])
	plt.show()

