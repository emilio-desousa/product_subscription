import product_sub.settings as stg
from product_sub.infrastructure.dataset_builder import DatasetBuilder
from sklearn.base import BaseEstimator, TransformerMixin
from product_sub.domain.feature_encoder import FrequencyEncoder


class CategoricalCreatorFromNumerical(BaseEstimator, TransformerMixin):
    """Create categoricals columns from numerical

    Parameters
    ----------
    BaseEstimator : sklearn Object
        BaseEstimator
    TransformerMixin : sklearn Object
        TransformerMixin
    """

    def __init__(self, array_with_dicts_with_bounds):
        """Transformer initialization

        Parameters
        ----------
        array_with_dicts_with_bounds : array
            Array with dicts inside corresponding to the parameters to create new columns from numerical
            dict inside:
            {
                "inf": 4,  =>  lower bound to compare to create columns
                "sup": 8, => upper bound
                "column_source": COL_RAW_NB_CONTACT_LAST_CAMPAIGN, => column source that we want to transform
                "column_dist": "is_first_campaign", => column to create
            },
        """
        self.array_with_dicts_with_bounds = array_with_dicts_with_bounds

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = self._create_cat_columns_from_dict(X)
        return X

    def _create_col(self, df, inf, sup, column_source, column_dist):
        df[column_dist] = 0
        if inf == None:
            df.loc[(df[column_source] == sup), column_dist] = 1
        elif sup == None:
            df.loc[(df[column_source] > inf), column_dist] = 1
        else:
            df.loc[
                (df[column_source] > inf) & (df[column_source] < sup), column_dist
            ] = 1

    def _create_cat_columns_from_dict(self, df):
        df_to_create_cols = df.copy()
        for dict_with_bounds in self.array_with_dicts_with_bounds:
            self._create_col(df_to_create_cols, **dict_with_bounds)
        return df_to_create_cols


class CategoricalFeatureCreator(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X["is_first_campaign"] = 0
        X.loc[
            (X[stg.COL_RAW_RESULT_LAST_CAMPAIGN] == "premier_contact"),
            "is_first_campaign",
        ] = 1
        print(X.isna().sum())
        return X


if __name__ == "__main__":
    from sklearn.pipeline import Pipeline
    from product_sub.domain.data_cleaning import NumImputer, CatImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
    from sklearn.compose import make_column_selector as selector, ColumnTransformer

    numeric_transformer = Pipeline(
        steps=[
            ("num_imputer", NumImputer()),
            (
                "create_categorical",
                CategoricalCreatorFromNumerical(stg.DICT_TO_CREATE_COLS),
            ),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("cat_imputer", CatImputer()),
            ("cat_creator", CategoricalFeatureCreator()),
            (
                "freq_encoder",
                FrequencyEncoder([stg.COL_RAW_CONTACT, stg.COL_RAW_EDUCATION]),
            ),
            ("encoder", OneHotEncoder()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, selector(dtype_exclude="category")),
            ("cat", categorical_transformer, selector(dtype_include="category")),
        ]
    )
    data = DatasetBuilder("data.csv", "socio_eco.csv").create_dataset()
    X_cat = data.select_dtypes(include="category")
    X_num = data.select_dtypes(exclude="category")
    test = categorical_transformer.fit_transform(X_cat)
    test2 = numeric_transformer.fit_transform(X_num)
    test3 = preprocessor.fit_transform(data)
    # pipe = Pipeline(steps=[("transf", creator)])
    # test = preprocessor.fit(data)