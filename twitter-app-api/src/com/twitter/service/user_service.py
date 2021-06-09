from flask import jsonify
from flask import current_app as app
import requests

from src.com.twitter.dao.tweet_dao import save_tweet


def get_user_details_by_name(name):
    bearer_token = config['BEARER_TOKEN']
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
