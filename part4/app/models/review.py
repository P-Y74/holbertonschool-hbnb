#!/usr/bin/python3
"""
Module defining BaseModel, Review, and PlaceNotFoundError classes.

This module provides:
- A base model class (`BaseModel`) that handles unique IDs and timestamps.
- A review class (`Review`) that represents a review for a place by a user,
  with validation of attributes.
- A custom exception (`PlaceNotFoundError`) for cases where a place is not
found.

Classes:
    BaseModel: Base class with ID and timestamp attributes and basic
    save/update methods.
    Review: Model representing a user review of a place, including rating
    and text.

Imports:
    uuid: For generating unique string IDs.
    datetime: For managing timestamps.
    app.models.place.Place: The Place model representing a location.
    app.models.user.User: The User model representing a user.

Usage example:
    place = Place()
    user = User(first_name="Alice", last_name="Doe",
    email="alice@example.com")
    review = Review(id="1234", place=place, user=user, rating=5,
    text="Great place!")
"""

from app.extensions import db
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .baseclass import BaseModel


class Review(BaseModel):
    """Represents a review for a place made by a user."""

    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='reviews')


    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5',
                        name='check_rating_range'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user': {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            }
        }
