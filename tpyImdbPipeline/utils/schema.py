from pyspark.sql import types as T


class TitleAkasSchema:
    schema = T.StructType([
        T.StructField("titleId", T.StringType(), True),
        T.StructField("ordering", T.IntegerType(), True),
        T.StructField("title", T.StringType(), True),
        T.StructField("region", T.StringType(), True),
        T.StructField("language", T.StringType(), True),
        T.StructField("types", T.StringType(), True),
        T.StructField("attributes", T.StringType(), True),
        T.StructField("isOriginalTitle", T.IntegerType(), True),
    ])


class TitleBasicsSchema:
    schema = T.StructType([
        T.StructField("tconst", T.StringType(), True),
        T.StructField("titleType", T.StringType(), True),
        T.StructField("primaryTitle", T.StringType(), True),
        T.StructField("originalTitle", T.StringType(), True),
        T.StructField("isAdult", T.IntegerType(), True),
        T.StructField("startYear", T.IntegerType(), True),
        T.StructField("endYear", T.IntegerType(), True),
        T.StructField("runtimeMinutes", T.IntegerType(), True),
        T.StructField("genres", T.StringType(), True),
    ])


class TitlePrincipalsSchema:
    schema = T.StructType([
        T.StructField("tconst", T.StringType(), True),
        T.StructField("ordering", T.IntegerType(), True),
        T.StructField("nconst", T.StringType(), True),
        T.StructField("category", T.StringType(), True),
        T.StructField("job", T.StringType(), True),
        T.StructField("characters", T.StringType(), True),
    ])


class TitleRatingsSchema:
    schema = T.StructType([
        T.StructField("tconst", T.StringType(), True),
        T.StructField("averageRating", T.DoubleType(), True),
        T.StructField("numVotes", T.IntegerType(), True),
    ])


class PersonSchema:
    schema = T.StructType([
        T.StructField("nconst", T.StringType(), True),
        T.StructField("primaryName", T.StringType(), True),
        T.StructField("birthYear", T.IntegerType(), True),
        T.StructField("deathYear", T.IntegerType(), True),
        T.StructField("primaryProfession", T.StringType(), True),
        T.StructField("knownForTitles", T.StringType(), True),
    ])