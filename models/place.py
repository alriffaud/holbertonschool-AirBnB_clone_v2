#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity


"""if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))"""


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity,
                                                 viewonly=False)
        @property
        def amenities(self):
            """ This method returns the list of Amenity instances based on the
            attribute amenity_ids that contains all Amenity.id linked to the
            Place."""
            from models.amenity import Amenity
            from models import storage
            amenity_instances = []
            for obj in storage.all(Amenity).values():
                if obj.amenity_ids == self.id:
                    amenity_instances.append(obj)
            return amenity_instances

        @amenities.setter
        def amenities(self, amenity):
            """This method handles append method for adding an Amenity.id to the
            attribute amenity_ids"""
            from models.amenity import Amenity
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)
        amenity_ids = []
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Return the list of Reviews instances with
            place_id equal to the current Review.id
            """
            return [review for review in
                    models.storage.all("Review").values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """"""
            return [amenity for amenity in
                    models.storage.all("Amenity").values()
                    if amenity.amenity_ids == self.id]

        @amenities.setter
        def amenities(self, amenity=None):
            """"""
            if amenity is not None and amenity.__class__.__name__ == "Amenity":
                self.amenity_ids.append(amenity.id)