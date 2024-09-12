#!/usr/bin/env python3
"""
a flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """
    route to add a user to a db
    """
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        return jsonify({"message": "please provide username and pass"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
