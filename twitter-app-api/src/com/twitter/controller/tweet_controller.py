from flask import Blueprint, jsonify, request
from flask_restful import reqparse, Resource
from src.com.twitter.service.tweet_service import get_tweets_by_criteria

tweet_controller = Blueprint(name="tweets", import_name=__name__)

parser = reqparse.RequestParser()
parser.add_argument('userId')


class TweetSearchResource(Resource):
    def get(self):
        search_criteria = parser.parse_args()
        return get_tweets_by_criteria(search_criteria)

