from datetime import datetime, timezone

from app.extensions import db
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self, user_repository, amenity_repository, review_repository):
        super().__init__(Place)
        self.user_repository = user_repository
        self.amenity_repository = amenity_repository
        self.review_repository = review_repository

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        if isinstance(owner_id, dict):
            owner_id = owner_id.get('id')
        if not owner_id:
            raise ValueError("owner_id is required")

        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        try:
            price = float(place_data['price'])
            latitude = float(place_data['latitude'])
            longitude = float(place_data['longitude'])
        except (ValueError, KeyError):
            raise ValueError("Invalid numeric value for price,"
                             "latitude or longitude")
        try:
            new_place = Place(
                title=place_data['title'],
                description=place_data['description'],
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner=owner,
                owner_id=owner.id
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid place data: {str(e)}")

        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repository.get(amenity_id)
            if amenity:
                amenities.append(amenity)
        new_place.amenities = amenities

        review_ids = place_data.get('reviews', [])
        reviews = []
        for review_id in review_ids:
            review = self.review_repository.get(review_id)
            if review:
                reviews.append(review)
        new_place.reviews = reviews

        db.session.add(new_place)
        db.session.commit()
        return new_place

    def get_place(self, place_id):
        return self.model.query.filter_by(id=place_id).first()

    def get_all_places(self):
        return self.model.query.all()

    def update_place(self, place_id, place_data):
        place = self.model.query.filter_by(id=place_id).first()
        if not place:
            return None

        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            try:
                place.price = float(place_data['price'])
            except ValueError:
                raise ValueError("Invalid price value")
        if 'latitude' in place_data:
            try:
                place.latitude = float(place_data['latitude'])
            except ValueError:
                raise ValueError("Invalid latitude value")
        if 'longitude' in place_data:
            try:
                place.longitude = float(place_data['longitude'])
            except ValueError:
                raise ValueError("Invalid longitude value")

        if 'owner_id' in place_data:
            owner = self.user_repository.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner

        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities

        if 'reviews' in place_data:
            reviews = []
            for review_id in place_data['reviews']:
                review = self.review_repository.get(review_id)
                if review:
                    reviews.append(review)
            place.reviews = reviews

        place.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        return place

    def delete_place(self, place_id):
        place = self.model.query.filter_by(id=place_id).first()
        if place:
            db.session.delete(place)
            db.session.commit()
            return True
        return False
