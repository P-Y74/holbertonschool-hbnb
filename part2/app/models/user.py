#!/usr/bin/python3
"""
User and BaseModel module.

This module defines the BaseModel class which provides common attributes
and methods
for models, and the User class which represents a user with personal
information,
including validation and management of related places and reviews.

Classes:
    BaseModel: Base class with unique ID and timestamp management.
    User: Represents a user with first name, last name, email, admin status,
    and related places and reviews.

Dependencies:
    uuid: For generating unique identifiers.
    re: For validating email addresses.
    datetime: For managing creation and update timestamps.
    app.models.place.Place: Represents places associated with a user.
    app.models.review.Review: Represents reviews associated with a user.
"""

import uuid
import re
from datetime import datetime
from app.models.place import Place
from app.models.review import Review


class BaseModel:
    """
    BaseModel class that provides common attributes and methods for other
    models.

    Attributes:
        id (str): Unique identifier for the instance, generated as a UUID4
        string.
        created_at (datetime): Timestamp when the instance was created.
        updated_at (datetime): Timestamp when the instance was last updated.
    """

    def __init__(self, id=None, created_at=None, updated_at=None):
        """
        Initialize a new BaseModel instance.

        Args:
            id (str, optional): Unique identifier. If None, a new UUID4 string
            is generated.
            created_at (datetime, optional): Creation timestamp. If None,
            current datetime is used.
            updated_at (datetime, optional): Last update timestamp. If None,
            current datetime is used.
        """
        self.id = id if id else str(uuid.uuid4())
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def save(self):
        """
        Update the `updated_at` timestamp to the current datetime.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update attributes of the instance based on a dictionary and save
        changes.

        Args:
            data (dict): Dictionary of attribute names and values to
            update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class User(BaseModel):
    """
    User class representing a user with personal details and related places
    and reviews.

    Attributes:
        first_name (str): First name of the user, max length 50.
        last_name (str): Last name of the user, max length 50.
        email (str): Valid email address of the user.
        is_admin (bool): Whether the user has admin privileges.
        places (list): List of Place instances related to the user.
        reviews (list): List of Review instances related to the user.
    """

    def __init__(self, first_name, last_name, email, is_admin=False, id=None,
                 created_at=None, updated_at=None):
        """
        Initialize a new User instance.

        Args:
            first_name (str): User's first name. Must be a string with max 50
            characters.
            last_name (str): User's last name. Must be a string with max 50
            characters.
            email (str): User's email address. Must be a valid email string.
            is_admin (bool, optional): Admin status. Defaults to False.
            id (str, optional): Unique identifier. If None, a new UUID4 string
            is generated.
            created_at (datetime, optional): Creation timestamp. Defaults
            to now if None.
            updated_at (datetime, optional): Last update timestamp. Defaults
            to now if None.

        Raises:
            TypeError: If any argument is of incorrect type.
            ValueError: If first_name or last_name exceed 50 characters or
            email is invalid.
        """
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be a boolean")
        self.is_admin = is_admin

        if not isinstance(first_name, str):
            raise TypeError("first_name must be a string")
        if len(first_name) > 50:
            raise ValueError(
                "first_name must contain a maximum of 50"
                "characters"
            )
        self.first_name = first_name

        if not isinstance(last_name, str):
            raise TypeError("last_name must be a string")
        if len(last_name) > 50:
            raise ValueError(
                "last_name must contain a maximum of 50"
                "characters"
            )
        self.last_name = last_name

        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if not self.is_email_valid(email):
            raise ValueError("invalid email format")
        self.email = email

        self.places = []
        self.reviews = []

    def is_email_valid(self, email):
        """
        Validate the format of an email address using a regular expression.

        Args:
            email (str): Email address to validate.

        Returns:
            bool: True if email is valid, False otherwise.
        """
        pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
                   r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")

        return re.match(pattern, email) is not None

    def new_place(self, place):
        """
        Add a Place instance to the user's places list.

        Args:
            place (Place): Place instance to add.
        """
        self.places.append(place)

    def new_review(self, review):
        """
        Add a Review instance to the user's reviews list.

        Args:
            review (Review): Review instance to add.
        """
        self.reviews.append(review)

    def to_dict(self):
        """
        Convertit l'objet User en dictionnaire, utile pour le JSON.

        Returns:
            dict: Représentation dictionnaire de l'utilisateur.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
