from scipy import spatial
import numpy as np
import csv
import pickle

data=[]
with open('airports.dat.csv', 'rb') as f:
	rdr=csv.reader(f)
	for row in rdr:
		data.append((float(row[6]), float(row[7])))
data=np.asarray(data)
# print(data)
# print(data)
tree=spatial.KDTree(data)

# print(tree.data)
(d, l)=tree.query([-5.82, 144.29])
print(tree.data[l])

with open('start_end.pickle', 'rb') as f:
	data=pickle.load(f)

row=data[0]
s_pos=(row[2], row[3])
print(s_pos)
(d, l)=tree.query(s_pos)
pos=tree.data[l]

select * from 
res=getRes(query, db)
