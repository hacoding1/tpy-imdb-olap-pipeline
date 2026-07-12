import os 
import duckdb
from dotenv import load_dotenv
from typing import List, Optional
from pyspark.sql import DataFrame
from pyspark.sql import types as T
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from tpyImdbPipeline.utils.schema import *
from tpyImdbPipeline.utils.logger import get_logger
from tpyImdbPipeline.utils.statusTracker import StatusTracker
from tpyImdbPipeline.kaggleDownloader.kaggleDownloader import KaggleDownloader


logger = get_logger(__name__)


# Load environment variables
load_dotenv()
kaggleDataset = os.getenv("KAGGLE_DATASET")
kaggleDownloadDir = os.getenv("KAGGLE_DOWNLOAD_DIR")
targetParquetPath = os.getenv("TARGET_PARQUET_PATH")


def downloadDataFromKaggle():
    # Download data from Kaggle
    try:
        logger.info(f"Starting download of Kaggle dataset: {kaggleDataset}")
        kd = KaggleDownloader(download_directory=kaggleDownloadDir)
        kd.download_dataset(dataset=kaggleDataset, unzip=True, force=False, quiet=False)
    except Exception as e:
            logger.error(f"Error occurred while downloading Kaggle dataset: {e}")
            raise
    return


def readDataFrame(spark: SparkSession, **kwargs) -> DataFrame:
    # Read data from file into a Spark DataFrame with specified options
    try:
        logger.info(f"Reading data from file: {kwargs['file_path']}")
        reader = spark.read
        if "format" in kwargs:
            reader = reader.format(kwargs["format"])
        if "schema" in kwargs:
            reader = reader.schema(kwargs["schema"])
        if "sep" in kwargs:
            reader = reader.option("sep", kwargs["sep"])
        if "header" in kwargs:
            reader = reader.option("header", kwargs["header"])
        if "inferSchema" in kwargs:
            reader = reader.option("inferSchema", kwargs["inferSchema"])
        if "nullValue" in kwargs:
            reader = reader.option("nullValue", kwargs["nullValue"])
        if "options" in kwargs:
            for key, value in kwargs["options"].items():
                reader = reader.option(key, value)
        return reader.load(kwargs["file_path"])
    except Exception as e:
        logger.error(f"Error occurred while reading data from file: {e}")
        raise


def extractTransformLoad(spark:SparkSession):
    try:
        # Extract data from Kaggle dataset
        logger.info("Starting ETL process...")
        title_akas_df, title_basics_df, title_principals_df, title_ratings_df, person_df = (
                readDataFrame(spark, file_path=os.path.join(kaggleDownloadDir, "title.akas.tsv"), format="csv", schema=TitleAkasSchema.schema, sep="\t", header=True, nullValue="\\N"),
                readDataFrame(spark, file_path=os.path.join(kaggleDownloadDir, "title.basics.tsv"), format="csv", schema=TitleBasicsSchema.schema, sep="\t", header=True, nullValue="\\N"),
                readDataFrame(spark, file_path=os.path.join(kaggleDownloadDir, "title.principals.tsv"), format="csv", schema=TitlePrincipalsSchema.schema, sep="\t", header=True, nullValue="\\N"),
                readDataFrame(spark, file_path=os.path.join(kaggleDownloadDir, "title.ratings.tsv"), format="csv", schema=TitleRatingsSchema.schema, sep="\t", header=True, nullValue="\\N"),
                readDataFrame(spark, file_path=os.path.join(kaggleDownloadDir, "name.basics.tsv"), format="csv", schema=PersonSchema.schema, sep="\t", header=True, nullValue="\\N")
            )
        logger.info("Data extraction completed successfully, starting transformation...")
        # Transform data
        title_akas_df = (
            title_akas_df
            .withColumn("types", F.when(F.col("types").isNull() | (F.trim(F.col("types")) == ""), None).otherwise(F.split(F.col("types"), ",")))
            .withColumn("attributes", F.when(F.col("attributes").isNull() | (F.trim(F.col("attributes")) == ""), None).otherwise(F.split(F.col("attributes"), ",")))
            .withColumn("isOriginalTitle", F.col("isOriginalTitle").cast("boolean"))
        )
        # Transform data
        title_basics_df = (
            title_basics_df
            .withColumn("isAdult", F.col("isAdult").cast("boolean"))
            .withColumn("genres", F.when(F.col("genres").isNull() | (F.trim(F.col("genres")) == ""), None).otherwise(F.split(F.col("genres"), ",")))
        )
        # Transform data
        person_df = (
            person_df
            .withColumn("primaryProfession", F.when(F.col("primaryProfession").isNull() | (F.trim(F.col("primaryProfession")) == ""), None).otherwise(F.split(F.col("primaryProfession"), ",")))
            .withColumn("knownForTitles", F.when(F.col("knownForTitles").isNull() | (F.trim(F.col("knownForTitles")) == ""), None).otherwise(F.split(F.col("knownForTitles"), ",")))
        )
        logger.info("Writing transformed data to Parquet files...")
        # Write data to Parquet files
        movie_fact_cols = [
            "tconst", "titleType", "primaryTitle", "originalTitle", "isAdult", 
            "startYear", "endYear","runtimeMinutes","genres","averageRating","numVotes"
        ]
        movie_fact_df = title_basics_df.join(title_ratings_df, on="tconst", how="left").select(*movie_fact_cols) # .limit(1000) # limiting to 1000 rows as running in local machine
        movie_fact_partition_cols = ["titleType","startYear"]
        movie_fact_df.write.format("parquet").mode("overwrite").option("partitionOverwriteMode", "dynamic").option("compression", "snappy").partitionBy(*movie_fact_partition_cols).save(os.path.join(targetParquetPath, "movie_facts/"))
        # Write data to Parquet files
        movie_people_cols = [
            "tconst", "nconst", "primaryName", "birthYear", "deathYear",
            "primaryProfession", "category", "job", "characters"
        ]
        movie_people_df = title_principals_df.join(person_df, on="nconst", how="inner").select(*movie_people_cols) # .limit(1000) # limiting to 1000 rows as running in local machine
        movie_people_df.write.format("parquet").mode("overwrite").option("compression", "snappy").save(os.path.join(targetParquetPath, "movie_people/"))
        # Write data to Parquet files
        title_cols = [
            "titleId", "ordering", "title", "region", "language",
            "types", "attributes", "isOriginalTitle"
        ]
        title_df = title_akas_df.select(*title_cols) # .limit(1000) # limiting to 1000 rows as running in local machine
        title_df.write.format("parquet").mode("overwrite").option("compression", "snappy").save(os.path.join(targetParquetPath, "title_akas/"))
        logger.info("ETL process completed successfully.")
        return 
    except Exception as e:
        logger.error(f"Error occurred during ETL process: {e}")
        raise


def loadParquetToDuckDB(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    parquet_path: str,
    indexes: Optional[List[str]] = None,
) -> None:
    # Load Parquet files into DuckDB and create indexes if specified
    try:
        logger.info(f"Loading '{table_name}' into DuckDB...")
        con.execute(f"DROP TABLE IF EXISTS {table_name};")
        con.execute(f"""
            CREATE TABLE {table_name} AS
            SELECT *
            FROM read_parquet('{parquet_path}');
        """)
        if indexes:
            for column in indexes:
                con.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{table_name}_{column}
                    ON {table_name}({column});
                """)
        logger.info(f"Loaded table '{table_name}'.")
        return
    except Exception as e:
        logger.error(f"Error occurred while loading '{table_name}' into DuckDB: {e}")
        raise


def loadToOLAP():
    # Load Parquet datasets into DuckDB for OLAP queries
    try:
        logger.info("Loading Parquet datasets into DuckDB...")
        duckdb_path = os.getenv("DUCKDB_DATABASE_PATH")
        con = duckdb.connect(database=duckdb_path)
        loadParquetToDuckDB(
            con=con,
            table_name="movie_fact",
            parquet_path=os.path.join(targetParquetPath, "movie_facts", "**", "*.parquet"),
            indexes=["tconst", "primaryTitle", "startYear"]
        )
        loadParquetToDuckDB(
            con=con,
            table_name="movie_people",
            parquet_path=os.path.join(targetParquetPath, "movie_people", "*.parquet"),
            indexes=["tconst", "nconst"]
        )
        loadParquetToDuckDB(
            con=con,
            table_name="localized_titles",
            parquet_path=os.path.join(targetParquetPath, "title_akas", "*.parquet"),
            indexes=["titleId", "region"]
        )
        logger.info(con.execute("SHOW TABLES").fetchall())
        con.close()
    except Exception as e:
        logger.error(f"Error occurred while loading Parquet datasets into DuckDB: {e}")
        raise


def main():
    # Initialize Spark session and StatusTracker
    spark = SparkSession.builder.appName("tpyImdbPipeline").getOrCreate()
    tracker = StatusTracker(logger=logger)
    # Step 1: download
    if not tracker.has_marker("downloadDataFromKaggle"):
        logger.info("Starting downloadDataFromKaggle step...")
        downloadDataFromKaggle()
        tracker.create_marker("downloadDataFromKaggle")
    else:
        logger.info("Skipping downloadDataFromKaggle; marker exists")
    # Step 2: ETL (requires Spark)
    if not tracker.has_marker("extractTransformLoad"):
        try:
            logger.info("Starting extractTransformLoad step...")
            extractTransformLoad(spark)
            tracker.create_marker("extractTransformLoad")
        finally:
            spark.stop()
    else:
        logger.info("Skipping extractTransformLoad; marker exists")
    # Step 3: load to OLAP
    if not tracker.has_marker("loadToOLAP"):
        logger.info("Starting loadToOLAP step...")
        loadToOLAP()
        tracker.create_marker("loadToOLAP")
    else:
        logger.info("Skipping loadToOLAP; marker exists")
    # All done: remove markers so next full run can execute
    logger.info("All steps completed successfully. Clearing status markers for next run.")
    tracker.clear_all_markers()
    logger.info("Pipeline execution completed successfully.")
    return


if __name__ == "__main__":
    main()