import os
import sys

import requests
from src.common.log import logger
from src.common.settings import settings


def main():
    logger.info(tmsg := f"fetcher ...")

    data_dir: str = settings.data_dir
    filename: str = settings.data_file_csv
    url: str = settings.url

    os.makedirs(data_dir, exist_ok=True)

    if not os.path.exists(filename):
        logger.info(msg := f"Getting {url} ...")
        with requests.session() as session, open(filename, "w") as file:
            response = session.get(url)
            response.raise_for_status()
            logger.info(f"Response: {response.status_code}")
            logger.info(f"{msg} done")
            if response.status_code == 200:
                logger.info(f"Writing to {filename} ...")
                file.write(response.text)
                logger.info(f"{msg} done")
            else:
                raise AssertionError(f"Failed to get: {url}")
    else:
        logger.info(f"File {filename} already exists. Skipping")
        sys.exit(99)

    logger.info(f"{tmsg} done")


if __name__ == '__main__':
    main()
