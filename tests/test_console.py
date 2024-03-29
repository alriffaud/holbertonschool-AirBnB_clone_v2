#!/usr/bin/python3
""" Module for testing console"""
import unittest
import sys
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os
from models import storage


class TestConsole(unittest.TestCase):
    """ Class to test console methods """
    def setUp(self):
        """ Set up test environment """
        self.console = HBNBCommand()

    def tearDown(self):
        """ Remove storage file at end of tests """
        pass

    @patch('sys.stdout', new_callable=StringIO)
    def test_prompt(self, mock_stdout):
        """promt test"""
        with self.assertRaises(SystemExit) as e:
            self.console.onecmd('EOF')
        self.assertEqual(e.exception.code, None)
        self.assertEqual(mock_stdout.getvalue(), '\n')

    def test_help_quit(self):
        """help quit test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('quit')
            self.assertEqual(mock_stdout.getvalue(),
                             "Exits the program with formatting\n\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_quit(self, mock_stdout):
        "do_quit test"
        with self.assertRaises(SystemExit):
            self.console.do_quit('')
        self.assertEqual(mock_stdout.getvalue(), '')

    def test_help_EOF(self):
        """help EOF test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('EOF')
            self.assertEqual(mock_stdout.getvalue(),
                             "Exits the program without formatting\n\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_EOF(self, mock_stdout):
        """do_EOF test"""
        with self.assertRaises(SystemExit) as e:
            self.console.do_EOF('')
        self.assertEqual(e.exception.code, None)
        self.assertEqual(mock_stdout.getvalue(), '\n')

    def test_emptyline(self):
        """empty line test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.emptyline()
            self.assertEqual(mock_stdout.getvalue(), '')

    def test_precmd(self):
        """pre cmd test"""
        line = "User.update(\"test_id\", {\"name\": \"test_name\"})"
        new_line = self.console.precmd(line)
        self.assertEqual(new_line,
                         "update User test_id {\"name\": \"test_name\"}")

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdin.isatty', return_value=True)
    def test_postcmd(self, mock_isatty, mock_stdin):
        """Test postcmd method"""
        mock_stdin.write('input\n')
        mock_stdin.seek(0)
        self.assertFalse(self.console.postcmd(False, ''))

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create(self, mock_stdout):
        """do_create test"""
        with patch('builtins.input', side_effect=['BaseModel']):
            self.console.onecmd('create BaseModel')
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) > 0)
        instance_id = output
        created_instance = storage.all().get('BaseModel.' + instance_id)
        self.assertIsInstance(created_instance, BaseModel)

    def test_help_create(self):
        """help_create test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('create')
            self.assertIn("Creates a class of any type",
                          mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show(self, mock_stdout):
        """do_show test"""
        base_model = BaseModel()
        key = base_model.__class__.__name__ + '.' + base_model.id
        storage.all()[key] = base_model
        self.console.onecmd('show BaseModel {}'.format(base_model.id))
        self.assertIn(base_model.__str__(), mock_stdout.getvalue())

    def test_help_show(self):
        """help show test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('show')
            self.assertIn("Shows an individual instance of a class",
                          mock_stdout.getvalue())

    def test_do_destroy(self):
        """do_destroy test"""
        obj = BaseModel()
        obj_id = obj.id
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_destroy('BaseModel {}'.format(obj_id))
            self.assertNotIn(obj.__str__(), mock_stdout.getvalue())

    def test_help_destroy(self):
        """help_destroy test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('destroy')
            self.assertIn("Destroys an individual instance of a class",
                          mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all(self, mock_stdout):
        """do_all test"""
        base_model = BaseModel()
        key = base_model.__class__.__name__ + '.' + base_model.id
        storage.all()[key] = base_model
        self.console.onecmd('all BaseModel')
        output = mock_stdout.getvalue().strip()
        self.assertIn(base_model.__str__(), output)

    def test_help_all(self):
        """help all test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('all')
            self.assertIn("Shows all objects, or all of a class",
                          mock_stdout.getvalue())

    def test_do_count(self):
        """do_count test"""
        obj = BaseModel()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_count('BaseModel')
            self.assertEqual(mock_stdout.getvalue(), '1\n')

    def test_help_count(self):
        """help count test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('count')
            self.assertIn("Usage: count <class_name>", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_update(self, mock_stdout):
        """do_update test"""
        base_model = BaseModel()
        key = base_model.__class__.__name__ + '.' + base_model.id
        storage.all()[key] = base_model
        self.console.onecmd('update BaseModel {} name "new_name"'.format(
            base_model.id))
        updated_base_model = storage.all().get(key)
        self.assertEqual(updated_base_model.name, "new_name")
        # self.assertIn("new_name", mock_stdout.getvalue())

    """@patch('sys.stdout', new_callable=StringIO)
    def test_do_create2(self, mock_stdout):
    """   """Test do_create method"""
    """# Call the do_create method to create a BaseModel instance
        self.console.onecmd('create BaseModel')

        # Check if the output of the console contains "BaseModel"
        self.assertIn("BaseModel", mock_stdout.getvalue())"""

    def test_help_update(self):
        """help update test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('update')
            self.assertIn("Updates an object with new information",
                          mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
