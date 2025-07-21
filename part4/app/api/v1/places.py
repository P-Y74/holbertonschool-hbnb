"""
places.py - API namespace for managing Place resources in the HBnB
application.

This module defines the RESTful endpoints for performing operations
related to places, including creating, retrieving, and updating places.
It also defines the data models for request validation and API documentation
using Flask-RESTx.

Models:
    - PlaceAmenity: Represents an amenity associated with a place.
    - PlaceUser: Represents the owner of a place.
    - PlaceReview: Represents a user review of a place.
    - Place: Represents a place with its details, amenities, owner, and
    reviews.

Endpoints:
    - /places/ [GET, POST]
    - /places/<place_id> [GET, PUT]

Dependencies:
    - flask_restx
    - app.services.facade: Business logic layer for place operations.
"""
from app.models.place import Place
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})
# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True, description='Latitude of the place'
        ),
    'longitude': fields.Float(
        required=True, description='Longitude of the place'
        ),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(
        fields.Nested(amenity_model), description='List of amenities'
        ),
    'reviews': fields.List(
        fields.Nested(review_model), description='List of reviews'
        )
})


@api.route('/')
class PlaceList(Resource):
    """
    Resource class for handling the list of places.

    Methods:
        - GET: Retrieve all places.
        - POST: Create a new place.
    """
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        """
        Expects:
            JSON body matching the `Place` model.

        Returns:
            dict: The created place as a dictionary.
            int: HTTP status code.
        """
        data = api.payload
        if isinstance(data.get('owner_id'), dict):
            data['owner_id'] = data['owner_id'].get('id')
        data['owner_id'] = get_jwt_identity()
        required_fields = [
            'title', 'price', 'latitude', 'longitude'
            ]
        for field in required_fields:
            if field not in data or not data[field]:
                return {"message": f"{field} is required"}, 400
        try:
            place: Place = facade.create_place(data)
            return place.to_dict(), 201

        except ValueError:
            return {'error': 'Invalid input: please check your data'}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        """
        Returns:
            list: A list of dictionaries, each representing a place.
            int: HTTP status code.
        """
        places = facade.get_all_places()
        result = [place.to_dict() for place in places]
        return result, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource class for handling a single place by ID.

    Methods:
        - GET: Retrieve a place by ID.
        - PUT: Update a place by ID.
    """
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        """
        Get place details by ID.

        Args:
            place_id (str): Unique identifier of the place.

        Returns:
            dict: Place data if found.
            int: HTTP status code.
        """
        place = facade.get_place(place_id)
        if place is None:
            return {'message': 'Place not found'}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        data = api.payload
        if isinstance(data.get('owner_id'), dict):
            data['owner_id'] = data['owner_id'].get('id')
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        if place.owner.id != current_user_id:
            return {'message': 'Unauthorized action.'}, 403

        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'message': 'Place not found'}, 404
            return {
                "message": "Place updated successfully",
                "place": updated_place.to_dict()
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400
