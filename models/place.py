#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity


if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ This class defines a place by various attributes """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)

        @property
        def amenities(self):
            """ This method returns the list of Amenity instances based on the
            attribute amenity_ids that contains all Amenity.id linked to the
            Place."""
            from models import storage
            amenity_instances = []
            for obj in storage.all(Amenity).values():
                if obj.amenity_ids == self.id:
                    amenity_instances.append(obj)
            return amenity_instances

        @amenities.setter
        def amenities(self, amenity):
            """This method handles append method for adding an Amenity.id to
            the attribute amenity_ids"""
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

    """@property
    def reviews(self):"""
    """This method returns the list of Review instances with place_id equals
        to the current Place.id"""
    """from models.review import Review
        from models import storage
        review_instances = []
        for obj in storage.all(Review).values():
            if obj.place_id == self.id:
                review_instances.append(obj)
        return review_instances

    @property
    def amenities(self):"""
    """ This method returns the list of Amenity instances based on the
        attribute amenity_ids that contains all Amenity.id linked to the
        Place.
    """
    """from models.amenity import Amenity
        from models import storage
        amenity_instances = []
        for obj in storage.all(Amenity).values():
            if obj.amenity_ids == self.id:
                amenity_instances.append(obj)
        return amenity_instances

    @amenities.setter
    def amenities(self, amenity):"""
    """This method handles append method for adding an Amenity.id to the
        attribute amenity_ids"""
    """from models.amenity import Amenity
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)"""
