#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models import storage


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(str(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """ returns the list of City instances with state_id equals
            to the current State.id"""
            city_instances = []
            for key, obj in storage.all().items():
                if obj.__class__.__name__ == 'City':
                    if obj.state_id == self.id:
                        city_instances.append(obj)
            return city_instances
