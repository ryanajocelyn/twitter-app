from flask import Blueprint, jsonify, request
from flask_restful import Resource

auth_controller = Blueprint(name="auth", import_name=__name__)


class AuthResource(Resource):
    def get(self):
        output = {"msg": "Hello World !!"}
        return jsonify(output)
