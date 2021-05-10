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


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id=None):
    """states"""
    willy = storage.get('City', city_id)
    if willy is None:
        abort(404)
    places_dict = []
    for item in storage.all('Place').values():
        # print("--------------------------------------------")
        # print(storage.all().get('City', state_id))
        # print(item.state_id)
        # print("--------------------------------------------")
        if item.city_id == city_id:
            places_dict.append(item.to_dict())
    return jsonify(places_dict)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """state"""
    if storage.get('Place', place_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('Place', place_id).to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id=None):
    """state"""
    willy = storage.get('Place', place_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """state"""
    willy2 = storage.get('City', city_id)
    if willy2 is None:
        abort(404)
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is None:
        abort(400, 'Not a JSON')
    elif "name" not in willy.keys():
        abort(400, 'Missing name')
    elif "user_id" not in willy.keys():
        abort(400, 'Missing user_id')
    else:
        willy3 = storage.get('User', willy['user_id'])
        if willy3 is None:
            abort(404)
        new_city = Place(name=willy['name'], city_id=city_id,
                         user_id=willy['user_id'])
        # new_city = City(state_id=state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """put/update state"""
    """ Request dict """
    place_store = storage.get(Place, place_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if place_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    for key, val in dict_w.items():
        if key == 'city_id' or\
           key == 'user_id' or\
           key == 'id' or\
           key == 'created_at' or\
           key == 'updated_at':
            pass
        else:
            if place_store is not None:
                setattr(place_store, key, val)
                place_store.save()
                return jsonify(place_store.to_dict()), 200
    abort(404)
