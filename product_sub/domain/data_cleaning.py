import product_sub.settings as stg
from product_sub.infrastructure.dataset_builder import DatasetBuilder
from sklearn.base import BaseEstimator, TransformerMixin


class CatImputer(BaseEstimator, TransformerMixin):
    """Impute nan values from categorical features

    Parameters
    ----------
    BaseEstimator
    TransformerMixin
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """Fill nan values thnaks to differents values from other features
        Ex: if JOB_TYPE = Manager and Education is missing => Fill Education with "Tertiaire"
                because it is the mode of Education when job is Manager

        Parameters
        ----------
        X : pandas.DataFrame
            DataFrame to transform ( with only categorical features )
        y : np.Array, optional
            targets, by default None

        Returns
        -------
        pandas.DataFrame
            Transformed Dataframe ( with no more nan values is categorical featurees)
        """
        df = X.copy()
        for feature in df:
            if not feature == stg.COL_RAW_RESULT_LAST_CAMPAIGN:
                df = df.assign(
                    **{feature: lambda df: df[feature].cat.add_categories("Autre")}
                )
            if feature == stg.COL_RAW_JOB:
                df = self._deal_with_job_type(df)
            if feature == stg.COL_RAW_EDUCATION:
                df = self._deal_with_education_nan(df)
            if feature == stg.COL_RAW_RESULT_LAST_CAMPAIGN:
                df = df.assign(
                    **{
                        feature: lambda df: df[feature].cat.add_categories(
                            "premier_contact"
                        )
                    }
                )
                df = df.assign(
                    **{feature: lambda df: df[feature].fillna("premier_contact")}
                )
            if feature == stg.COL_RAW_STATUS:
                df = df.assign(**{feature: lambda df: df[feature].fillna("Marie")})

        df = df.fillna("Autre")
        return df

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


if __name__ == "__main__":
    from product_sub.domain.feature_selector import FeatureSelector
    import numpy as np
    from sklearn.pipeline import (
        FeatureUnion,
        Pipeline,
        make_pipeline,
        make_union,
    )

    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import make_column_selector as selector
    from sklearn.compose import ColumnTransformer
    from sklearn.model_selection import train_test_split

    RANDOM_STATE = 42

    dataset_merged = DatasetBuilder(
        filename_bank="data.csv", filename_socio="socio_eco.csv"
    ).create_dataset()
    X = dataset_merged.drop(columns=stg.COL_RAW_SUBSCRIPTION)
    y = dataset_merged[stg.COL_RAW_SUBSCRIPTION].values
    cat_imputer = CatImputer(["JOB_TYPE", "EDUCATION"])
    categorical_transformer = Pipeline(
        steps=[("cat_imputer", cat_imputer), ("encoder", OneHotEncoder())]
    )
    numeric_transformer = Pipeline(
        steps=[("num_imputer", NumImputer()), ("scaler", StandardScaler())]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, selector(dtype_exclude="category")),
            ("cat", categorical_transformer, selector(dtype_include="category")),
        ]
    )
    clf = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression()),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    x_test, y = clf.fit(X_train, y_train)
