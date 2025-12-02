#MetIoR model generator - generates model files as .pkl files.
#Runs on metior_masterlist and generates ten model pickle files - mod_dump[N].pkl (N - 1 through 10)

import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
import pickle
from joblib import Parallel,delayed
import joblib

f=open('metior_masterlist')
mlines=f.readlines()
f.close()
mlines=mlines[1:]

anno_list=[]
pred_vals_list_of_list=[]

for i in range(len(mlines)):
	anno=mlines[i].split()[5]
	if anno=='D':
		anno=1
	elif anno=='O':
		anno=0
	anno_list.append(anno)
	vals=mlines[i].split()[6:]
	vals_num=[]
	for j in vals:
		vals_num.append(float(j))
	pred_vals_list_of_list.append(vals_num)

X=pd.DataFrame(pred_vals_list_of_list)
y=pd.DataFrame(anno_list)

n_splits=10
skf=StratifiedKFold(n_splits=n_splits,shuffle=True,random_state=42)

n_estimators_optimal=200
max_depth_optimal=None
min_samples_split_optimal=2
bootstrap_optimal=False

foldnum=1
for train_index,test_index in skf.split(X,y):
	X_train,X_test=X.iloc[train_index],X.iloc[test_index]
	y_train,y_test=y.iloc[train_index],y.iloc[test_index]
	rfc=RandomForestClassifier(n_estimators=n_estimators_optimal,max_depth=max_depth_optimal,min_samples_split=min_samples_split_optimal,bootstrap=bootstrap_optimal)
	rfc.fit(X_train,y_train)
	joblib.dump(rfc,'mod_dump'+str(foldnum)+'.pkl')
	foldnum+=1
