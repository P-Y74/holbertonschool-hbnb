#!/usr/bin/python3
"""
Place module.

This module defines two classes: BaseModel and Place.
- BaseModel provides basic ID and timestamp functionality.
- Place represents a rental place, with validations on title, price,
  location, and relationships with amenities and reviews.
"""
from app.extensions import db
from .baseclass import BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

place_amenity = db.Table('place_amenity',
                         Column('place_id', Integer, ForeignKey('places.id'), primary_key=True),
                         Column('amenity_id', Integer, ForeignKey('amenities.id'), primary_key=True)
                         )


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

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates="places")
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenity, lazy='subquery',
                             backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner_id

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [a.to_dict() for a in self.amenities],
            'reviews': [r.to_dict() for r in self.reviews]
        }
