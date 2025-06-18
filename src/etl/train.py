import json
import os

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.common.log import logger
from src.common.settings import settings


def main():
    logger.info(tmsg := f"process ...")

    logger.info(msg := f"Reading {settings.data_file_parquet} ...")
    df: pd.DataFrame = pd.read_parquet(settings.data_file_parquet)
    logger.info(f"{msg} done: {df.shape}")

    X: pd.DataFrame = df.drop(columns=['diagnosis'])

    # Encoding categorial target
    df['diagnosis_encoded'] = df['diagnosis'].map({'M': 0, 'B': 1})
    y: pd.Series = df['diagnosis_encoded']

    test_size = settings.test_size
    random_state = settings.random_state
    logger.info(msg := f"Splitting data ...")
    logger.info(f"Params: test_size: {test_size}; random_state: {random_state}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    logger.info(f"{msg} done")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Training
    max_iter = settings.max_iter
    logger.info(msg := f"Training model ...")
    logger.info(f"Params: max_iter: {max_iter}; random_state: {random_state}")
    model = LogisticRegression(max_iter=max_iter, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    logger.info(f"{msg} done")

    # Predict
    logger.info(msg := f"Evaluating model ...")
    y_pred = model.predict(X_test_scaled)

    # Evaluate
    accuracy: float  = accuracy_score(y_test, y_pred)
    precision: float = precision_score(y_test, y_pred)
    recall: float    = recall_score(y_test, y_pred)
    f1: float        = f1_score(y_test, y_pred)
    logger.info(f"{msg} done")
    logger.info(
        f"Result:\naccuracy: {accuracy:.2f}"
        f"\nprecision: {precision:.2f}"
        f"\nrecall: {recall:.2f}"
        f"\nf1: {f1:.2f}"
    )

    results_file: str = settings.results_file
    logger.info(msg := f"Writing results to: {results_file} ...")
    results = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

    os.makedirs(settings.results_dir, exist_ok=True)
    with open(results_file, "w") as f:
        json.dump(results, f)
    logger.info(f"{msg} done")

    logger.info(f"{tmsg} done")


if __name__ == '__main__':
    main()
