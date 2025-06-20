"""
Amenity API endpoints using Flask-RESTx.

This module defines RESTful API endpoints for managing "amenities"
(e.g., features of a property)
via HTTP methods (GET, POST, PUT). It uses a service facade to handle
business logic and data access.

Routes:
    - /amenities/         [GET, POST]: List all amenities or create a
    new one.
    - /amenities/<id>     [GET, PUT] : Get or update a specific amenity
    by ID.

Models:
    - Amenity: Defines the expected structure of an amenity object
    with a required 'name' field.

Functions:
    - post(): Create a new amenity.
    - get(): Retrieve all amenities.
    - get(amenity_id): Get details of a specific amenity.
    - put(amenity_id): Update the name of a specific amenity.

Dependencies:
    - Flask
    - Flask-RESTx
    - app.services.facade: Handles business logic (create, retrieve,
    update amenities).

Error Handling:
    - Returns appropriate HTTP status codes and messages for invalid
    input or missing resources.
"""
from flask import request
from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """
    Resource for creating and listing amenities.

    Methods:
        - POST: Create a new amenity.
        - GET: Retrieve all amenities.
    """
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity.

        Returns:
            Tuple (dict, int): JSON response with created amenity and
            status code 201,
                               or error message with status code 400.
        """
        data = api.payload
        try:
            name = data['name'].strip()
            if not name:
                return {"message": "Name is required"}, 400

            amenity = facade.create_amenity({'name': name})

            return amenity.to_dict(), 201

        except ValueError:
            return {'error': 'Invalid input: please check your data.'}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve all amenities.

        Returns:
            Tuple (list, int): A list of amenity dictionaries and HTTP
            tatus code 200.
        """
        amenities = facade.get_all_amenities()
        result = [amenity.to_dict() for amenity in amenities]
        return result, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource for retrieving and updating a specific amenity by ID.

    Methods:
        - GET: Retrieve an amenity by its ID.
        - PUT: Update an existing amenity's information.
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get details of a specific amenity by ID.

        Args:
            amenity_id (str): The ID of the amenity to retrieve.

        Returns:
            Tuple (dict, int): Amenity data and status code 200, or error
            message with status 404.
        """
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {'message': 'Amenty not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update the name of an existing amenity.

        Args:
            amenity_id (str): The ID of the amenity to update.

        Returns:
            Tuple (dict, int): Updated amenity data and status code 200,
                               or error message with status 400 or 404.
        """
        data = api.payload
        if 'name' not in data or not data['name'].strip():
            return {'message': 'Name is required'}, 400
        name = data['name'].strip()
        update_amenity = facade.update_amenity(amenity_id, {'name': name})
        if update_amenity is None:
            return {'message': 'Amenity not found'}, 404
        return update_amenity.to_dict(), 200
