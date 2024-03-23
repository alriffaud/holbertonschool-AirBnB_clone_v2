#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey,  String
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel):
    """This class defines a user by various attributes"""
    __tablename__ = "users"
    if getenv("HBTN_TYPE_STORAGE") = "db":
        email = Column(str(128), nullable=False)
        password = Column(str(128), nullable=False)
        first_name = Column(str(128), nullable=False)
        last_name = Column(str(128), nullable=False)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
