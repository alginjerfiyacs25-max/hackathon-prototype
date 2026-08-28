from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
FEATURES=['rainfall','forecast_rainfall','soil_saturation','river_level','slope','upstream_flow','river_distance','elevation']
_model=None; _metrics={}

def train_model():
    rng=np.random.default_rng(7); X=rng.uniform(0,100,(240,8)); X[:,6]=rng.uniform(.3,8,240); X[:,7]=rng.uniform(700,1500,240)
    y=((X[:,0]*.3+X[:,1]*.15+X[:,2]*.2+X[:,3]*.2+X[:,5]*.15)>52).astype(int)
    split=190; global _model,_metrics
    lr=LogisticRegression(max_iter=1000).fit(X[:split],y[:split]); rf=RandomForestClassifier(n_estimators=80,random_state=7).fit(X[:split],y[:split]); _model=rf
    _metrics={'dataset':'Simulated training data','logistic_regression':_score(lr,X[split:],y[split:]),'random_forest':_score(rf,X[split:],y[split:]),'feature_importance':dict(sorted(zip(FEATURES,rf.feature_importances_),key=lambda x:x[1],reverse=True))}
    return _metrics

def _score(model,X,y):
    p=model.predict(X); return {k:round(v,3) for k,v in {'accuracy':accuracy_score(y,p),'precision':precision_score(y,p,zero_division=0),'recall':recall_score(y,p,zero_division=0),'f1':f1_score(y,p,zero_division=0)}.items()}
def get_metrics(): return _metrics or train_model()
def get_model_metrics(): return get_metrics()
def predict_risk(values: dict):
    get_metrics(); arr=np.array([[values[k] for k in FEATURES]]); probability=float(_model.predict_proba(arr)[0,1]); return {'risk_probability':round(probability*100,1),'risk_level':'CRITICAL' if probability>=.75 else 'HIGH' if probability>=.5 else 'LOW','model':'Random Forest','is_simulated':True}
