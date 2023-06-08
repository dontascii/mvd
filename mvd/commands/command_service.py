
from typing import List
from rich_click import RichCommand
import rich_click as click

from mvd.commands.environment import LazyClickGroup


class CommandService:
    """
    Provides utility methods for interacting with
    click commands
    """

    def __init__(self):

        self.command_list: List[str] = []

    @property
    def command_list(self):
        if not len(self._command_list):
            cmds: List[str] = LazyClickGroup().list_commands(None)
            self._command_list = [cmd.upper() for cmd in cmds] + ["HELP",
                                                                  "QUIT"]
        return self._command_list

    @command_list.setter
    def command_list(self, value):
        self._command_list = value

    def auto_complete(self, str_input: str = "",
                      black_list: List[str] = ["CLI"]) -> List[str]:
        return [cmd for cmd in self.command_list if
                cmd.startswith(str_input) and
                cmd not in black_list]

    def render_help(self, params=[], context=None) -> str:
        result = ""
        if len(params) > 1:
            if params[1] in self.command_list:
                cmd = LazyClickGroup().get_command(context, params[1])
                usage: str = cmd.get_usage(context)
                usage = usage.replace("mvd cli", params[1])
                usage = usage.replace(" [OPTIONS]", "")
                result += usage
                result += "\n" + cmd.get_short_help_str()
        elif len(params) == 1:
            result += '\nAvailable Commands: '
            for cmd in self.command_list:
                result += f"\n{cmd}"
            result += "\nUse `HELP <COMMAND>` for help on a specific command."
        return result

    def invoke_command_with_context(self, params=[], context:click.Context=None) -> str:
        if params[0] in ['ADD','CLEAR','REMOVE','REMOVEALL']:
            context.obj.do_save = True
        cmd_command: RichCommand = LazyClickGroup().get_command(context, params[0])
        cmd_command.allow_extra_args = True
        cmd_context = cmd_command. \
            make_context(params[0], params[1:], context.parent)
        with cmd_context:
            result =  cmd_command.invoke(cmd_context)
        return result
           
