/******************************************************************************
 File Name  : queriesOLAPDDL.sql

 Description
 ------------------------------------------------------------------------------
 This file documents the DuckDB DDL statements used by the IMDb OLAP pipeline.

 The ETL pipeline performs the following sequence:

    1. Download IMDb dataset from Kaggle
    2. Transform raw TSV files using PySpark
    3. Export Snappy-compressed Parquet datasets
    4. Load Parquet datasets into DuckDB
    5. Create indexes for OLAP queries

 NOTE
 ----
 These DDL statements are executed programmatically from:

     tpyImdbPipeline/main.py

 Specifically:

     loadToOLAP()
        └── loadParquetToDuckDB()

 executes the equivalent SQL shown below.

 This SQL file is provided as documentation/reference to satisfy the project
 deliverable requiring the OLAP database DDL.
******************************************************************************/

------------------------------------------------------------------------------
-- Drop Existing Tables
------------------------------------------------------------------------------

DROP TABLE IF EXISTS movie_fact;

DROP TABLE IF EXISTS movie_people;

DROP TABLE IF EXISTS localized_titles;


------------------------------------------------------------------------------
-- Movie Fact Table
--
-- Source:
--     data/processed/movie_facts/
--
-- Partitioned By:
--     titleType
--     startYear
------------------------------------------------------------------------------

CREATE TABLE movie_fact AS
SELECT *
FROM read_parquet(
    '/opt/project/data/processed/movie_facts/**/*.parquet'
);


------------------------------------------------------------------------------
-- Movie People Table
--
-- Source:
--     data/processed/movie_people/
------------------------------------------------------------------------------

CREATE TABLE movie_people AS
SELECT *
FROM read_parquet(
    '/opt/project/data/processed/movie_people/*.parquet'
);


------------------------------------------------------------------------------
-- Localized Titles Table
--
-- Source:
--     data/processed/title_akas/
------------------------------------------------------------------------------

CREATE TABLE localized_titles AS
SELECT *
FROM read_parquet(
    '/opt/project/data/processed/title_akas/*.parquet'
);


------------------------------------------------------------------------------
-- Indexes
--
-- These indexes are created after loading the Parquet datasets to improve
-- lookup and join performance for analytical workloads.
------------------------------------------------------------------------------

--------------------------------------------------
-- movie_fact
--------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_movie_fact_tconst
ON movie_fact(tconst);

CREATE INDEX IF NOT EXISTS idx_movie_fact_primaryTitle
ON movie_fact(primaryTitle);

CREATE INDEX IF NOT EXISTS idx_movie_fact_startYear
ON movie_fact(startYear);


--------------------------------------------------
-- movie_people
--------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_movie_people_tconst
ON movie_people(tconst);

CREATE INDEX IF NOT EXISTS idx_movie_people_nconst
ON movie_people(nconst);


--------------------------------------------------
-- localized_titles
--------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_localized_titles_titleId
ON localized_titles(titleId);

CREATE INDEX IF NOT EXISTS idx_localized_titles_region
ON localized_titles(region);


------------------------------------------------------------------------------
-- Validation Queries
------------------------------------------------------------------------------

-- List all OLAP tables

SHOW TABLES;


-- Verify schema

DESCRIBE movie_fact;

DESCRIBE movie_people;

DESCRIBE localized_titles;


-- Verify row counts

SELECT COUNT(*) AS movie_fact_count
FROM movie_fact;

SELECT COUNT(*) AS movie_people_count
FROM movie_people;

SELECT COUNT(*) AS localized_titles_count
FROM localized_titles;

------------------------------------------------------------------------------
-- End of File
------------------------------------------------------------------------------
