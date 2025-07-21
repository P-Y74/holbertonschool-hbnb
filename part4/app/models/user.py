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

import re

from app.extensions import bcrypt, db
from app.models.place import Place
from app.models.review import Review
from sqlalchemy.orm import relationship

from .baseclass import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
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

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', back_populates="owner", lazy=True)
    reviews = relationship('Review', backref='user', lazy=True)

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

    def to_dict(self):
        """
        Converts the User object into a dictionary, useful for JSON serialization.

        Returns:
            dict: Dictionary representation of the user.
        """

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
