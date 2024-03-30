#!/usr/bin/python3
"""test for db file storage"""
import unittest
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


class TestDbStorage(unittest.TestCase):
    '''this will test the FileStorage'''
    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "file",
                                                       "Don't run file")
    def test_attr(self):
        """Checking attributes"""
        self.assertTrue(hasattr(DBStorage, "_DBStorage__engine"))
        self.assertTrue(hasattr(DBStorage, "_DBStorage__session"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))
