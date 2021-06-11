from src.com.twitter.model.tweet_model import Tweets
from src.app import db, app

from flask import jsonify
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert


def search_tweets(search_criteria):
    tweets = Tweets.query

    if search_criteria['userId'] is not None:
        tweets = tweets.filter_by(app_user_id=search_criteria['userId'])

    if search_criteria['start_date'] is not None:
        tweets = tweets.filter_by(created_at >= search_criteria['start_date'])

    if search_criteria['end_date'] is not None:
        tweets = tweets.filter_by(created_at <= search_criteria['end_date'])

    return [twt.to_dict() for twt in tweets.all()]


def save_tweet(tweet_data):
    try:
        upsert(Tweets, {
            "tweet_id": tweet_data['tweet_id'],
            "app_user_id": tweet_data['app_user_id'],
            "app_user_name": tweet_data['app_user_name'],
            "author_id": tweet_data['author_id'],
            "tweet": tweet_data['tweet'],
            "created_at": datetime.strptime(tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
        })
    except:
        app.logger.error(f"Error while saving Tweet: {tweet_data['tweet_id']}")

    # Fri Jun 11 07:05:28 +0000 2021
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
