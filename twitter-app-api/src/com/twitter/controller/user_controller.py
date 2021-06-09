from flask import Blueprint, jsonify, request
from flask_restful import reqparse, Resource
from src.com.twitter.service.user_service import get_user_details_by_name, sync_tweets_by_id

user_controller = Blueprint(name="users", import_name=__name__)

parser = reqparse.RequestParser()
parser.add_argument('name')

twt_parser = reqparse.RequestParser()
twt_parser.add_argument('userId')


class UserResource(Resource):
    def get(self):
        args = parser.parse_args()
        print(args)
        return get_user_details_by_name(args['name'])


class TweetResource(Resource):
    def get(self):
        args = twt_parser.parse_args()
        print(args)
        return sync_tweets_by_id(args['userId'])

