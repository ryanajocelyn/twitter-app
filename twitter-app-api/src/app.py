"""
Flask Application
"""

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import sys

from src.com.twitter.controller.auth_controller import auth_controller, AuthResource
from src.com.twitter.controller.user_controller import user_controller, UserResource, TweetResource

app = Flask(__name__)


def add_api_bp(blueprint, prefix, resources):
    api = Api(blueprint)
    
    for resource, resource_path in resources:
        api.add_resource(resource, resource_path)

    app.register_blueprint(blueprint, url_prefix=prefix)


add_api_bp(auth_controller, '/api/v1/auth', [(AuthResource, '/login')])
add_api_bp(user_controller, '/api/v1/users', [(UserResource, '/user'), (TweetResource, '/tweets')])
