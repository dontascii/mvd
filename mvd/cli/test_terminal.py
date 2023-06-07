"""
test_terminal.py
author: dontascii
email: dontascii@duck.com
copyright 2023 - Joel Clegg
"""
import unittest
from unittest.mock import MagicMock
from mvd.commands.command_service import CommandService
from mvd.cli.terminal import  InteractiveCli

class TestAutoCompleteInputParser(unittest.TestCase):
    """
    unittest class for AutoCompleteInputParser
    """

    def setUp(self):
        self.parser = InteractiveCli()
        self.command_service = CommandService()

    def test_fill_auto_complete(self):
        self.parser.user_input = "HEL"
        self.parser.command_service.auto_complete = MagicMock(
            return_value=["HELP", "HELLO"])
        self.parser.fill_auto_complete()
        self.assertEqual(self.parser.user_input, "HELP")
        self.parser.command_service.auto_complete = MagicMock(
            return_value=[])
        self.parser.user_input = "ABC"
        self.parser.fill_auto_complete()
        self.assertEqual(self.parser.user_input, "ABC")
        self.parser.command_service.auto_complete = MagicMock(
            return_value=["ADD"])
        self.parser.user_input = "HELP a"
        self.parser.fill_auto_complete()
        self.assertEqual(self.parser.user_input, "HELP ADD")

class TestInteractiveCli(unittest.TestCase):
    """
    unittest class for InteractiveCli 
 
    """

    def setUp(self):
        self.cli = InteractiveCli()
        self.cli.command_service = CommandService()


    def test_auto_complete(self):
        self.cli.terminal = MagicMock()
        self.cli.terminal.get_location = MagicMock(return_value=(0, 0))
        self.cli.user_input = "HE"
        self.cli.command_service.auto_complete = MagicMock(return_value=["HELP", "HELLO"])
        self.cli.auto_complete()
        self.cli.terminal.bold_yellow.assert_called_with("LP")

    def test_parse_input_quit_command(self):
        self.cli = InteractiveCli()
        self.cli.user_input = "QUIT"
        self.cli.running = True
        self.cli.parse_input()
        self.assertFalse(self.cli.running)

    def test_parse_input_help_command(self):
        self.cli.user_input = "HELP COMMAND"
        self.cli.command_service.render_help = MagicMock(return_value="Help information")
        self.cli.parse_input()
        self.assertEqual(self.cli._InteractiveCli__out, "\n>>>HELP COMMAND\nHelp information")

    def test_parse_input_valid_command(self):
        self.cli.user_input = "VALID COMMAND"
        self.cli.command_service.command_list = ["VALID", "COMMAND"]
        self.cli.command_service.invoke_command_with_context = MagicMock(return_value="Command output")
        self.cli.parse_input()
        self.assertEqual(self.cli._InteractiveCli__out, "\n>>>VALID COMMAND\nCommand output")

if __name__ == '__main__':
    unittest.main()
