"""
Flask Application
"""

from flask import Flask, jsonify
import sys

from src.com.twitter.controller.auth_controller import auth_controller

app = Flask(__name__)

app.register_blueprint(auth_controller, url_prefix="/api/v1/auth")
