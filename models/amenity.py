#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    """class amenity that conatins name """
    #if getenv("HBNB_TYPE_STORAGE") == "db":
     #   from models.place import place_amenity
      #  __tablename__ = "amenities"
       # name = Column(String(128), nullable=False)
        #place_amenities = relationship("Place", secondary=place_amenity,
     #                                  back_populates="amenities")
    #else:
    name = ""
