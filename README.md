# Spark Streaming Project - SF Crime Statistics

## Introduction

Statistical analyses of the Kaggle - San Francisco crime incidents data using Apache Spark Structured Streaming. This project will create a Kafka server to produce data, and ingest data through Spark Structured Streaming. Udacity Data Streaming Project

## Requirements
* Spark 2.4.3
* Scala 2.11.x
* Java 1.8.x
* Kafka build with Scala 2.11.x
* Python 3.6.x or 3.7.x

## How to use the application

In order to run the application you will need to start:

1. Zookeeper config:

`/usr/bin/zookeeper-server-start config/zookeeper.properties`

2. Kafka server config:

`/usr/bin/kafka-server-start config/server.properties`

3. Kafka consumer - kafka-console-consumer:

`kafka-console-consumer --bootstrap-server localhost:9092 --topic sf.police.servicecalls --from-beginning'

4. Run Spark job - Spark-submit:

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py`


### Kafka Consumer Console Output

![alt text](https://github.com/lemonjchung/Spark-Streaming_SFCrime-Statistics/blob/main/screenshots/SFCrime_Kafka-console-consumer2.png)

### Spark Job - progress reporter

![alt text](https://github.com/lemonjchung/Spark-Streaming_SFCrime-Statistics/blob/main/screenshots/SFCrime_datastream_spark-submit2.png)

### Spark UI

![alt text](https://github.com/lemonjchung/Spark-Streaming_SFCrime-Statistics/blob/main/screenshots/SFCrime-SparkStreamingUI1.png)

![alt text](https://github.com/lemonjchung/Spark-Streaming_SFCrime-Statistics/blob/main/screenshots/SFCrime-SparkStreamingUI2.png)

