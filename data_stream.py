import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf


# - Create a schema for incoming resources
schema = StructType([
    StructField("crime_id", StringType(), True),
    StructField("original_crime_type_name", StringType(), True),
    StructField("report_date", StringType(), True),
    StructField("call_date", StringType(), True),
    StructField("offense_date", StringType(), True),
    StructField("call_time", StringType(), True),
    StructField("call_date_time", StringType(), True),
    StructField("disposition", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("agency_id", StringType(), True),
    StructField("address_type", StringType(), True),
    StructField("common_location", StringType(), True)
])

def run_spark_job(spark):

    # - Create Spark Configuration
    # Create Spark configurations with max offset of 200 per trigger
    # set up correct bootstrap server and port
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sf.police.servicecalls") \
        .option('maxOffsetsPerTrigger', 200) \
        .option('maxRatePerPartition', 200) \
        .option("startingOffsets", "earliest") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    # - extract the correct column from the kafka input resources
    # Take only value and convert it to String
    kafka_df = df.selectExpr("CAST(value AS STRING)") 

    service_table = kafka_df\
        .select(psf.from_json(psf.col('value'), schema).alias("DF"))\
        .select("DF.*")

    # - select original_crime_type_name and disposition
    distinct_table = service_table.select(psf.col("original_crime_type_name"), psf.col("disposition"))
    distinct_table.printSchema()
                
    # count the number of original crime type
    agg_df = distinct_table.select(distinct_table.original_crime_type_name, distinct_table.disposition) \
            .groupBy(psf.col("original_crime_type_name")) \
            .count()


    # - Q1. Submit a screen shot of a batch ingestion of the aggregation
    #   - write output stream
    query = agg_df \
            .writeStream \
            .format("console") \
            .outputMode("complete") \
            .start()

    # - attach a ProgressReporter
    query.awaitTermination()

    # - get the right radio code json path
    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)

    # clean up your data so that the column names match on radio_code_df and agg_df
    # we will want to join on the disposition code

    # - rename disposition_code column to disposition
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # - join on disposition column
    join_query = agg_df \
                .join(radio_code_df,"disposition") \
                .writeStream \
                .format("console") \
                .queryName("join") \
                .start()
    
    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # - Create Spark in Standalone mode
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .config("spark.ui.port", 3000) \ # for Spark Streaming UI 
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
