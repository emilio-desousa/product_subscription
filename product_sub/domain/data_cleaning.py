import product_sub.settings as stg
from product_sub.infrastructure.dataset_builder import DatasetBuilder
from sklearn.base import BaseEstimator, TransformerMixin
from product_sub.domain.feature_selector import FeatureSelector
import numpy as np


class CatImputer(BaseEstimator, TransformerMixin):
    def __init__(self, feature_names):
        self._feature_names = feature_names

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for feature in self._feature_names:
            if feature == stg.COL_RAW_JOB:
                X = self._deal_with_job_type(X)
            if feature == stg.COL_RAW_EDUCATION:
                X = self._deal_with_education_nan(X)
            else:
                X = X.fillna("Autre")
        return X

    def _fillna_edu(self, df, filter_val, val):
        df2 = df.copy()
        mask = df[stg.COL_RAW_JOB] == filter_val
        df2.loc[mask, stg.COL_RAW_EDUCATION] = df.loc[
            mask, stg.COL_RAW_EDUCATION
        ].fillna(val)
        return df2

    def _fillna_from_job_or_edu(self, df, filter_val, val, is_job):
        df2 = df.copy()
        if is_job:
            mask = df[stg.COL_RAW_EDUCATION] == filter_val
            df2.loc[mask, stg.COL_RAW_JOB] = df.loc[mask, stg.COL_RAW_JOB].fillna(val)
        else:
            mask = df[stg.COL_RAW_JOB] == filter_val
            df2.loc[mask, stg.COL_RAW_EDUCATION] = df.loc[
                mask, stg.COL_RAW_EDUCATION
            ].fillna(val)
        return df2

    def _deal_with_job_type(self, X):
        for couple in stg.ARRAY_WITH_COUPLE_TO_FILL_JOB:
            X = self._fillna_from_job_or_edu(X, couple[0], couple[1], True)
        X[stg.COL_RAW_JOB] = X[stg.COL_RAW_JOB].fillna("Autre")
        return X

    def _deal_with_education_nan(self, X):
        for couple_job_edu in stg.ARRAY_WITH_COUPLE_TO_FILL_EDU:
            X = self._fillna_from_job_or_edu(
                X, couple_job_edu[0], couple_job_edu[1], False
            )
        X[stg.COL_RAW_EDUCATION] = X[stg.COL_RAW_EDUCATION].fillna("Autre")
        return X


class NumImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.fillna(X.mean())
        return X.values


if __name__ == "__main__":

    def check_missing_with_two_col(df, feat1, feat2):
        jobs = list(df[feat1].unique())
        edu = list(df[feat2].unique())
        dataframes = []
        for e in edu:
            dfe = df[df[feat2] == e][feat1]
            print(f"{feat1} {e} :{dfe.isna().sum()}")
        print(f"{df[feat1].value_counts()}")
        print(f"Total missing : {df[feat1].isna().sum()}")

    def get_missing_percent(df_tmp):
        sum_na = df_tmp.isna().sum()
        size = df_tmp.shape[0]
        percents_missing = sum_na / size * 100
        sorted_percents = percents_missing.sort_values(ascending=False)
        print(
            f"###\n###\n### Pourcentage de valeurs manquantes par colonnes \n###\n###\n###\n{sorted_percents}"
        )

    dataset_merged = DatasetBuilder(
        filename_bank="data.csv", filename_socio="socio_eco.csv"
    ).merge()
    X = FeatureSelector(object).fit(dataset_merged).transform(dataset_merged)
    nan = (
        CatImputer(feature_names=["JOB_TYPE", "EDUCATION"])
        .fit(dataset_merged)
        .transform(X)
    )
