#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(str(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    def cities(self):
        """ returns the list of City instances with state_id equals
        to the current State.id"""

