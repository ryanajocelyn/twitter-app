"""
Resource to handle the Tweet related operations
"""
from flask import Blueprint, jsonify, request
from flask_restful import reqparse, Resource
import logger

from src.app import app
from src.com.twitter.service.tweet_service import get_tweets_by_criteria

tweet_controller = Blueprint(name="tweets", import_name=__name__)

# Parser for Search Criteria
parser = reqparse.RequestParser()
parser.add_argument('userId')
parser.add_argument('start_date')
parser.add_argument('end_date')


class TweetSearchResource(Resource):
    """
    Resource to search tweets based on user, start and end date
    """
    def get(self):
        app.logger.info('Search Tweets..')
        search_criteria = parser.parse_args()
        return get_tweets_by_criteria(search_criteria)

