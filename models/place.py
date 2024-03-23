#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv


place_amenity = Table('place_amenity', Bas.metadata,
                      Column('place_id', str(60), ForeignKey(places_id)),
                      Column('amenity_id', str(60), ForeignKey(amenities.id)))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if getenv("HBTN_TYPE_STORAGE") == "db":
        city_id = Column(str(128), nullable=False, ForeignKey(cities.id))
        user_id = Column(str(60), nullable=False, ForeignKey(users.id))
        name = Column(str(128), nullable=False)
        description = Column(str(1024), nullable=False)
        number_rooms = Column(int, nullable=False, default=0)
        number_bathrooms = Column(int, nullable=False, default=0)
        max_guest = Column(int, nullable=False, default=0)
        price_by_night = Column(int, nullable=False, default=0)
        latitude = Column(float, nullable=False)
        longitude = Column(float, nullable=False)
        reviews = relationship("Review", backref="place",
                               casacade="all, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenity")
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
    def review(self):
        """getter attribute reviews that returns the list of
        Review instances with place_id equals to the current Place.id"""
        from models import storage
        from models.reviews import Review
        review_instances = []
        for obj in storage.all(Review).values():
            if obj.place_id == self.id:
                review_instances.append(obj)
        return review_instances

    @property
    def amenities(self):
        """returns the list of Amenity instances based on the attribute
        amenity_ids that contains all Amenity.id linked to the Place"""
    

    @amenities.setter
    def amenities(self):
        """handles append method for adding an Amenity.id to the
        attribute amenity_ids"""
