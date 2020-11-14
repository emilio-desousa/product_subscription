from product_sub.infrastructure.dataset_builder import DatasetBuilder
from product_sub.domain.data_cleaning import NumImputer, CatImputer
from product_sub.domain.feature_selector import FeatureSelector
import product_sub.settings as stg

from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline, make_union
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

dataset_merged = DatasetBuilder(
    filename_bank="data.csv", filename_socio="socio_eco.csv"
).merge()

dataset_merged = dataset_merged.drop(columns=stg.COL_RAW_DATE)
X = dataset_merged.drop(columns=stg.COL_RAW_SUBSCRIPTION)
y = dataset_merged[stg.COL_RAW_SUBSCRIPTION].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

num_pipeline = make_pipeline(FeatureSelector(np.number), NumImputer(), StandardScaler())
cat_pipeline = make_pipeline(
    FeatureSelector(object),
    CatImputer([stg.COL_RAW_JOB, stg.COL_RAW_EDUCATION]),
    OneHotEncoder(),
)
X_train.shape
data_pipeline = make_union(num_pipeline, cat_pipeline)
full_pipeline = make_pipeline(data_pipeline, LogisticRegression(max_iter=500))
full_pipeline.fit(X_train, y_train)
y_pred = full_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\naccuracy : ", accuracy)
