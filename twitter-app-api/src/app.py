"""
Flask Application
"""

import sys
import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("src.config.ProductionConfig")
else:
    app.config.from_object("src.config.DevelopmentConfig")

db = SQLAlchemy(app)

from src.com.twitter.controller.auth_controller import auth_controller, AuthResource
from src.com.twitter.controller.user_controller import user_controller, UserResource, TweetResource
from src.com.twitter.controller.tweet_controller import tweet_controller, TweetSearchResource


def add_api_bp(blueprint, prefix, resources):
    api = Api(blueprint)
    
    for resource, resource_path in resources:
        api.add_resource(resource, resource_path)

    app.register_blueprint(blueprint, url_prefix=prefix)


add_api_bp(auth_controller, '/api/v1/auth', [(AuthResource, '/login')])
add_api_bp(user_controller, '/api/v1/users', [(UserResource, '/user'), (TweetResource, '/sync/tweets')])
add_api_bp(tweet_controller, '/api/v1/tweets', [(TweetSearchResource, '/search')])
