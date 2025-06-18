from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    proj_dir: str    = "/app"

    # Source URL
    url: str         = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
    data_dir: str    = "/hdd/data"
    results_dir: str = "/hdd/results"

    @computed_field
    @property
    def data_file_csv(self) -> str:
        return f"{self.data_dir}/wbdc.csv"

    @computed_field
    @property
    def data_file_parquet(self) -> str:
        return f"{self.data_dir}/wbdc.parquet"

    # Column names for downloaded dataset
    column_names: list[str] = [
        'id',
        'diagnosis',
        # 1
        'radius1',
        'texture1',
        'perimeter1',
        'area1',
        'smoothness1',
        'compactness1',
        'concavity1',
        'concave_points1',
        'symmetry1',
        'fractal_dimension1',
        # 2
        'radius2',
        'texture2',
        'perimeter2',
        'area2',
        'smoothness2',
        'compactness2',
        'concavity2',
        'concave_points2',
        'symmetry2',
        'fractal_dimension2',
        # 3
        'radius3',
        'texture3',
        'perimeter3',
        'area3',
        'smoothness3',
        'compactness3',
        'concavity3',
        'concave_points3',
        'symmetry3',
        'fractal_dimension3',
    ]

    test_size: float  =    0.2
    random_state: int =     42
    max_iter: int     = 10_000

    @computed_field
    @property
    def results_file(self) -> str:
        return f"{self.results_dir}/results.json"

    # yandex_oauth_token: str
    # yandex_iam_url: str = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    # yandex_disk_url: str = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    # yandex_disk_folder: str = "tmp/de-exam/results.json"


settings = Settings()
