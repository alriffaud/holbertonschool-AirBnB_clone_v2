#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table, Integer, Float
from sqlalchemy.orm import relationship
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id')),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'))
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if getenv("HBTN_TYPE_STORAGE") == "db":
        city_id = Column(String(128), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
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
    def reviews(self):
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
        from models import storage
        from models.amenity import Amenity
        amenity_instances = []
        for obj in storage.all(Amnity).values():
            if obj.amenity_ids == self.id:
                amenity_instances.append(obj)
        return amenity_instances

    

    @amenities.setter
    def amenities(self, amenity):
        """handles append method for adding an Amenity.id to the
        attribute amenity_ids"""
        from models.amenity import Amenity
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
