from flask import Blueprint, jsonify, request

auth_controller = Blueprint(name="auth", import_name=__name__)


@auth_controller.route('/login', methods=['GET'])
def login():
    output = {"msg": "Hello World !!"}
    return jsonify(output)