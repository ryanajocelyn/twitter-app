"""
Resource for User related operations
"""
from flask import Blueprint, jsonify, request
from flask_restful import reqparse, Resource
import logger

from src.app import app
from src.com.twitter.service.user_service import \
    get_user_details_by_name, \
    sync_tweets_by_id, \
    sync_timeline_by_id

user_controller = Blueprint(name="users", import_name=__name__)

parser = reqparse.RequestParser()
parser.add_argument('name')

twt_parser = reqparse.RequestParser()
twt_parser.add_argument('userId')
twt_parser.add_argument('userName')


class UserResource(Resource):
    """
        Get User details by screen name or user name
    """
    def get(self):
        args = parser.parse_args()
        print(args)
        return get_user_details_by_name(args['name'])


class TweetResource(Resource):
    """
        Get Tweets by User
    """
    def get(self):
        app.logger.info('Get Tweets By User..')
        args = twt_parser.parse_args()
        print(args)
        return sync_tweets_by_id(args['userId'])


class UserTimelineResource(Resource):
    """
    Get Timeline Information by User
    """
    def get(self):
        app.logger.info('Get Timeline By User..')
        args = twt_parser.parse_args()
        print(args)

        return sync_timeline_by_id(args['userId'], args['userName'])
