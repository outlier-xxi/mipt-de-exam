from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    proj_dir: str = "/app"

    url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
    data_dir: str = "/hdd/data"
    results_dir: str = "/hdd/results"

    @computed_field
    @property
    def data_file(self) -> str:
        return f"{self.data_dir}/wbdc.csv"


settings = Settings()
