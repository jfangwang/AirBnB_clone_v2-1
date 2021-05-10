#!/usr/bin/python3
"""City File"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from flask import request


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(place_id=None):
    """states"""
    willy = storage.get('Place', place_id)
    if willy is None:
        abort(404)
    review_dict = []
    for item in storage.all('Review').values():
        if item.place_id == place_id:
            review_dict.append(item.to_dict())
    return jsonify(review_dict)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_city(review_id=None):
    """state"""
    if storage.get('Review', review_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('Review', review_id).to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_city(review_id=None):
    """state"""
    willy = storage.get('Review', review_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'],
                 strict_slashes=False)
def post_city(place_id=None):
    """state"""
    willy2 = storage.get('Place', place_id)
    if willy2 is None:
        abort(404)
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is None:
        abort(400, 'Not a JSON')
    elif "user_id" not in willy.keys():
        abort(400, 'Missing user_id')
    elif "text" not in willy.keys():
        abort(400, 'Missing text')
    else:
        new_review = City(user_id=willy['user_id'], text=willy['text'])
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_city(review_id=None):
    """put/update state"""
    """ Request dict """
    city_store = storage.get(Review, review_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if city_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    if city_store is not None:
        abort(404)
    for key, val in dict_w.items():
        if key == 'user_id' or\
           key == 'place_id' or\
           key == 'id' or\
           key == 'created_at' or\
           key == 'updated_at':
            pass
        else:
                setattr(city_store, key, val)
                city_store.save()
                return jsonify(city_store.to_dict()), 200
