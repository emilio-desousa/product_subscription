import product_sub.settings as stg
from product_sub.infrastructure.dataset_builder import DatasetBuilder
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, feature_names):
        self.feature_names = feature_names

    def fit(self, X, y=None):

        frequency_array = []
        for feature in self.feature_names:
            frequency = X.groupby(feature).size() / len(X)
            frequency_array.append({"freq": frequency, "feature": feature})
        self.frequency_array = frequency_array
        return self

    def transform(self, X, y=None):
        df_with_freq = X.copy()
        for dict_frequency in self.frequency_array:
            freq, feature = dict_frequency.values()
            df_with_freq = df_with_freq.assign(
                **{feature: lambda df: df[feature].map(freq).astype("float64")}
            )
            # self._change_col_to_freq(X, **dict_frequency)
        return df_with_freq

    def _change_col_to_freq(self, df, freq, feature):
        df_with_freq = df.assign(**{feature: lambda df: df[feature].map(freq)})


class OneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, feature_names):
        self.feature_names = feature_names

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df_to_onehot = X.copy()
        for feature in self.feature_names:
            one_hot_df = pd.get_dummies(df_to_onehot[feature])
            df_to_onehot = df_to_onehot.drop(columns=feature)
            df_to_onehot = df_to_onehot.join(one_hot_df)
        # print(df_to_onehot)
        return df_to_onehot
