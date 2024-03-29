#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import os
import json


class test_fileStorage(unittest.TestCase):
    """ Class to test file storage methods """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]
        self.file_path = "test_file.json"
        self.storage = FileStorage()
        self.storage._FileStorage__file_path = self.file_path
        self.storage._FileStorage__objects = {}

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        obj = BaseModel()
        self.storage.new(obj)
        key = obj.__class__.__name__ + "." + obj.id
        self.assertIn(key, self.storage.all().keys())

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            self.assertEqual(new.to_dict()['id'], obj.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            self.assertEqual(key, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    #nuevos
    def test_file_path_attribute(self):
        """This function tests __file_path attribute"""
        self.assertEqual(
            self.storage._FileStorage__file_path, "test_file.json")

    def test_working_save(self):
        """Test to validate save works."""
        fs = FileStorage()
        fs.new(BaseModel())
        fs.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_objects_attribute(self):
        """This function tests __objects attribute"""
        self.assertEqual(self.storage._FileStorage__objects, {})

    def test_all_method(self):
        """This function tests all method"""
        self.assertEqual(self.storage.all(), {})

    def test_all_return_type(self):
        """Test to validate all() returns an object."""
        self.assertEqual(type(self.storage.all()), dict)

    def test_all_return_type(self):
        """Test to validate all() returns an empty dict"""
        self.assertFalse(self.storage.all())
        self.storage.new(BaseModel())
        self.assertTrue(self.storage.all())

    def test_new_method(self):
        """This function tests new method"""
        obj = BaseModel()
        self.storage.new(obj)
        key = "BaseModel.{}".format(obj.id)
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], obj)

    def test_save_method(self):
        """This function tests save method"""
        obj = BaseModel()
        key = "BaseModel.{}".format(obj.id)
        self.storage.all()[key] = obj
        storage.save()
        self.assertTrue(os.path.exists('file.json'))
        with open('file.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            self.assertIn(key, data)
            self.assertEqual(data[key], obj.to_dict())

    def test_reload_method(self):
        """This function tests reload method"""
        obj = BaseModel()
        key = "BaseModel.{}".format(obj.id)
        self.storage.all()[key] = obj
        self.storage.save()
        # Clear objects and reload from the file
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertIn(key, self.storage.all())
        reloaded_obj = self.storage.all()[key]
        self.assertIsInstance(reloaded_obj, BaseModel)
        self.assertEqual(reloaded_obj.to_dict(), obj.to_dict())

    def test_working_reload_2(self):
        """Test to validate reload works."""
        b = BaseModel()
        key = "BaseModel" + "." + b.id
        b.save()
        b1 = BaseModel()
        key1 = "BaseModel" + "." + b1.id
        b1.save()
        self.assertTrue(storage.all()[key] is not None)
        self.assertTrue(storage.all()[key1] is not None)
        with self.assertRaises(KeyError):
            storage.all()[12345]

    def test_working_reload(self):
        """Checks reload functionality if file_path doesn't exist"""
        fs = FileStorage()
        b = BaseModel()
        key = "BaseModel" + '.' + b.id
        fs.new(b)
        fs.save()
        fs.reload()
        self.assertTrue(fs.all()[key])


if __name__ == '__main__':
    unittest.main()