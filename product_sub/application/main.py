from product_sub.infrastructure.dataset_builder import DatasetBuilder
from product_sub.domain.pipeline_creator import PipelineCreator
import product_sub.settings as stg

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN


def main():
    dataset_merged = DatasetBuilder(
        filename_bank=stg.FILENAME_BANK, filename_socio=stg.FILENAME_SOCIO_ECO
    ).create_dataset()
    X = dataset_merged.drop(columns=stg.COL_RAW_SUBSCRIPTION)
    y = dataset_merged[stg.COL_RAW_SUBSCRIPTION].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=stg.RANDOM_STATE
    )
    custom_pipeline_accessor = PipelineCreator()
    preprocessor = custom_pipeline_accessor.preprocessor
    X_train_processed = preprocessor.fit_transform(X_train)
    smote_enn = SMOTEENN(sampling_strategy=0.8, random_state=stg.RANDOM_STATE)
    X_train, y_train = smote_enn.fit_resample(X_train_processed, y_train)
    gradient_classifier = GradientBoostingClassifier()
    gradient_classifier.fit(X_train, y_train)

    X_test = preprocessor.transform(X_test)
    gradient_classifier.predict(X_test)


if __name__ == "__main__":
    main()