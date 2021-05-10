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


@app_views.route("/users/<user_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id=None):
    """state"""
    willy = storage.get('User', user_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def post_user():
    """state"""
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is None:
        abort(400, 'Not a JSON')
    elif "email" not in willy.keys():
        abort(400, 'Missing email')
    elif "password" not in willy.keys():
        abort(400, 'Missing password')
    else:
        a = willy["password"]
        a = a.encode('utf-8')
        test = hashlib.md5(a).hexdigest()
        new_user = User(email=willy['email'],
                        password=test)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


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
