"""
Flask Application
"""

import sys
import os
import logging

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("src.config.ProductionConfig")
else:
    app.config.from_object("src.config.DevelopmentConfig")

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)
app.logger.addHandler(s_handler)
app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)

from src.com.twitter.controller.auth_controller import \
    auth_controller, \
    TwitterAuthResource, \
    TwitterCallbackResource, \
    TwitterRequestTokenResource, \
    TwitterAccessTokenResource, \
    TwitterProfileResource

from src.com.twitter.controller.user_controller import \
    user_controller, \
    UserResource, \
    TweetResource, \
    UserTimelineResource

from src.com.twitter.controller.tweet_controller import tweet_controller, TweetSearchResource

from src.com.twitter.test_twitter import TwitterAuthenticate, TwitterCallback


def add_api_bp(blueprint, prefix, resources):
    api = Api(blueprint)
    
    for resource, resource_path in resources:
        api.add_resource(resource, resource_path)

    app.register_blueprint(blueprint, url_prefix=prefix)


add_api_bp(auth_controller, '/api/v1/twitter',
           [(TwitterRequestTokenResource, '/oauth/request_token'),
            (TwitterAccessTokenResource, '/oauth/access_token'),
            (TwitterProfileResource, '/users/profile_banner'),
            (TwitterAuthResource, '/login'),
            (TwitterCallbackResource, '/callback')])
add_api_bp(user_controller, '/api/v1/users', [(UserResource, '/user'),
                                              (TweetResource, '/sync/tweets'),
                                              (UserTimelineResource, '/sync/timeline')])
add_api_bp(tweet_controller, '/api/v1/tweets', [(TweetSearchResource, '/search')])

# Initialize Our RESTful API
# api_tw = Api(app)
#
# api_tw.add_resource(TwitterAuthenticate, '/authenticate/twitter')
# api_tw.add_resource(TwitterCallback, '/callback1/twitter')
