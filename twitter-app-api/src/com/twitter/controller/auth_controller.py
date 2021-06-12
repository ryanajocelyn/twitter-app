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
        userid = res_split[2].split('=')[1]
        username = res_split[3].split('=')[1]

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


class TwitterAuthResource(Resource):
    # Here we are making it so this endpoint accepts GET requests
    def get(self):
        app.logger.info('Authenticating..')

        # We must generate our signed OAuth Headers
        uri, headers, body = oauth.sign('https://twitter.com/oauth/request_token')
        # We need to make a request to twitter with the OAuth parameters we just created
        res = requests.get(uri, headers=headers, data=body)
        # This returns a string with OAuth variables we need to parse
        res_split = res.text.split('&')  # Splitting between the two params sent back
        oauth_token = res_split[0].split('=')[1]  # Pulling our APPS OAuth token from the response.
        # Now we have to redirect to the login URL using our OAuth Token

        return redirect('https://api.twitter.com/oauth/authenticate?oauth_token=' + oauth_token, 302)


# We need to create a parser for that callback URL
def callback_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token')
    parser.add_argument('oauth_token_secret')
    parser.add_argument('oauth_verifier')
    return parser


# Now we setup the Resource for the callback
class TwitterCallbackResource(Resource):
    def get(self):
        parser = callback_parser()
        args = parser.parse_args() # Parse our args into a dict

        # We need to make a request to twitter with this callback OAuth token
        res = requests.post('https://api.twitter.com/oauth/access_token?oauth_token=' + args['oauth_token'] + '&oauth_verifier=' + args['oauth_verifier'])
        res_split = res.text.split('&')

        # Now we need to parse our oauth token and secret from the response
        oauth_token = res_split[0].split('=')[1]
        oauth_secret = res_split[1].split('=')[1]
        userid = res_split[2].split('=')[1]
        username = res_split[3].split('=')[1]

        return redirect('http://localhost:3000', 302)


class TwitterLogoutResource(Resource):
    def post(self):
        app.logger.info('OAuth: Logout Resource..')

        @after_this_request
        def delete_oauth_token_cookie(response):
            response.delete_cookie('oauth_token')
            return response

        return {'success': True}
