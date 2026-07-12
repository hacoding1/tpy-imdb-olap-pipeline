-- ============================================================
-- IMDb OLAP Queries
-- ============================================================

-- List all tables
SHOW TABLES;

-- ============================================================
-- Row Counts
-- ============================================================

SELECT COUNT(*) AS total_movies
FROM movie_fact;

SELECT COUNT(*) AS total_people
FROM movie_people;

SELECT COUNT(*) AS total_localized_titles
FROM localized_titles;

-- ============================================================
-- Schema
-- ============================================================

DESCRIBE movie_fact;

DESCRIBE movie_people;

DESCRIBE localized_titles;

-- ============================================================
-- Top Rated Movies
-- ============================================================

SELECT
    primaryTitle,
    startYear,
    averageRating,
    numVotes
FROM movie_fact
WHERE titleType = 'movie'
ORDER BY averageRating DESC,
         numVotes DESC
LIMIT 20;

-- ============================================================
-- Highest Rated TV Series
-- ============================================================

SELECT
    primaryTitle,
    averageRating,
    numVotes
FROM movie_fact
WHERE titleType='tvSeries'
ORDER BY averageRating DESC,
         numVotes DESC
LIMIT 20;

-- ============================================================
-- Movies Released Per Year
-- ============================================================

SELECT
    startYear,
    COUNT(*) AS total_titles
FROM movie_fact
WHERE titleType='movie'
GROUP BY startYear
ORDER BY startYear;

-- ============================================================
-- Average Rating By Title Type
-- ============================================================

SELECT
    titleType,
    ROUND(AVG(averageRating),2) AS average_rating,
    COUNT(*) AS total_titles
FROM movie_fact
GROUP BY titleType
ORDER BY average_rating DESC;

-- ============================================================
-- Adult vs Non Adult Titles
-- ============================================================

SELECT
    isAdult,
    COUNT(*) AS total_titles
FROM movie_fact
GROUP BY isAdult;

-- ============================================================
-- Longest Movies
-- ============================================================

SELECT
    primaryTitle,
    runtimeMinutes,
    startYear
FROM movie_fact
WHERE runtimeMinutes IS NOT NULL
ORDER BY runtimeMinutes DESC
LIMIT 20;

-- ============================================================
-- Most Voted Movies
-- ============================================================

SELECT
    primaryTitle,
    numVotes,
    averageRating
FROM movie_fact
ORDER BY numVotes DESC
LIMIT 20;

-- ============================================================
-- Average Runtime By Genre
-- ============================================================

SELECT
    genre,
    ROUND(AVG(runtimeMinutes),2) AS avg_runtime,
    COUNT(*) AS total_titles
FROM (
    SELECT
        runtimeMinutes,
        UNNEST(genres) AS genre
    FROM movie_fact
)
GROUP BY genre
ORDER BY avg_runtime DESC;

-- ============================================================
-- Average Rating By Genre
-- ============================================================

SELECT
    genre,
    ROUND(AVG(averageRating),2) AS avg_rating,
    COUNT(*) AS total_titles
FROM (
    SELECT
        averageRating,
        UNNEST(genres) AS genre
    FROM movie_fact
)
GROUP BY genre
ORDER BY avg_rating DESC;

-- ============================================================
-- Top Actors
-- ============================================================

SELECT
    primaryName,
    COUNT(*) AS movie_count
FROM movie_people
WHERE category='actor'
GROUP BY primaryName
ORDER BY movie_count DESC
LIMIT 20;

-- ============================================================
-- Top Directors
-- ============================================================

SELECT
    primaryName,
    COUNT(*) AS movies_directed
FROM movie_people
WHERE category='director'
GROUP BY primaryName
ORDER BY movies_directed DESC
LIMIT 20;

-- ============================================================
-- Most Common Professions
-- ============================================================

SELECT
    profession,
    COUNT(*) AS total_people
FROM (
    SELECT
        UNNEST(primaryProfession) AS profession
    FROM movie_people
)
GROUP BY profession
ORDER BY total_people DESC;

-- ============================================================
-- Localized Titles By Region
-- ============================================================

SELECT
    region,
    COUNT(*) AS total_titles
FROM localized_titles
GROUP BY region
ORDER BY total_titles DESC;

-- ============================================================
-- Localized Titles By Language
-- ============================================================

SELECT
    language,
    COUNT(*) AS total_titles
FROM localized_titles
GROUP BY language
ORDER BY total_titles DESC;

-- ============================================================
-- Top Rated Movies With Directors
-- ============================================================

SELECT
    mf.primaryTitle,
    mf.averageRating,
    mp.primaryName AS director
FROM movie_fact mf
JOIN movie_people mp
    ON mf.tconst = mp.tconst
WHERE mp.category='director'
ORDER BY mf.averageRating DESC
LIMIT 20;

-- ============================================================
-- Movies With Multiple Directors
-- ============================================================

SELECT
    mf.primaryTitle,
    COUNT(*) AS directors
FROM movie_fact mf
JOIN movie_people mp
    ON mf.tconst=mp.tconst
WHERE mp.category='director'
GROUP BY mf.primaryTitle
HAVING COUNT(*) > 1
ORDER BY directors DESC;

-- ============================================================
-- Top 100 Movies (Minimum 10,000 Votes)
-- ============================================================

SELECT
    primaryTitle,
    startYear,
    averageRating,
    numVotes
FROM movie_fact
WHERE numVotes >= 10000
ORDER BY averageRating DESC
LIMIT 100;