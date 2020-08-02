from datetime import datetime
import logging
import os
import praw
from dotenv import load_dotenv

load_dotenv(verbose=True)

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER = os.getenv("REDDIT_USER")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERAGENT = os.getenv("REDDIT_USERAGENT")
SUB_REDDIT = os.getenv("SUB_REDDIT")


class RedditNotifier:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USER,
            password=REDDIT_PASSWORD,
            user_agent=REDDIT_USERAGENT
        )
        self.sub_reddit = self.reddit.subreddit(SUB_REDDIT)

    def send_notification(self, content):
        logging.info(content.get('body'))
        self.sub_reddit.submit(
            title="{} : {}".format(content.get('title'), datetime.now().strftime("%Y-%m-%d")),
            selftext=content.get('body'),
            flair_id=content.get('flair_id')
        )


reddit_notifier = RedditNotifier()
