#!/usr/bin/python3
'''Contains the places_reviews view for the API.'''
from flask import request, jsonify
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

review_methods = ['GET', 'DELETE', 'PUT']


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=review_methods)
def handle_reviews(place_id=None, review_id=None):
    '''The method handler for the reviews endpoint.
    '''
    req_handlers = {
        'GET': get_reviews,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in req_handlers:
        return req_handlers[request.method](place_id, review_id)
    raise MethodNotAllowed(list(req_handlers.keys()))


def get_reviews(place_id=None, review_id=None):
    '''Gets the review with the given id or all reviews in
    the place with the given id.
    '''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            reviews = []
            for review in place.reviews:
                reviews.append(review.to_dict())
            return jsonify(reviews)
    elif review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
    raise NotFound()


def remove_review(place_id=None, review_id=None):
    '''Removes a review with the given id.
    '''
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_review(place_id=None, review_id=None):
    '''Adds a new review.
    '''
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    res = request.get_json()
    if 'user_id' not in res:
        raise BadRequest(description='Missing user_id')
    if type(res) is not dict:
        raise BadRequest(description='Not a JSON')
    user = storage.get(User, res['user_id'])
    if not user:
        raise NotFound()
    if 'text' not in res:
        raise BadRequest(description='Missing text')
    res['place_id'] = place_id
    new_review = Review(**res)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


def update_review(place_id=None, review_id=None):
    '''Updates the review with the given id.
    '''
    xkeys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            res = request.get_json()
            if type(res) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in res.items():
                if key not in xkeys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
    raise NotFound()
