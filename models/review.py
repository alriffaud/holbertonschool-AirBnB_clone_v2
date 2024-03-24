#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
#from sqlalchemy import Column, String, ForeignKey
#from os import getenv


class Review(BaseModel):
    """ Review classto store review information """
    #__tablename__ = "reviews"
    #if getenv("HBTN_TYPE_STORAGE") == "db":
     #   text = Column(String(1024), nullable=False)
      #  place_id = Column(String(60), ForeignKey("places.id"))
       # user_id = Column(nullable=False, ForeignKey("users.id"))
    #else:
    place_id = ""
    user_id = ""
    text = ""
