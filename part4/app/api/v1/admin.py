from app.services import facade
from app.models.user import User
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('admin', description='Admin operations')


@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        if not user_data:
            return {'error': 'Invalid or missing JSON data'}, 400
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500

        return {'id': new_user.id,
                'message': 'User successfully registered'}, 201


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        if not data:
             return {'error': 'Invalid or missing JSON data'}, 400

        email = data.get('email')
        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and str(existing_user.id) != str(user_id):
                return {'error': 'Email already in use'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if 'password' in data:
            password = data['password']
            user.hash_password(password)
            data.pop('password')

        updated_user = facade.put_user(user_id, data)
        if not updated_user:
            return {'error': 'Update failed'}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        if not amenity_data:
            return {'error': 'Invalid or missing JSON data'}, 400

        try:
            name = amenity_data['name'].strip()
            if not name:
                return {"message": "Name is required"}, 400

            amenity = facade.create_amenity({'name': name})

            return amenity.to_dict(), 201

        except ValueError:
            return {'error': 'Invalid input: please check your data.'}, 400


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        if not amenity_data:
            return {'error': 'Invalid or missing JSON data'}, 400

        if 'name' not in amenity_data or not amenity_data['name'].strip():
            return {'message': 'Name is required'}, 400
        name = amenity_data['name'].strip()
        update_amenity = facade.update_amenity(amenity_id, {'name': name})
        if update_amenity is None:
            return {'message': 'Amenity not found'}, 404
        return update_amenity.to_dict(), 200


@api.route('/places/<place_id>')
class AdminPlaceRessource(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place_data = request.json
        if not place_data:
            return {'error': 'Invalid or missing JSON data'}, 400
        if isinstance(place_data.get('owner_id'), dict):
            place_data['owner_id'] = place_data['owner_id'].get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'message': 'Unauthorized action.'}, 403

        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'message': 'Place not found'}, 404
            return {
                "message": "Place updated successfully",
                "place": updated_place.to_dict()
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    def delete(self, place_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'message': 'Unauthorized action.'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200


@api.route('/<review_id>')
class AdminReviewRessource(Resource):
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review_data = request.json
        if not review_data:
            return {'error': 'Invalid or missing JSON data'}, 400
        if isinstance(review_data.get('owner_id'), dict):
            review_data['owner_id'] = review_data['owner_id'].get('id')

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        if not is_admin and review.owner_id != user_id:
            return {'message': 'Unauthorized action.'}, 403

        update_review = facade.update_review(review_id, review_data)

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
    def delete(self, review_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        if not is_admin and review.owner_id != user_id:
            return {'message': 'Unauthorized action.'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
