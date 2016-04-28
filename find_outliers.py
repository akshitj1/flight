import pickle
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import csv
from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from scipy import stats

data=[]
with open('newdata.csv', 'rb') as f:
	rdr=csv.reader(f)
	for row in rdr:
		data.append([int(row[1]), int(row[2])])
data=np.array(data)
# print(data)
outliers_fraction = 0.05
# est=svm.OneClassSVM(nu=0.95 * outliers_fraction + 0.05,kernel="rbf", gamma=0.1)
est=EllipticEnvelope(contamination=.1)
# est=KMeans(n_clusters=3)
est.fit(data)
# labels=est.labels_
y_pred=est.decision_function(data).ravel()
threshold = stats.scoreatpercentile(y_pred,
                                            100 * outliers_fraction)

labels=[ (2 if y>threshold  else 1) for y in y_pred];
# labels=est.labels_
print(labels)
plt.scatter(data[:,0], data[:,1], c=labels, lw=0)
plt.show()