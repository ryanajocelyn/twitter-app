from src.com.twitter.model.tweet_model import Tweets
from src.app import db

from flask import jsonify
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert


def search_tweets(search_criteria):
    tweets = Tweets.query

    if search_criteria['userId'] is not None:
        tweets = tweets.filter_by(author_id=search_criteria['userId'])

    if search_criteria['start_date'] is not None:
        tweets = tweets.filter_by(time >= search_criteria['start_date'])

    if search_criteria['end_date'] is not None:
        tweets = tweets.filter_by(time <= search_criteria['end_date'])

    return [twt.to_dict() for twt in tweets.all()]


def save_tweet(tweet_data):
    upsert(Tweets, {
        "tweet_id": tweet_data['id'],
        "orig_tweet_id": tweet_data['origId'],
        "tweet": tweet_data['text'],
        "time": datetime.strptime(tweet_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        "author_id": tweet_data['author_id']
    })

    # db.session.add(tweet)
    # db.session.commit()
    return None


def upsert(model, insert_dict):
    """model can be a db.Model or a table(), insert_dict should contain a primary or unique key."""
    inserted = insert(model).values(**insert_dict)
    upserted = inserted.on_duplicate_key_update(
        id=func.LAST_INSERT_ID(model.tweet_id), **{k: inserted.inserted[k]
                               for k, v in insert_dict.items()})
    res = db.engine.execute(upserted)

    return res.lastrowid