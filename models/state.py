#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
#from sqlalchemy import Column, String
#from sqlalchemy.orm import relationship
#from os import getenv


class State(BaseModel):
    """ State class """
    #if getenv('HBNB_TYPE_STORAGE') == 'db':
        #__tablename__ = "states"
       # name = Column(String(128), nullable=False)
      #  cities = relationship("City", backref="state",
     #                         cascade="all, delete-orphan")
    #else:
    name = ""
#
       # @property
        #def cities(self):
         #   """ returns the list of City instances with state_id equals
          #  to the current State.id"""
           # from models import storage
            #from models.city import City
            #city_instances = []
            #for obj in storage.all(City).values():
             #   if obj.state_id == self.id:
             #       city_instances.append(obj)
            #return city_instances
