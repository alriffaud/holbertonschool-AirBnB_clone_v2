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
import json
import console
import tests
from models.engine.file_storage import FileStorage


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "Invalid syntax")
class TestConsole(unittest.TestCase):
    """ Class to test console methods """
    def setUp(self):
        """ Set up test environment """
        self.console = HBNBCommand()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
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

    def test_help_update(self):
        """help update test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.do_help('update')
            self.assertIn("Updates an object with new information",
                          mock_stdout.getvalue())


class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        cls.consol = HBNBCommand()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.consol

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "Invalid syntax")
    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create(self, mock_stdout):
        """do_create test"""
        with patch('builtins.input', side_effect=['BaseModel']):
            self.consol.onecmd('create BaseModel')
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) > 0)
        instance_id = output
        self.assertFalse(instance_id.startswith("BaseModel."))
        created_instance = storage.all().get(instance_id)
        self.assertNotIsInstance(created_instance, BaseModel)

    def test_show(self):
        """Test show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "Invalid syntax")
    def test_all(self):
        """Test all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "Invalid syntax")
    def test_z_all(self):
        """Test alternate all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.all()")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.all()")
            self.assertEqual('', f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "Invalid syntax")
    def test_z_count(self):
        """Test count command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.count()")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.count()")
            self.assertEqual('', f.getvalue())

    def test_z_show(self):
        """Test alternate show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("safdsa.show()")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual('', f.getvalue())

    def test_destroy(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("Galaxy.destroy()")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.destroy(12345)")
            self.assertEqual('', f.getvalue())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                                                       "Invalid syntax")
    def test_update(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("sldkfjsl.update()")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(12345)")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ")")
            self.assertEqual('', f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual('', f.getvalue())


if __name__ == "__main__":
    unittest.main()
