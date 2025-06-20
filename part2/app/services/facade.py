import uuid
from datetime import datetime, timezone

from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("owner_id is required")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        try:
            price = float(place_data['price'])
            latitude = float(place_data['latitude'])
            longitude = float(place_data['longitude'])
        except (ValueError, KeyError):
            raise ValueError("Invalid numeric value for price, latitude or longitude")
        try:
            new_place = Place(
                id=None,
                owner=owner,
                title=place_data['title'],
                description=place_data.get('description'),
                price=price,
                latitude=latitude,
                longitude=longitude,
                created_at=None,
                updated_at=None
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid place data: {str(e)}")

        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                new_place.add_amenity(amenity)

        review_ids = place_data.get('reviews', [])
        for review_id in review_ids:
            review = self.review_repo.get(review_id)
            if review:
                new_place.add_review(review)

        self.place_repo.add(new_place)
        return new_place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
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
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner

        if 'amenities' in place_data:
            place.amenities.clear()
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        if 'reviews' in place_data:
            place.reviews.clear()
            for review_id in place_data['reviews']:
                review = self.review_repo.get(review_id)
                if review:
                    place.add_review(review)

        place.updated_at = datetime.now(timezone.utc)
        return place

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def put_user(self, user_id, new_data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(new_data)
        return user


    def get_all_user(self):
        return self.user_repo.get_all()

    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        if not name or not isinstance(name, str):
            raise ValueError("Name is required")
        new_amenity = Amenity(
            id=str(uuid.uuid4()),
            name=name,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
            )
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            return None
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            return None
        name = amenity_data.get('name')
        if not name:
            raise ValueError('Name invalid')
        amenity.name = name
        amenity.updated_at = datetime.now(timezone.utc)
        return amenity

    def create_review(self, review_data):
        user = self.get_user(review_data["user_id"])
        place = self.get_place(review_data["place_id"])
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get(place_id)

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
       review = self.review_repo.get(review_id)
       return self.review_repo.delete(review)
