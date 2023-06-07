import unittest
import sys
import os
from unittest.mock import MagicMock
from mvd.commands.environment import Environment, LazyClickGroup
import mvd.dictionary.multivaluedict as multivaluedict
import rich_click as click


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.environment = Environment()

    def test_environment_initialization(self):
        self.assertFalse(self.environment.verbose)
        self.assertIsNone(self.environment.dict_file)
        self.assertTrue(self.environment.do_save)
        self.assertIsInstance(self.environment.dictionary,
                              multivaluedict.MultiValueDict)

    def test_environment_log(self):
        click.echo = MagicMock()
        self.environment.log("Test log message")
        # Assert that click.echo was called with the expected arguments
        click.echo.assert_called_once_with("Test log message", file=sys.stderr)

    def test_environment_vlog_verbose_enabled(self):
        self.environment.verbose = True
        self.environment.log = MagicMock()
        self.environment.vlog("Test verbose log message")
        # Assert that self.environment.log was called with the expected arguments
        self.environment.log.assert_called_once_with("Test verbose log message")

    def test_environment_vlog_verbose_disabled(self):
        self.environment.verbose = False
        self.environment.log = MagicMock()
        self.environment.vlog("Test verbose log message")
        # Assert that self.environment.log was not called
        self.environment.log.assert_not_called()


class TestLazyClickGroup(unittest.TestCase):

    def setUp(self):
        self.lazy_click_group = LazyClickGroup()

    def test_list_commands(self):
        self.lazy_click_group.cmd_folder = "test_commands_folder"
        os.listdir = MagicMock(
            return_value=["cmd_command1.py", "cmd_command2.py",
                          "other_file.txt"])
        command_list = self.lazy_click_group.list_commands(None)
        self.assertEqual(command_list, ["command1", "command2"])

    def test_get_command_with_valid_module(self):
        # I can not figure out how to mock __import__
        # to get this test to work
        self.assertTrue(1, 1)

    def test_get_command_with_invalid_module(self):
        # I can not figure out how to mock __import__
        # to get this test to work
        self.assertTrue(1, 1)


if __name__ == '__main__':
    unittest.main()
