from product_sub.infrastructure.dataset_builder import DatasetBuilder
from product_sub.domain.pipeline_creator import PipelineCreator
from product_sub.settings.utils import update_progress
import product_sub.settings as stg
from sklearn.ensemble import RandomForestClassifier
from imblearn.combine import SMOTEENN

# from sklearn.metrics import plot_confusion_matrix, classification_report

import pandas as pd
from os.path import join
import argparse


def main():
    PARSER = argparse.ArgumentParser(description="Prediction of subscription")

    PARSER.add_argument(
        "--filename_to_predict",
        "-fp",
        required=True,
        help="File to predict ( only csv supported for now )",
    )

    ARGS = PARSER.parse_args()

    SAVED_FILENAME = f"{ARGS.filename_to_predict}"
    update_progress(0)
    print("progress : Predict subscription")

    dataset_merged = DatasetBuilder(filename_bank=stg.FILENAME_BANK, filename_socio=stg.FILENAME_SOCIO_ECO).create_dataset()
    X_train = dataset_merged.drop(columns=stg.COL_RAW_SUBSCRIPTION)
    y_train = dataset_merged[stg.COL_RAW_SUBSCRIPTION].values

    update_progress(0.2)
    print("progress : Build Dataset")
    preprocessor_pipeline = PipelineCreator().preprocessor
    X_train_processed = preprocessor_pipeline.fit_transform(X_train)

    update_progress(0.3)
    print("progress : Deal with imbalenced classes")
    smote_enn = SMOTEENN(sampling_strategy=0.8, random_state=stg.RANDOM_STATE, n_jobs=-1)
    X_train, y_train = smote_enn.fit_resample(X_train_processed, y_train)

    update_progress(0.6)
    print("progress : Fit model")
    random_forest_classifier = RandomForestClassifier(**stg.RFC_PARAMS)
    random_forest_classifier.fit(X_train, y_train)

    update_progress(0.9)
    print("progress : Predict")
    X_test = DatasetBuilder(
        filename_bank=SAVED_FILENAME,
        filename_socio=stg.FILENAME_SOCIO_ECO_TEST,
        is_test=True,
    ).create_dataset()
    X_test_transformed = preprocessor_pipeline.transform(X_test)
    predictions = random_forest_classifier.predict(X_test_transformed)
    X_test["PREDICTED_SUBSCRIPTION"] = predictions
    X_test.to_csv(join(stg.PROCESSED_DATA_DIR, "predictions.csv"))
    print("Completed!")
    print("You can find the csv file with the predictions inside in data/processed/predictions.csv ! ")


if __name__ == "__main__":
    main()
