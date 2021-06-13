"""
Flask Application Main

Entry point for the flask application defines the key configurations like

    1. Configuration based on environment
    2. Application Logger
    3. Database Connections
    4. Api Blueprints and Routes
"""

import sys
import os
import logging

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration based on application environment
if app.config["ENV"] == "production":
    app.config.from_object("src.config.ProductionConfig")
else:
    app.config.from_object("src.config.DevelopmentConfig")

# Logger Configuration
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)
app.logger.addHandler(s_handler)
app.logger.setLevel(logging.DEBUG)

# Database Configuration
db = SQLAlchemy(app)

# Blueprints and API Routes
from src.com.twitter.controller.auth_controller import \
    auth_controller, \
    TwitterRequestTokenResource, \
    TwitterAccessTokenResource, \
    TwitterProfileResource, \
    TwitterLogoutResource

from src.com.twitter.controller.user_controller import \
    user_controller, \
    UserResource, \
    TweetResource, \
    UserTimelineResource

from src.com.twitter.controller.tweet_controller import tweet_controller, TweetSearchResource


def add_api_bp(blueprint, prefix, resources):
    """
    Common method to register the Blueprint for each resource

    :param blueprint:
    :param prefix:
    :param resources:
    :return:
    """
    api = Api(blueprint)
    
    for resource, resource_path in resources:
        api.add_resource(resource, resource_path)

    app.register_blueprint(blueprint, url_prefix=prefix)


# Register Blueprints
add_api_bp(auth_controller, '/v1/twitter',
           [(TwitterRequestTokenResource, '/oauth/request_token'),
            (TwitterAccessTokenResource, '/oauth/access_token'),
            (TwitterProfileResource, '/users/profile_banner'),
            (TwitterLogoutResource, '/logout')])

add_api_bp(user_controller, '/v1/users', [(UserResource, '/user'),
                                          (TweetResource, '/sync/tweets'),
                                          (UserTimelineResource, '/sync/timeline')])

add_api_bp(tweet_controller, '/v1/tweets', [(TweetSearchResource, '/search')])
