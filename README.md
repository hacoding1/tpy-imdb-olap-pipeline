# tpy-imdb-olap-pipeline

A PySpark-based ETL pipeline that downloads the IMDb dataset from Kaggle, transforms the raw TSV files, exports optimized Snappy-compressed Parquet datasets, and loads them into DuckDB for OLAP analytics.

---

# Features

- Download IMDb dataset directly from Kaggle
- Distributed ETL using Apache Spark Standalone Cluster
- PySpark DataFrame transformations
- Snappy-compressed Parquet output
- Category and time-based partitioning
- DuckDB OLAP database generation
- Index creation for faster analytical queries
- Dockerized Spark Master + scalable Spark Workers
- Python Wheel packaging

---

# Project Structure

```text
tpy-imdb-olap-pipeline
│
├── data
│   ├── raw
│   ├── processed
│   └── notebooks
│
├── database
│   └── duckdb
│
├── dist
│
├── jobs
│   └── run_pipeline.py
│
├── logs
│
├── spark
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
│
├── tpyImdbPipeline
│
├── docker-compose.yml
├── setup.py
├── requirements.txt
└── .env
```

---

# Prerequisites

- Python 3.8+
- Docker Desktop
- Docker Compose
- Git
- Windows Winget (for DuckDB CLI)

---

# 1. Clone Repository

```bash
git clone <repository-url>

cd tpy-imdb-olap-pipeline
```

---

# 2. Create Python Virtual Environment

## Windows

```cmd
python -m venv .venv

.venv\Scripts\activate
```

## Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Upgrade pip.

```bash
python -m pip install --upgrade pip
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# 3. Build Python Wheel

```bash
python -m build
```

Generated wheel:

```text
dist/
```

---

# 4. Configure Environment Variables

Create `.env`

```properties
# ============================================================
# Logging
# ============================================================

LOG_PATH="/opt/project/logs/"
LOG_FILE_NAME="tpyImdbPipeline.log"

# ============================================================
# Kaggle
# ============================================================

KAGGLE_USERNAME="your_kaggle_username"
KAGGLE_KEY="your_kaggle_api_key"

KAGGLE_DOWNLOAD_DIR="/opt/project/data/raw/"
KAGGLE_DATASET="ashirwadsangwan/imdb-dataset"

# ============================================================
# Parquet Output
# ============================================================

TARGET_PARQUET_PATH="/opt/project/data/processed/"

# ============================================================
# DuckDB
# ============================================================

DUCKDB_DATABASE_PATH="/opt/project/database/duckdb/imdb.duckdb"

# ============================================================
# Spark Worker Configuration
# ============================================================

SPARK_WORKER_MEMORY=2G
SPARK_WORKER_CORES=2
```

---

# 5. Build Docker Image

```bash
docker compose build --no-cache
```

Verify image.

```bash
docker images
```

---

# 6. Start Spark Cluster

Start Spark Master with two workers.

```bash
docker compose up -d --build --scale spark-worker=2
```

Use any number of workers.

Example:

```bash
docker compose up -d --build --scale spark-worker=4
```

Verify containers.

```bash
docker ps
```

View master logs.

```bash
docker logs spark-master
```

Spark Master UI

```
http://localhost:8080
```

---

# 7. Verify Spark Installation

Open shell.

```bash
docker exec -it spark-master bash
```

Current user.

```bash
whoami
```

Python version.

```bash
python --version
```

Installed packages.

```bash
pip freeze
```

Spark version.

```bash
spark-submit --version
```

Verify PySpark.

```python
import pyspark

print(pyspark.__version__)

exit()
```

---

# 8. Install Latest Wheel

Whenever the project code changes:

Build a new wheel.

```bash
python -m build
```

Reinstall inside Spark Master.

```bash
docker exec spark-master \
pip install --force-reinstall /opt/project/dist/tpyImdbPipeline-*.whl
```

---

# 9. Execute Spark ETL Pipeline

## Windows CMD

```cmd
docker exec spark-master spark-submit --master spark://spark-master:7077 --py-files /opt/project/dist/tpyImdbPipeline-1.0.0-py3-none-any.whl /opt/project/jobs/run_pipeline.py
```

## Linux/macOS

```bash
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --py-files /opt/project/dist/tpyImdbPipeline-1.0.0-py3-none-any.whl \
    /opt/project/jobs/run_pipeline.py
```

The pipeline performs the following steps:

1. Download IMDb dataset from Kaggle
2. Read TSV datasets
3. Transform data using PySpark
4. Export Snappy-compressed Parquet datasets
5. Load Parquet datasets into DuckDB
6. Create OLAP tables
7. Create indexes

---

# 10. Output Generated

```text
data
├── raw
│
├── processed
│   ├── movie_facts
│   ├── movie_people
│   └── title_akas
│
database
└── duckdb
    └── imdb.duckdb

logs
└── tpyImdbPipeline.log
```

---

# 11. Install DuckDB CLI (Windows)

Install using Winget.

```cmd
winget install DuckDB.cli
```

If `duckdb` is not recognized after installation, add the following directory to your **User PATH**.

```text
C:\Users\<username>\AppData\Local\Microsoft\WinGet\Packages\DuckDB.cli_Microsoft.Winget.Source_8wekyb3d8bbwe
```

Close and reopen Command Prompt.

Verify installation.

```cmd
duckdb --version
```

---

# 12. Query DuckDB

Open database.

```cmd
duckdb database\duckdb\imdb.duckdb
```

Show tables.

```sql
SHOW TABLES;
```

Describe table.

```sql
DESCRIBE movie_fact;
```

Preview data.

```sql
SELECT *
FROM movie_fact
LIMIT 10;
```

Record count.

```sql
SELECT COUNT(*)
FROM movie_fact;
```

Top-rated movies.

```sql
SELECT
    primaryTitle,
    startYear,
    averageRating,
    numVotes
FROM movie_fact
WHERE numVotes > 10000
ORDER BY averageRating DESC,
         numVotes DESC
LIMIT 10;
```

Movies released in 2020.

```sql
SELECT
    primaryTitle,
    averageRating
FROM movie_fact
WHERE startYear = 2020
ORDER BY averageRating DESC;
```

Top cast/crew by number of titles.

```sql
SELECT
    primaryName,
    category,
    COUNT(*) AS total_titles
FROM movie_people
GROUP BY
    primaryName,
    category
ORDER BY total_titles DESC
LIMIT 20;
```

Localized titles for a movie.

```sql
SELECT
    title,
    region,
    language,
    isOriginalTitle
FROM localized_titles
WHERE titleId='tt0111161';
```

Exit DuckDB.

```sql
.exit
```

---

# 13. Monitor Spark Cluster

Spark Master UI

```
http://localhost:8080
```

View running containers.

```bash
docker ps
```

Master logs.

```bash
docker logs spark-master
```

Worker logs.

```bash
docker logs custom-spark-cluster-spark-worker-1
```

View running Spark applications.

```bash
http://localhost:8080
```

---

# 14. Stop Cluster

```bash
docker compose down -v
```

---

# 15. Remove Docker Image

```bash
docker rmi custom-spark
```

---

# Rebuilding After Code Changes

Whenever application code changes:

Build wheel.

```bash
python -m build
```

Reinstall wheel.

```bash
docker exec spark-master \
pip install --force-reinstall /opt/project/dist/tpyImdbPipeline-*.whl
```

Run pipeline.

```cmd
docker exec spark-master spark-submit --master spark://spark-master:7077 --py-files /opt/project/dist/tpyImdbPipeline-1.0.0-py3-none-any.whl /opt/project/jobs/run_pipeline.py
```

No Docker image rebuild is required unless:

- Dockerfile changes
- Python dependencies change (`requirements.txt`)
- Spark image configuration changes