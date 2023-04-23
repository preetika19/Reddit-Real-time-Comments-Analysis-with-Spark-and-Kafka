import sys
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split
from pyspark.sql.functions import col, concat_ws , lit
from pyspark.sql.functions import to_json, struct
from pyspark.ml.feature import StopWordsRemover, RegexTokenizer



if __name__ == "__main__":
    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]
    sendTopic = sys.argv[4]

    # bootstrapServers = "localhost:9092"
    # subscribeType = "subscribe"
    # topics = "topic1"

    spark = SparkSession\
        .builder\
        .appName("RedditWordCount")\
        .getOrCreate()

    lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .option("failOnDataLoss", "false")\
        .load()\
        .selectExpr("CAST(value AS STRING)")

    lines = lines.toDF('text')
    tokenizer = RegexTokenizer(pattern=r'(?:\p{Punct}|\s)+', inputCol='text', outputCol='text_temp')
    txt_arr = tokenizer.transform(lines)

    remover = StopWordsRemover(inputCol="text_temp", outputCol="filtered_line")
    vector_no_stopw_df = remover.transform(txt_arr)

    word_column = vector_no_stopw_df.select(concat_ws(' ', vector_no_stopw_df.filtered_line).alias('word'))
    words = word_column.select(explode(split(word_column.word, ' ')).alias('word'))

    wordCounts = words.groupBy('word').count()
    wordCounts = wordCounts.select("word", to_json(struct("word","count")).alias("value"))

    kafka_df_string = wordCounts.select\
        (col("word").alias("key")\
        ,col("value"))

    query = kafka_df_string \
        .writeStream \
        .outputMode('update')\
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("checkpointLocation", "./pl")\
        .option("topic", sendTopic) \
        .start()

    # query = kafka_df_string\
    #     .writeStream \
    #     .outputMode('update')\
    #     .format("console")\
    #     .option("path", "./parc")\
    #     .start()


    query.awaitTermination()
