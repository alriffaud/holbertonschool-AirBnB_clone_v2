#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """class amenity that conatins name """
    __tablename__ = "amenities"
    if getenv(HBTN_TYPE_STORAGE) == "db":
        name = Column(str(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity,
                                       back_populates="amenities")
    else:
        name = ""
