# tpy-imdb-olap-pipeline

## Prerequisites

* Python 3.8+
* Docker Desktop
* Docker Compose
* Git

---

# 1. Clone the Repository

```bash
git clone <repository-url>
cd tpy-imdb-olap-pipeline
```

---

# 2. Create Python Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade pip and install development dependencies.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# 3. Build the Python Wheel

```bash
python -m build
```

The generated wheel will be available under:

```text
dist/
```

---

# 4. Configure Environment Variables

Create or update the `.env` file.

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
KAGGLE_API_TOKEN="your_kaggle_api_token"

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
# Spark Worker Configuration (Optional)
# ============================================================

SPARK_WORKER_MEMORY=2G
SPARK_WORKER_CORES=2
```

---

# 5. Build Docker Image

```bash
docker compose build --no-cache
```

Verify the image.

```bash
docker images
```

---

# 6. Start Spark Cluster

Start one Spark Master and N Spark Workers.

```bash
docker compose up -d --build --scale spark-worker=2
```

Verify containers.

```bash
docker ps
```

Check the Spark Master logs.

```bash
docker logs spark-master
```

Spark Master UI:

```
http://localhost:8080
```

---

# 7. Verify Container

Open a shell.

```bash
docker exec -it spark-master bash
```

Verify user.

```bash
whoami
```

Verify Python.

```bash
python --version
```

Verify installed packages.

```bash
pip freeze
```

Verify Spark.

```bash
spark-submit --version
```

Verify PySpark.

```python
import pyspark

print(pyspark.__version__)
```

Exit Python.

```python
exit()
```

---

# 8. Install Latest Wheel

Since the wheel is mounted through the `dist/` volume, reinstall it after every build.

```bash
docker exec spark-master \
pip install --force-reinstall /opt/project/dist/tpyImdbPipeline-*.whl
```

---

# 9. Execute Spark ETL Job

Test with sample execution.

```cmd
docker exec spark-master spark-submit ^
  --master spark://spark-master:7077 ^
  --py-files /opt/project/dist/tpyImdbPipeline-1.0.0-py3-none-any.whl ^
  /opt/project/jobs/run_pipeline.py
```

Submit the Spark job.

```bash
docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --py-files /opt/project/dist/tpyImdbPipeline-1.0.0-py3-none-any.whl \
    /opt/project/jobs/run_pipeline.py
```

Submit the Spark job (Windows CMD Prompt).

```cmd
docker exec spark-master spark-submit --master spark://spark-master:7077 --py-files /opt/project/dist/tpyImdbPipeline-1.0.0-py3-none-any.whl /opt/project/jobs/run_pipeline.py
```

The pipeline performs the following steps:

1. Download IMDb dataset from Kaggle
2. Extract TSV datasets
3. Apply data transformations
4. Export Snappy-compressed Parquet datasets
5. Load Parquet datasets into DuckDB
6. Create OLAP tables and indexes

---

# 10. Generated Output

```
data/
├── raw/
│
├── processed/
│   ├── movie_facts/
│   ├── movie_people/
│   └── title_akas/
│
database/
└── duckdb/
    └── imdb.duckdb

logs/
└── tpyImdbPipeline.log
```

---

# 11. Query DuckDB

The generated database can be opened directly from the host machine.

Example:

```bash
duckdb database/duckdb/imdb.duckdb
```

Useful commands:

```sql
SHOW TABLES;

DESCRIBE movie_fact;

SELECT *
FROM movie_fact
LIMIT 10;
```

---

# 12. Stop the Cluster

Stop all containers and remove associated volumes.

```bash
docker compose down -v
```

---

# 13. Remove Docker Image

```bash
docker rmi custom-spark
```
