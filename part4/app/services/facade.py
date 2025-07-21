from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.services.repositories.user_repository import UserRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository


class HBnBFacade:
    def __init__(self):
        self.user_repository = UserRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()
        self.place_repository = PlaceRepository(
            self.user_repository,
            self.amenity_repository,
            self.review_repository
        )

    def create_place(self, place_data):
        return self.place_repository.create_place(place_data)

    def get_place(self, place_id):
        return self.place_repository.get_place(place_id)

    def get_all_places(self):
        return self.place_repository.get_all_places()

    def update_place(self, place_id, place_data):
        return self.place_repository.update_place(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repository.delete_place(place_id)

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def put_user(self, user_id, new_data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(new_data)
        return user

    def get_all_user(self):
        return self.user_repository.get_all_user()

    def create_amenity(self, amenity_data):
        return self.amenity_repository.create_amenity(amenity_data)

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get_amenity(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all_amenities()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repository.update_amenity(amenity_id, amenity_data)

    def create_review(self, review_data):
        return self.review_repository.create_review(review_data)

    def get_review(self, review_id):
        return self.review_repository.get_review(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all_reviews()

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_reviews_by_place(place_id)

    def update_review(self, review_id, review_data):
        return self.review_repository.update_review(review_id, review_data)

    def get_review_by_user_and_place(self, user_id, place_id):
        return self.review_repository.get_review_by_user_and_place(
            user_id, place_id)

    def delete_review(self, review_id):
        return self.review_repository.delete_review(review_id)
