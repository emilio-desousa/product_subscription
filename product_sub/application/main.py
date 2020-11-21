from product_sub.infrastructure.dataset_builder import DatasetBuilder
from product_sub.domain.pipeline_creator import PipelineCreator
import product_sub.settings as stg
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from imblearn.combine import SMOTEENN
from sklearn.metrics import plot_confusion_matrix, classification_report

import pandas as pd
from os.path import join
import argparse
import time, sys


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

    dataset_merged = DatasetBuilder(
        filename_bank=stg.FILENAME_BANK_TRAIN, filename_socio=stg.FILENAME_SOCIO_ECO
    ).create_dataset()
    X_train = dataset_merged.drop(columns=stg.COL_RAW_SUBSCRIPTION)
    y_train = dataset_merged[stg.COL_RAW_SUBSCRIPTION].values

    update_progress(0.2)
    print("progress : Build Dataset")
    preprocessor_pipeline = PipelineCreator().preprocessor
    X_train_processed = preprocessor_pipeline.fit_transform(X_train)

    update_progress(0.3)
    print("progress : Deal with imbalenced classes")
    smote_enn = SMOTEENN(
        sampling_strategy=0.8, random_state=stg.RANDOM_STATE, n_jobs=-1
    )
    X_train, y_train = smote_enn.fit_resample(X_train_processed, y_train)

    update_progress(0.6)
    print("progress : Fit model")
    gradient_classifier = GradientBoostingClassifier()
    gradient_classifier.fit(X_train, y_train)

    update_progress(0.9)
    print("progress : Predict")
    X_test = DatasetBuilder(
        filename_bank=SAVED_FILENAME,
        filename_socio=stg.FILENAME_SOCIO_ECO,
        is_test=True,
    ).create_dataset()
    X_test = preprocessor_pipeline.transform(X_test)
    gradient_classifier.predict(X_test)
    print("Completed!")


def update_progress(progress):
    barLength = 10
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = "\rPercent: [{0}] {1}% {2}".format(
        "#" * block + "-" * (barLength - block), progress * 100, status
    )
    sys.stdout.write(text)
    sys.stdout.flush()


def main3():
    dataset_merged = DatasetBuilder(
        filename_bank=stg.FILENAME_BANK_TRAIN, filename_socio=stg.FILENAME_SOCIO_ECO
    ).create_dataset()
    X_train = dataset_merged.drop(columns=stg.COL_RAW_SUBSCRIPTION)
    y_train = dataset_merged[stg.COL_RAW_SUBSCRIPTION].values
    X_test = DatasetBuilder(
        filename_bank="data_test.csv",
        filename_socio=stg.FILENAME_SOCIO_ECO,
        is_test=True,
    ).create_dataset()
    X_test_with_target = pd.read_csv(
        join(stg.RAW_DATA_DIR, "data_test_target.csv"), sep=stg.SEP
    )
    X_test_with_target[stg.COL_RAW_SUBSCRIPTION] = X_test_with_target[
        stg.COL_RAW_SUBSCRIPTION
    ].replace(stg.BOOLEAN_ENCODING)
    y_test = X_test_with_target[stg.COL_RAW_SUBSCRIPTION].values
    custom_pipeline_accessor = PipelineCreator()
    preprocessor = custom_pipeline_accessor.preprocessor
    X_train_processed = preprocessor.fit_transform(X_train)
    smote_enn = SMOTEENN(
        sampling_strategy=0.8, random_state=stg.RANDOM_STATE, n_jobs=-1
    )
    X_train, y_train = smote_enn.fit_resample(X_train_processed, y_train)
    gradient_classifier = GradientBoostingClassifier()
    gradient_classifier.fit(X_train, y_train)

    X_test = preprocessor.transform(X_test)
    gradient_classifier.predict(X_test)
    y_true, y_pred = y_test, gradient_classifier.predict(X_test)
    print(classification_report(y_true, y_pred))
    plot_confusion_matrix(gradient_classifier, X_test, y_test)


def main2():
    df_market = pd.read_csv(join(stg.RAW_DATA_DIR, "data.csv"), sep=stg.SEP)
    X = df_market.drop(columns=stg.COL_RAW_SUBSCRIPTION)
    y = df_market[stg.COL_RAW_SUBSCRIPTION].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=stg.RANDOM_STATE
    )
    X_train["SUBSCRIPTION"] = y_train
    X_test_with_target = X_test.copy()
    X_test_with_target["SUBSCRIPTION"] = y_test
    X_train.to_csv("data_train.csv", index=False, sep=stg.SEP)
    X_test_with_target.to_csv("data_test_target.csv", index=False, sep=stg.SEP)
    X_test.to_csv("data_test.csv", index=False, sep=stg.SEP)


if __name__ == "__main__":
    main()
