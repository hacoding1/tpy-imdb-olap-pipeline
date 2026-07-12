from setuptools import setup, find_packages

setup(
    name="tpyImdbPipeline",
    version="1.0.0",
    description="IMDb Spark ETL Pipeline",
    author="Harish Aravindh",
    author_email="ha30.coding1@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "pyspark",
        "pandas",
        "pyarrow",
        "duckdb",
        "boto3",
        "python-dotenv",
        "kaggle",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "tpy-imdb=tpyImdbPipeline.main:main",
        ]
    }
)