from scipy import spatial
import numpy as np
import csv
import pickle
from flight import getConn, getRes


def buildTree():
	data=[]
	with open('airports.dat.csv', 'rb') as f:
		rdr=csv.reader(f)
		for row in rdr:
			data.append((float(row[6]), float(row[7])))
	data=np.asarray(data)
	# print(data)
	# print(data)
	tree=spatial.KDTree(data)
	return tree
def getNrPoint(p, tree):
	# print(tree.data)
	(d, l)=tree.query(p)
	return tree.data[l]

def getAirport(p, tree, db):
	pos=getNrPoint(p, tree)
	query=('select * from airports where lat={0} and lon={1}').format(pos[0], pos[1])
	res=getRes(query, db)[0]
	return int(res[0])

def populateAirports():
	db=getConn()
	tree=buildTree()
	with open('start_end.pickle', 'rb') as f:
		data=pickle.load(f)
	mData=[]
	tData=[]
	for row in data:
		s_pos=(row[2], row[3])
		e_pos=(row[4], row[5])
		s_air=getAirport(s_pos, tree, db)
		e_air=getAirport(e_pos, tree, db)
		tData.append((s_air, e_air, row[1]))
		mData.append((row[0], s_air, e_air, row[1]))
	tData.sort()
	for row in tData:
		print row

if __name__=="__main__":
	populateAirports();