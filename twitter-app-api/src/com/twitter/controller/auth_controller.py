"""
Authentication related API Routes
"""
from flask import Blueprint, Flask, jsonify, request, redirect, after_this_request
from flask_restful import Api, Resource, reqparse
from requests_oauthlib.oauth1_auth import Client
from twitter import *

import requests
import logger
import json

from src.app import app

auth_controller = Blueprint(name="auth", import_name=__name__)


class TwitterRequestTokenResource(Resource):
    """
    Resource to fetch the Request Token from Twitter
    """
    def post(self):
        app.logger.info('OAuth: Request Token Resource..')

        oauth = Client(app.config['TWITTER_CONSUMER_KEY'], client_secret=app.config['TWITTER_CONSUMER_SECRET'])
        uri, headers, body = oauth.sign('https://twitter.com/oauth/request_token')

        res = requests.get(uri, headers=headers, data=body)
        res_split = res.text.split('&')
        oauth_token = res_split[0].split('=')[1]
        oauth_token_secret = res_split[1].split('=')[1]

        res_data = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }

        @after_this_request
        def set_oauth_token_cookie(response):
            response.set_cookie('oauth_token', json.dumps(res_data), max_age=64800, httponly=True)
            return response

        return res_data


class TwitterAccessTokenResource(Resource):
    """
        Resource to fetch the Access Token from Twitter
    """
    def post(self):
        app.logger.info('OAuth: Access Token Resource..')

        parser = callback_parser()
        args = parser.parse_args()

        oauth_token = json.loads(request.cookies.get('oauth_token'))
        oauth = Client(app.config['TWITTER_CONSUMER_KEY'],
                       client_secret=app.config['TWITTER_CONSUMER_SECRET'],
                       resource_owner_key=args['oauth_token'],
                       resource_owner_secret=oauth_token['oauth_token_secret'],
                       verifier=args['oauth_verifier'])
        uri, headers, body = oauth.sign('https://api.twitter.com/oauth/access_token')

        res = requests.post(uri, headers=headers, data=body)
        app.logger.info('Access Response=' + res.text)
        res_split = res.text.split('&')
        oauth_token = res_split[0].split('=')[1]
        oauth_secret = res_split[1].split('=')[1]

        res_data = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_secret
        }

        @after_this_request
        def set_oauth_token_cookie(response):
            response.set_cookie('oauth_token', json.dumps(res_data), max_age=64800, httponly=True)
            return response

        return {
            'success': True
        }


class TwitterProfileResource(Resource):
    """
        Resource to fetch the User Profile Information from Twitter
    """
    def get(self):
        app.logger.info('OAuth: Request User Profile..')

        oauth_cookie = request.cookies.get('oauth_token')
        if oauth_cookie is not None:
            oauth_token = json.loads(oauth_cookie)
            oauth = Client(app.config['TWITTER_CONSUMER_KEY'],
                           client_secret=app.config['TWITTER_CONSUMER_SECRET'],
                           resource_owner_key=oauth_token['oauth_token'],
                           resource_owner_secret=oauth_token['oauth_token_secret'])
            uri, headers, body = oauth.sign('https://api.twitter.com/1.1/account/verify_credentials.json')
            res = requests.get(uri, headers=headers, data=body)

            return res.json()

        return None


# We need to create a parser for that callback URL
def callback_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token')
    parser.add_argument('oauth_token_secret')
    parser.add_argument('oauth_verifier')
    return parser


class TwitterLogoutResource(Resource):
    """
        Resource to process the application logout
    """
    def post(self):
        app.logger.info('OAuth: Logout Resource..')

        @after_this_request
        def delete_oauth_token_cookie(response):
            response.delete_cookie('oauth_token')
            return response

        return {'success': True}
