import os
import requests
from src.common.log import logger
from src.common.settings import settings


def main():
    logger.info(tmsg := f"fetcher ...")

    data_dir = settings.data_dir
    filename: str = f"{data_dir}/wbdc.csv"
    url: str = settings.url

    os.makedirs(data_dir, exist_ok=True)

    if not os.path.exists(filename):
        logger.info(msg := f"Getting {url} ...")
        with requests.session() as session, open(filename, "w") as file:
            response = session.get(url)
            response.raise_for_status()
            logger.info(f"Response: {response.status_code}")
            if response.status_code == 200:
                file.write(response.text)

        logger.info(f"{tmsg} done")


if __name__ == '__main__':
    main()
