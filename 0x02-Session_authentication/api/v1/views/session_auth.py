#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login():
    """ POST /api/v1/auth_session/login
    Handle session login for a user
    """
    user_email = request.form.get("email")
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get("password")
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": user_email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    user_dict = user.to_json()
    response = make_response(jsonify(user_dict))

    session_name = os.getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route(
        "auth_session/logout",
        methods=["DELETE"],
        strict_slashes=False
                 )
def session_logout():
    """ DELETE /api/v1/auth_session/logout
    Handle session logout for a user
    """
    from api.v1.app import auth
    session_destroyed = auth.destroy_session(request)
    if not session_destroyed:
        abort(404)

    return jsonify({}), 200
