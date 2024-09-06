#!/usr/bin/env python3
"""
create a session in a browser
"""

from .auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, abort
from flask import jsonify
from os import getenv


class SessionAuth(Auth):
    """
    class that creates a user session when logged in
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a new user session
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrieves user's sesson id from the session dict
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
    

    def current_user(self, request=None):
        """
        returns current user based on cookie value
        """
        
        if request is None:
            return None
        
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login_route():
    """
     login route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    
    if password is None:
        return jsonify({"error": "password missing"}), 400
    
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    
    user = users[0]
    
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password"}), 401
    
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    if session_id is None:
        abort(403)

    user_data = user.to_json()

    session_name = getenv("SESSION_NAME", "_my_session_id")
    response = jsonify(user_data)
    response.set_cookie(session_name, session_id)

    return response, 200


def destroy_session(self, request=None):
    """
    deletes a session when the user logs out
    """
    
    


