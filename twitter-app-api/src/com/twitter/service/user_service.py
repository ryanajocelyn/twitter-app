from flask import jsonify, request, current_app as app
from twitter import *

import requests
import json

from src.app import app
from src.com.twitter.dao.tweet_dao import save_tweet


def get_user_details_by_name(name):
    bearer_token = app.config['BEARER_TOKEN']
    base_url = app.config['TWITTER_URL']

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    url = f'{base_url}/2/users/by/username/{name}'
    res = requests.get(url, headers=headers)
    print(res.text)

    return jsonify(res.text)


def sync_tweets_by_id(user_id):
    bearer_token = config['BEARER_TOKEN']
    base_url = app.config['TWITTER_URL']

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f'{base_url}/2/users/{user_id}/tweets?tweet.fields=created_at'
    res = requests.get(url, headers=headers)
    tweets = res.json()
    for tw_data in tweets['data']:
        tw_data['origId'] = tweets['meta']['oldest_id']
        tw_data['author_id'] = user_id
        save_tweet(tw_data)

    return res.json()


def sync_timeline_by_id(user_id, user_name):
    oauth_token = json.loads(request.cookies.get('oauth_token'))

    twitter = Twitter(auth=OAuth(
        oauth_token['oauth_token'],
        oauth_token['oauth_token_secret'],
        app.config['TWITTER_CONSUMER_KEY'],
        app.config['TWITTER_CONSUMER_SECRET']
    ))
    statuses = twitter.statuses.home_timeline(count=50)
    # app.logger.info(statuses)

    for status in statuses:
        app.logger.info("(%s) @%s %s" % (status["created_at"], status["user"]["screen_name"], status["text"]))
        tw_data = dict({
            "tweet_id": status["id"],
            "app_user_id": user_id,
            "app_user_name": user_name,
            "author_id": status["user"]["screen_name"],
            "tweet": status["text"],
            "created_at": status["created_at"]
        })

        save_tweet(tw_data)

    return statuses
