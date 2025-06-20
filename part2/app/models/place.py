#!/usr/bin/python3
"""
Place module.

This module defines two classes: BaseModel and Place.
- BaseModel provides basic ID and timestamp functionality.
- Place represents a rental place, with validations on title, price,
  location, and relationships with amenities and reviews.
"""

import uuid
from datetime import datetime

from app.models.amenity import Amenity
from app.models.review import Review
from app.models.user import User


class BaseModel:
    """
    Base model class providing ID, created_at, and updated_at fields.

    Attributes:
        id (str): Unique identifier.
        created_at (datetime): Timestamp of instance creation.
        updated_at (datetime): Timestamp of last update.
    """

    def __init__(self, id, created_at, updated_at):
        """
        Initializes the base model with ID and timestamps.

        Args:
            id (str): UUID string. If None, generates a new UUID.
            created_at (datetime): Creation time. Defaults to now if None.
            updated_at (datetime): Last update time. Defaults to now if None.
        """
        self.id = id if id else str(uuid.uuid4())
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def save(self):
        """
        Updates the `updated_at` timestamp to the current time.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Updates instance attributes using a dictionary of key-value pairs.

        Args:
            data (dict): Dictionary of attributes to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


class Place(BaseModel):
    """
    Represents a place available for rental.

    Inherits from BaseModel and adds fields such as title, description,
    price, coordinates, and related amenities and reviews.

    Attributes:
        owner (User): The user who owns the place.
        title (str): Title of the place (max 100 characters).
        description (str): Optional description.
        price (float): Price per night (must be positive).
        latitude (float): Latitude coordinate (-90.0 to 90.0).
        longitude (float): Longitude coordinate (-180.0 to 180.0).
        amenities (list): List of associated Amenity objects.
        reviews (list): List of associated Review objects.
    """

    def __init__(self, id, owner, title, description, price, latitude,
                 longitude, created_at, updated_at):
        """
        Initializes a Place instance with full validation.

        Args:
            id (str): UUID of the place.
            owner (User): User instance representing the owner.
            title (str): Title of the place.
            description (str): Optional description.
            price (float): Price per night.
            latitude (float): Latitude coordinate.
            longitude (float): Longitude coordinate.
            created_at (datetime): Creation time.
            updated_at (datetime): Last update time.

        Raises:
            TypeError: If any argument is of the wrong type.
            ValueError: If constraints (length/range) are violated.
        """
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        self.owner = owner

        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if len(title) > 100:
            raise ValueError("title must contain a maximum of 100"
                             "characters")
        self.title = title

        if description is not None and not isinstance(description, str):
            raise TypeError("description must be a string")
        self.description = description

        if not isinstance(price, float):
            raise TypeError("price must be a positive number")
        if price < 0:
            raise ValueError("price must be superior to 0")
        self.price = round(price, 2)

        if not isinstance(latitude, float):
            raise TypeError("latitude must be a number")
        if not -90 <= latitude <= 90:
            raise ValueError(
                "latitude must be within the range of -90.0 to 90.0")
        self.latitude = round(latitude, 1)

        if not isinstance(longitude, float):
            raise TypeError("longitude must be a number")
        if not -180 <= longitude <= 180:
            raise ValueError(
                "longitude must be within the range of -180.0 to 180.0")
        self.longitude = round(longitude, 1)

        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity):
        """
        Adds an Amenity object to the list of amenities.

        Args:
            amenity (Amenity): The amenity to add.
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """
        Adds a Review object to the list of reviews.

        Args:
            review (Review): The review to add.
        """
        self.reviews.append(review)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "owner_id": self.owner.id if self.owner else None,
            "owner": self.owner.to_dict() if self.owner else None,
            "amenities": [amenity.to_dict() for amenity in getattr(self, "amenities", [])],
            "reviews": [review.to_dict() for review in getattr(self, "reviews", [])]
        }


