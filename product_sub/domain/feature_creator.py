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
        X = self._create_val_from_dict(X)
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
        return column_source

    def _create_cat_columns_from_dict(self, df):
        df_to_create_cols = df.copy()
        source_cols_to_drop = []
        for dict_with_bounds in self.array_with_dicts_with_bounds:
            col_to_drop = self._create_col(df_to_create_cols, **dict_with_bounds)
            source_cols_to_drop.append(col_to_drop)
        cols_to_drop = list(set(source_cols_to_drop))
        df_to_create_cols = df_to_create_cols.drop(columns=cols_to_drop)
        return df_to_create_cols

    def _create_val(self, df, inf, sup, column_source, val):
        if inf == None:
            df[stg.COL_IS_FIRST_CAMPAIGN] = 0
            df.loc[(df[column_source] == sup), column_source] = val
            df.loc[(df[column_source] == sup), stg.COL_IS_FIRST_CAMPAIGN] = 1
        elif sup == None:
            df.loc[(df[column_source] > inf), column_source] = val
        else:
            df.loc[
                (df[column_source] > inf) & (df[column_source] < sup), column_source
            ] = val
        return column_source

    def _create_val_from_dict(self, df):
        df_to_create_cols = df.copy()
        source_cols_to_drop = []
        for dict_with_bounds in self.array_with_dicts_with_bounds:
            col_to_drop = self._create_val(df_to_create_cols, **dict_with_bounds)
            source_cols_to_drop.append(col_to_drop)
        cols_to_drop = list(set(source_cols_to_drop))
        # df_to_create_cols = df_to_create_cols.drop(columns=cols_to_drop)
        return df_to_create_cols


class CategoricalFeatureCreator(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X["is_last_campaign_success"] = 0
        X["is_last_campaign_fail"] = 0
        X.loc[
            (X[stg.COL_RAW_RESULT_LAST_CAMPAIGN] == "Succes"),
            "is_last_campaign_success",
        ] = 1
        X.loc[
            (X[stg.COL_RAW_RESULT_LAST_CAMPAIGN] == "Echec"),
            "is_last_campaign_fail",
        ] = 1
        X = X.drop(columns=stg.COL_RAW_RESULT_LAST_CAMPAIGN)
        return X


if __name__ == "__main__":
    from sklearn.pipeline import Pipeline
    from product_sub.domain.data_cleaning import NumImputer, CatImputer
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.compose import make_column_selector as selector, ColumnTransformer
    from product_sub.domain.feature_encoder import OneHotEncoder

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
                FrequencyEncoder(stg.COLS_TO_FREQ_ENCODE),
            ),
            ("one_hot_encoder", OneHotEncoder([stg.COL_RAW_JOB])),
        ]
    )
    # preprocessor.transformers[1][1].steps[3][1].categories_
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