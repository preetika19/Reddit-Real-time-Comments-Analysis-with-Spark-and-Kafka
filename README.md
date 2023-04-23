# Reddit-Real-time-Comments-Analysis-with-Spark-and-Kafka
Analyse real-time comments on Subreddit posts using Spark, Kafka and ELK stack
<br>
a) Create a Python application that reads from a real-time data source, such as Reddit API using PRAW. <br>
b) This incoming data should continuously be written to a Kafka topic e.g., topic1 <br>
c) Create a PySpark structured streaming application that continuously reads data from the Kafka topic (topic1) and keeps a running count of the named entities being mentioned. <br>
d) At the trigger time, a message containing the named entities and their counts should be sent to another Kafka topic e.g., topic2 <br>
e) Configure Logstash, Elasticsearch, and Kibana to read from the Kafka topic (topic2) and create a bar plot of the top 10 most frequent named entities and their counts.
