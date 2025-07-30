"""
Module reviews.py
------------------

This module defines the RESTful API endpoints related to reviews in the
application.
It uses Flask-RESTx to structure the API namespace, models, and resources.

Endpoints:
    - POST /reviews/: Create a new review
    - GET /reviews/: List all reviews
    - GET /reviews/<review_id>: Get a specific review by ID
    - PUT /reviews/<review_id>: Update a review
    - DELETE /reviews/<review_id>: Delete a review
    - GET /reviews/places/<place_id>/reviews: Get all reviews for a
    specific place

Dependencies:
    - Flask
    - Flask-RESTx
    - app.services.facade (acts as a service layer abstraction)

Author:
    Your Name (or team/project name)

"""
from app.services import facade
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('', strict_slashes=False)
class ReviewList(Resource):
    """
    Handles HTTP requests for creating and retrieving reviews.

    Methods:
        post(): Create a new review and return its data.
        get(): Retrieve a list of all existing reviews.
    """
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new review.

        Expects:
            JSON body matching the review_model schema.

        Returns:
            Tuple: A JSON object with the new review's data and HTTP 201
            status code.

        Responses:
            201: Review successfully created.
            400: Invalid input data.
        """
        user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = user['id']
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner.id == user['id']:
            return {'error': 'You cannot review your own place.'}, 403
        existing_review = facade.get_review_by_user_and_place(user['id'], review_data['place_id'])
        if existing_review:
            return {'error': 'You have already reviewed this place.'}, 400
        new_review = facade.create_review(review_data)

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id,
            'created_at': new_review.created_at.isoformat(),
            'updated_at': new_review.updated_at.isoformat()
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve all reviews.

        Returns:
            Tuple: A list of reviews and HTTP 200 status code.

        Responses:
            200: List of reviews retrieved successfully.
        """
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Handles operations on a single review resource by ID.

    Methods:
        get(review_id): Retrieve a specific review.
        put(review_id): Update a specific review.
        delete(review_id): Delete a specific review.
    """
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get a review by its ID.

        Args:
            review_id (str): The ID of the review.

        Returns:
            Tuple: JSON representation of the review and HTTP 200 status,
            or 404 if not found.

        Responses:
            200: Review found and returned.
            404: Review not found.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update an existing review.

        Args:
            review_id (str): The ID of the review to update.

        Expects:
            JSON body with updated fields.

        Returns:
            Tuple: Updated review data and HTTP status.

        Responses:
            200: Review updated successfully.
            400: Invalid input or update failed.
            404: Review not found.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        user = get_jwt_identity()
        if review.user_id != user['id']:
            return {'error': 'Unauthorized action.'}, 403

        data = request.get_json()
        update_review = facade.update_review(review_id, data)

        if not update_review:
            return {'error': 'Update failed'}, 400

        return {
            'id': update_review.id,
            'text': update_review.text,
            'rating': update_review.rating,
            'user_id': update_review.user_id,
            'place_id': update_review.place_id,
            'created_at': update_review.created_at.isoformat(),
            'updated_at': update_review.updated_at.isoformat()
        }, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review by its ID.

        Args:
            review_id (str): The ID of the review to delete.

        Returns:
            Tuple: Confirmation message and HTTP 200 status or 404 if
            not found.

        Responses:
            200: Review deleted successfully.
            404: Review not found.
        """
        user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user_id != user['id']:
            return {'error': 'Unauthorized action.'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Handles retrieval of reviews related to a specific place.

    Methods:
        get(place_id): Retrieve all reviews for a given place.
    """
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.

        Args:
            place_id (str): The ID of the place.

        Returns:
            Tuple: A list of reviews for the given place and HTTP 200
            status code.

        Responses:
            200: List of reviews returned.
            404: Place not found.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = [review for review in facade.get_all_reviews()
                   if review.place_id == place_id]
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        } for review in reviews], 200
