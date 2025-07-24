from datetime import datetime, timezone

from app.extensions import db
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def create_review(self, review_data):
        user = User.query.filter_by(id=review_data["user_id"]).first()
        place = Place.query.filter_by(id=review_data["place_id"]).first()

        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        review = Review(**review_data)
        db.session.add(review)
        db.session.commit()
        return review

    def get_review(self, review_id):
        return self.model.query.filter_by(id=review_id).first()

    def get_all_reviews(self):
        return self.model.query.all()

    def get_reviews_by_place(self, place_id):
        return self.model.query.filter_by(id=place_id)

    def update_review(self, review_id, review_data):
        review = self.model.query.filter_by(id=review_id).first()
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            try:
                review.rating = float(review_data['rating'])
            except ValueError:
                raise ValueError("Invalid rating value")
        if 'user_id' in review_data:
            user = User.query.filter_by(id=review_data['user_id']).first()
            if not user:
                raise ValueError("User not found")
            review.user = user
        if 'place_id' in review_data:
            place = Place.query.filter_by(id=review_data['place_id']).first()
            if not place:
                raise ValueError("Place not found")
            review.place = place

        review.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return review

    def get_review_by_user_and_place(self, user_id, place_id):
        return self.model.query.filter_by(user_id=user_id,
                                          place_id=place_id).first()

    def delete_review(self, review_id):
        review = self.model.query.filter_by(id=review_id).first()
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False
