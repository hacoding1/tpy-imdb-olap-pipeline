import os 
from dotenv import load_dotenv
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from tpyImdbPipeline.utils.logger import get_logger
from tpyImdbPipeline.kaggleDownloader.kaggleDownloader import KaggleDownloader

logger = get_logger(__name__)

def main():

    # load environment
    load_dotenv()

    # download data from Kaggle
    kaggle_download_dir = os.getenv("KAGGLE_DOWNLOAD_DIR") # "./data/raw/"
    kd = KaggleDownloader(download_directory=kaggle_download_dir)
    dataset = os.getenv("KAGGLE_DATASET")
    kd.download_dataset(dataset=dataset, unzip=True, force=False, quiet=False)

    # initialize Spark session
    spark = SparkSession.builder.appName("tpyImdbPipeline").getOrCreate()

    

if __name__ == "__main__":
    main()