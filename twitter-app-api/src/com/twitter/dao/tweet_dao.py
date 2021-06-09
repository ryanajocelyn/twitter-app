from src.com.twitter.dao.database import db
from src.com.twitter.model.tweet_model import Tweets

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert


def get_all_tweets():
    tweets = Tweet.query.all()

    return tweets


def save_tweet(tweet_data):
    tweet = Tweets(
        tweet_id=tweet_data['id'],
        orig_tweet_id=tweet_data['origId'],
        tweet=tweet_data['text'],
        time=datetime.today()
    )

    upsert(Tweets, {
        "tweet_id": tweet_data['id'],
        "orig_tweet_id": tweet_data['origId'],
        "tweet": tweet_data['text'],
        "time": datetime.today()
    })

    # db.session.add(tweet)
    # db.session.commit()
    return tweet


def upsert(model, insert_dict):
    """model can be a db.Model or a table(), insert_dict should contain a primary or unique key."""
    inserted = insert(model).values(**insert_dict)
    upserted = inserted.on_duplicate_key_update(
        id=func.LAST_INSERT_ID(model.tweet_id), **{k: inserted.inserted[k]
                               for k, v in insert_dict.items()})
    res = db.engine.execute(upserted)

    return res.lastrowid