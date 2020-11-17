import product_sub.settings as stg
from product_sub.infrastructure.dataset_builder import DatasetBuilder
from sklearn.base import BaseEstimator, TransformerMixin


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
                **{feature: lambda df: df[feature].map(freq)}
            )
            # self._change_col_to_freq(X, **dict_frequency)
        print(df_with_freq)
        return df_with_freq

    def _change_col_to_freq(self, df, freq, feature):
        df_with_freq = df.assign(**{feature: lambda df: df[feature].map(freq)})
