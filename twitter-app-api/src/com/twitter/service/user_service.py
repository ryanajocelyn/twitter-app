from flask import jsonify
import requests

from src.com.twitter.dao.tweet_dao import save_tweet


def get_user_details_by_name(name):
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAMnFQQEAAAAAqPvH66omnGKAC67B%2BU6hXOJucvg%3DxmAOIgSCUsQ1eFt4N960sgvcIWXaat1htWqX5NvKr6YJuHvKbd"
    }
    url = f'https://api.twitter.com/2/users/by/username/{name}'
    res = requests.get(url, headers=headers)
    print(res.text)

    return jsonify(res.text)


def sync_tweets_by_id(user_id):
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAMnFQQEAAAAAqPvH66omnGKAC67B%2BU6hXOJucvg%3DxmAOIgSCUsQ1eFt4N960sgvcIWXaat1htWqX5NvKr6YJuHvKbd"
    }
    url = f'https://api.twitter.com/2/users/{user_id}/tweets?tweet.fields=created_at'
    res = requests.get(url, headers=headers)
    tweets = res.json()
    for tw_data in tweets['data']:
        tw_data['origId'] = tweets['meta']['oldest_id']
        tw_data['author_id'] = user_id
        save_tweet(tw_data)

    return res.json()
