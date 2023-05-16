import joblib

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest
from azureml.core import Workspace, Model


dataset = pd.read_csv('Pat_Cain_Data.csv', parse_dates=[0], index_col=0)

# Create model pipeline & train
scaler = StandardScaler(with_mean=True, with_std=True)
model = IForest(contamination=float(0.5),
                n_estimators=100,
                max_features = 2/10,
                random_state=47)

model_pipeline = Pipeline([
    ('scaler', scaler),
    ('iforest', model)
])

model_pipeline.fit(dataset)

# Package model artifact
model_artifact = {
    'model': model_pipeline,
    'features': dataset.columns,
    'threshold': 0.85
}

with open('model.pkl', 'wb') as f:
    joblib.dump(model_artifact, f)
