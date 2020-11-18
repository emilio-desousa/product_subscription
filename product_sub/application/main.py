from product_sub.infrastructure.dataset_builder import DatasetBuilder
from product_sub.domain.data_cleaning import NumImputer, CatImputer
from product_sub.domain.feature_creator import (
    CategoricalCreatorFromNumerical,
    CategoricalFeatureCreator,
)
from product_sub.domain.feature_encoder import OneHotEncoder, FrequencyEncoder
import product_sub.settings as stg

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline, make_union
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import classification_report

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.compose import make_column_selector as selector
from sklearn.compose import ColumnTransformer

import numpy as np
import pandas as pd


def main():
    print("bla")


if __name__ == "__main__":
    main()