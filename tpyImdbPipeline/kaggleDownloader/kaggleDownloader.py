import os
from pathlib import Path
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
from tpyImdbPipeline.utils.logger import get_logger


load_dotenv()
logger = get_logger(__name__)


class KaggleDownloader:
    """
    Downloads datasets from Kaggle using the official Kaggle API.
    """
    def __init__(self, download_directory: Path):
        self.download_directory = Path(download_directory)
        self.download_directory.mkdir(parents=True, exist_ok=True)
        os.environ["KAGGLE_USERNAME"] = os.getenv("KAGGLE_USERNAME", "")
        os.environ["KAGGLE_API_TOKEN"] = os.getenv("KAGGLE_API_TOKEN", "")
        if not os.environ["KAGGLE_USERNAME"] or not os.environ["KAGGLE_API_TOKEN"]:
            raise ValueError(
                "KAGGLE_USERNAME and KAGGLE_API_TOKEN must be configured in the .env file."
            )
        self.api = KaggleApi()
        self.api.authenticate()

    def download_dataset(
        self,
        dataset: str,
        unzip: bool = True,
        force: bool = False,
        quiet: bool = False,
    ) -> Path:
        logger.info("Downloading Kaggle dataset: %s", dataset)
        self.api.dataset_download_files(
            dataset=dataset,
            path=str(self.download_directory),
            unzip=unzip,
            force=force,
            quiet=quiet,
        )
        logger.info("Dataset downloaded successfully to %s", self.download_directory)
        return self.download_directory