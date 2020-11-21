from product_sub.domain.data_cleaning import CatImputer
from product_sub.domain.feature_creator import (
    CategoricalCreatorFromNumerical,
    CategoricalFeatureCreator,
)
import product_sub.settings as stg

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.compose import make_column_selector as selector, ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

from product_sub.domain.feature_encoder import (
    OneHotEncoder,
    FrequencyEncoder,
    LabelEncoding,
)
from sklearn.impute import SimpleImputer


class PipelineCreator:
    def __init__(self):
        pass

    @property
    def numerical_transformer(self):
        return Pipeline(
            steps=[
                (
                    "create_categorical",
                    CategoricalCreatorFromNumerical(stg.DICT_CONTINUOUS_TO_CATEGORICAL),
                ),
                ("num_imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler()),
            ]
        )

    @property
    def categorical_transformer(self):
        return Pipeline(
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

    @property
    def preprocessor(self):
        return ColumnTransformer(
            transformers=[
                ("num", self.numerical_transformer, selector(dtype_exclude="category")),
                (
                    "cat",
                    self.categorical_transformer,
                    selector(dtype_include="category"),
                ),
            ]
        )


if __name__ == "__main__":
    PipelineCreator().preprocessor