#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel


class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ 'cities'
    state_id = Column(str(60), nullable=False, ForeingKey=("states.id"))
    name = Column(str(129), nullable=False)
