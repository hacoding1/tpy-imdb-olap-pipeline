# Dataset

- **Source:** https://www.kaggle.com/datasets/ashirwadsangwan/imdb-dataset/data
- **Dataset Name:** `ashirwadsangwan/imdb-dataset`

The IMDb dataset consists of five tab-separated value (TSV) files containing information about titles, ratings, cast & crew, localized titles, and people.

---

# Dataset Overview

## 1. `title.akas.tsv`

Contains localized and alternative titles for each IMDb title.

| Column | Type | Description |
|---------|------|-------------|
| `titleId` | String | IMDb title identifier (`tconst`). |
| `ordering` | Integer | Unique ordering of localized titles for a title. |
| `title` | String | Localized title. |
| `region` | String | Country or region code. |
| `language` | String | Language code. |
| `types` | Array\<String\> | Alternative title type (alternative, DVD, festival, TV, original, etc.). |
| `attributes` | Array\<String\> | Additional attributes describing the localized title. |
| `isOriginalTitle` | Boolean | Indicates whether the title is the original title. |

---

## 2. `title.basics.tsv`

Contains the primary metadata for movies, TV series, episodes, shorts and videos.

| Column | Type | Description |
|---------|------|-------------|
| `tconst` | String | IMDb title identifier. |
| `titleType` | String | Type of title (movie, short, tvSeries, tvEpisode, video, etc.). |
| `primaryTitle` | String | Commonly used title. |
| `originalTitle` | String | Original title in the original language. |
| `isAdult` | Boolean | Adult title indicator. |
| `startYear` | Integer | Release year or series start year. |
| `endYear` | Integer | Series end year (NULL for movies). |
| `runtimeMinutes` | Integer | Runtime in minutes. |
| `genres` | Array\<String\> | Up to three associated genres. |

---

## 3. `title.principals.tsv`

Contains principal cast and crew information.

| Column | Type | Description |
|---------|------|-------------|
| `tconst` | String | IMDb title identifier. |
| `ordering` | Integer | Principal ordering within a title. |
| `nconst` | String | IMDb person identifier. |
| `category` | String | Category such as actor, actress, director, writer, producer, etc. |
| `job` | String | Specific job title if available. |
| `characters` | String | Character name(s) played by the person. |

---

## 4. `title.ratings.tsv`

Contains aggregated IMDb ratings.

| Column | Type | Description |
|---------|------|-------------|
| `tconst` | String | IMDb title identifier. |
| `averageRating` | Double | Average IMDb rating. |
| `numVotes` | Integer | Number of user votes received. |

---

## 5. `name.basics.tsv`

Contains information about people associated with IMDb titles.

| Column | Type | Description |
|---------|------|-------------|
| `nconst` | String | IMDb person identifier. |
| `primaryName` | String | Primary credited name. |
| `birthYear` | Integer | Birth year. |
| `deathYear` | Integer | Death year (NULL if living). |
| `primaryProfession` | Array\<String\> | Up to three primary professions. |
| `knownForTitles` | Array\<String\> | IMDb title identifiers the person is known for. |

---

# Dataset Relationships

| Parent Table | Child Table | Join Column | Relationship |
|--------------|-------------|-------------|--------------|
| `title.basics` | `title.ratings` | `tconst` | One-to-zero/one |
| `title.basics` | `title.principals` | `tconst` | One-to-many |
| `name.basics` | `title.principals` | `nconst` | One-to-many |
| `title.basics` | `title.akas` | `tconst = titleId` | One-to-many |

The `title.basics` table serves as the central entity of the dataset. All other tables are linked either directly or indirectly through the IMDb title identifier (`tconst`) or the IMDb person identifier (`nconst`).
```