import praw
from kafka import KafkaProducer
import json
import re
import time
import sys

bootstrapServers = sys.argv[1]
sendTopic = sys.argv[2]

producer = KafkaProducer(bootstrap_servers=bootstrapServers)

reddit = praw.Reddit(client_id="",
                client_secret="",
                user_agent="")

subreddit = reddit.subreddit('soccer')

data = []

for comment in subreddit.stream.comments():
    try:
        print(30*'_')
        print()
        parent_id = str(comment.parent())
        submission = reddit.comment(parent_id)
        if (parent_id):
            print(comment.body)
            producer.send(sendTopic, comment.body.encode('utf-8'))


    except praw.exceptions.PRAWException as e:
        pass
