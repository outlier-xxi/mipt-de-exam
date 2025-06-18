import os

import pandas as pd

from src.common.log import logger
from src.common.settings import settings


def main():
    logger.info(tmsg := f"import ...")

    in_filename: str = settings.data_file_csv
    if not os.path.exists(in_filename):
        logger.error(msg := f"File {in_filename} does not exist")
        raise AssertionError(msg)

    logger.info(msg := f"Reading {in_filename} ...")
    df: pd.DataFrame = pd.read_csv(in_filename, header=None)
    logger.info(f"{msg} done: {df.shape}")
    df.columns = settings.column_names
    logger.info(f"Target values: {df['diagnosis'].value_counts()}")

    logger.info(msg := f"Checking for nulls ...")
    count_null: int = df.isnull().sum().sum()
    if count_null:
        logger.error(f"Found {count_null} nulls, extend your code")
        raise AssertionError(msg)
    logger.info(f"{msg} done: {count_null}")

    logger.info(msg := f"Checking for duplicates ...")
    count_dups: int = df.duplicated().sum()
    if count_dups:
        logger.error(f"Found {count_dups} duplicates, extend your code")
        raise AssertionError(msg)
    logger.info(f"{msg} done: {count_dups}")

    out_filename: str = settings.data_file_parquet
    logger.info(msg := f"Writing to {out_filename} ...")
    df.to_parquet(out_filename, index=False)
    logger.info(f"{msg} done")

    logger.info(f"{tmsg} done")


if __name__ == '__main__':
    main()
