import unittest
from unittest.mock import MagicMock, Mock
from typing import List
import rich_click as click
from mvd.commands.command_service import CommandService
from mvd.commands.environment import Environment, LazyClickGroup

class TestCommandService(unittest.TestCase):

    def setUp(self):
        self.command_service = CommandService()
        self.lazy_click_group = MagicMock()
        self.command_service.LazyClickGroup = MagicMock(return_value=self.lazy_click_group)

    def test_auto_complete(self):
        self.command_service.command_list = ["COMMAND1", "COMMAND2", "HELP", "QUIT"]
        completions = self.command_service.auto_complete("CO", black_list=["HELP"])
        self.assertEqual(completions, ["COMMAND1", "COMMAND2"])

    def test_render_help_with_command(self):
        mockObject = LazyClickGroup
        mockObject.get_command = Mock(return_value=MagicMock())
        mockObject.get_command.return_value.get_usage = \
            MagicMock(return_value="Usage: mvd cli [OPTIONS]")
        mockObject.get_command.return_value.get_short_help_str = \
            MagicMock(return_value="Short help")
        params = ["HELP", "CLI"]
        help_text = self.command_service.render_help(params)
        expected_output = "Usage: CLI\nShort help"
        self.assertEqual(help_text, expected_output)

    def test_render_help_without_command(self):
        self.command_service.command_list = ["COMMAND1", "COMMAND2", "HELP", "QUIT"]
        help_text = self.command_service.render_help(["HELP"])
        expected_output = "\nAvailable Commands: \nCOMMAND1\nCOMMAND2\nHELP\nQUIT\nUse `HELP <COMMAND>` for help on a specific command."
        self.assertEqual(help_text, expected_output)

    def test_invoke_command_with_context(self):
        mockObject = LazyClickGroup
        mockObject.get_command = Mock(return_value=MagicMock())
        mockObject.get_command.return_value.make_context = \
            MagicMock(return_value=MagicMock(spec=click.Context))
        mockObject.get_command.return_value.invoke = \
            MagicMock(return_value="Command output")
        params = ["ADD", "param1", "param2"]
        context = MagicMock(spec=click.Context)
        context.obj = Environment()
        context.parent = None
        result = self.command_service.invoke_command_with_context(params, context)
        self.assertEqual(result, "Command output")
        self.assertTrue(context.obj.do_save)

if __name__ == '__main__':
    unittest.main()
