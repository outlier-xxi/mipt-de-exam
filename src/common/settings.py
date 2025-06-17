from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    proj_dir: str = "/data/study.local/mipt.de"

    url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
    data_dir: str = "/hdd/data"
    results_dir: str = "/hdd/results"

settings = Settings()
