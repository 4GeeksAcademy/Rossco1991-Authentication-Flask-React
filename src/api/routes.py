"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['GET','POST'])
def sign_ups():
    data = request.json
    user = User.query.filter_by(email=data.get('email', None)).first()
    if user:
        return jsonify(message="User already exists"), 400
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return '', 204

@api.route('/login', methods=['GET','POST'])
def login():
      data = request.json
      user = User.query.filter_by(email=data.get('email', None)).first()

      if not user:
           return jsonify(message="Invalid username"), 401
      if user.password != data.get("password", None):
           return jsonify(message="Invalid password"), 401
      
      token= create_access_token(user.email)
      return jsonify(token=token)

@api.route('/private', methods=['GET'])
@jwt_required()
def secret_tunnel():
        user = User.query.filter_by('email').first()
        return jsonify(user)

