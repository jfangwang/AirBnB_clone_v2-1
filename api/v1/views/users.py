#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import hashlib
from flask import request


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """All users"""
    states_dict = []
    for item in storage.all('User').values():
        states_dict.append(item.to_dict())
    return jsonify(states_dict)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """User"""
    if storage.get('User', user_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('User', user_id).to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"], strict_slashes=False)
def user_delete(user_id=None):
    """deletes a user object"""
    userobj = storage.get(User, user_id)
    if userobj is None:
        abort(404)
    storage.delete(userobj)
    userobj.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def user_create():
    """creates a user object"""
    try:
        body_dict = request.get_json()
        if body_dict is None:
            abort(400, "Not a JSON")
    except Exception:
        abort(400, "Not a JSON")
    if "email" not in body_dict.keys():
        abort(400, "Missing email")
    if "password" not in body_dict.keys():
        abort(400, "Missing password")
    userobj = User(**body_dict)
    userobj.save()
    return jsonify(userobj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def user_update(user_id):
    """updates existing user object"""
    userobj = storage.get(User, user_id)
    if userobj is None:
        abort(404)
    try:
        body_dict = request.get_json()
    except:
        abort(400, "Not a JSON")
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("email", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(userobj, key, value)
    userobj.save()
    return jsonify(userobj.to_dict()), 200
