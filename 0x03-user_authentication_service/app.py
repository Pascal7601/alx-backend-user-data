#!/usr/bin/env python3
"""
a flask app
"""
from flask import (
        Flask, jsonify,
        request, abort,
        make_response, url_for, redirect
        )
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

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    define the login functionality
    when user logs in
    """
    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))

    response.set_cookie("session_id", session_id)
    
    return response

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    delete a session id of a user when they logout
    from the site
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)
        
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('home'))

@app.route('/profile', strict_slashes=False)
def profile():
    """
    get user profile which will be done
    when the user logs in is when they will be
    able to view their profile
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
