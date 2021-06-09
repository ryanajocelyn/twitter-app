from flask import jsonify
import requests

from src.com.twitter.dao.tweet_dao import search_tweets


def get_tweets_by_criteria(search_criteria):
    return search_tweets(search_criteria)
