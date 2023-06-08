"""
terminal.py
author: dontascii
email: dontascii@duck.com
copyright 2023 - Joel Clegg
"""
from abc import ABC, abstractmethod
from collections import deque
from typing import List, Union

import blessed
import rich_click as click

from mvd.commands.command_service import CommandService


class Parsable(ABC):
    """
    parse keyboard input
    """

    def __init__(self):
        self.__user_input: str = ""

    @property
    def user_input(self) -> str:
        return self.__user_input

    @user_input.setter
    def user_input(self, value: str) -> None:
        self.__user_input = value

    @abstractmethod
    def parse_input(self) -> None:
        pass


class AutoCompleteInputParser(Parsable):
    """InputParser with auto-completion and command history support"""

    def __init__(self, context: Union[click.Context, None] = None):
        super().__init__()
        self.context = context
        self.command_service: CommandService = CommandService()
        self.command_history = deque()
        self.back_cnt: int = 0

    def navigate_history(self, back: bool = True) -> None:
        """this callback is fired when the user presses the up/down
        arrows and populates the input with the next command in the 
        history buffer. 

        Args:
            back (bool, optional): Navigating backwards. (up arrow pressed) 
            Defaults to True.
        """
        if back:
            if self.back_cnt < len(self.command_history):
                # if we have commands still in the buffer
                command = self.command_history.popleft()
                # pop the top command
                self.command_history.append(command)
                # and add it to the end of the buffer
                self.back_cnt += 1
                # increment the counter
                self.user_input = command
                # and set the user_input
        elif self.back_cnt > 0:
            # pop the command at the end of the buffer
            command = self.command_history.pop()
            # and add it to the front 
            self.command_history.appendleft(command)
            # decrement our counter
            self.back_cnt -= 1
            # set the user_input
            self.user_input = command
        else:
            self.user_input = ""
            self.back_cnt = 0

    def fill_auto_complete(self) -> None:
        """
        auto-completes the command. This will be called when 
        the user presses the tab key 
        """
        user_input = self.user_input
        # split the input up into words
        user_inputs: List[str] = user_input.split(' ')
        # if the first word typed is "HELP", we want to 
        # auto-complete the second word. 
        if len(user_inputs) > 1 and user_inputs[0] == "HELP":
            user_input = user_inputs[1]
        cmds = self.command_service.auto_complete(user_input)
        if len(cmds):
            # auto-complete the word using the top command
            user_input = cmds[0]
            # replace the incomplete word with the auto-completed command
            user_inputs[-1] = user_input
            # set self.user_input to the full, auto-completed phrase
            self.user_input = ' '.join(user_inputs)
            # add it to the top of the history stack
            self.command_history.appendleft(self.user_input)

    @abstractmethod
    def auto_complete(self) -> None:
        pass


class InteractiveCli(AutoCompleteInputParser):
    """
    This class drives the interactive command-line interface. It handles
    parsing user input, command history, auto-complete
    functionality, command invocation, and other aspects of the UI.
    """

    def __init__(self, context: Union[click.Context, None] = None) -> None:
        super().__init__(context)

        self.__term: blessed.Terminal = blessed.Terminal()
        self.__running: bool = False
        self.__out: str = ""

    @property
    def terminal(self) -> blessed.Terminal:
        """
        getter that incapsulates the private __term attribute
        """
        return self.__term

    @terminal.setter
    def terminal(self, value: blessed.Terminal) -> None:
        """
        the setter that encapsulates the private __term attribute
        """
        self.__term: blessed.Terminal = value

    @property
    def running(self) -> bool:
        """
        the running property is the boolean value used for
        the while loop that refreshes the ui and waits for 
        user input. This encapsulates the private __running
        attribute       

        Returns:
            bool: the private __running attribute
        """
        return self.__running

    @running.setter
    def running(self, value: bool) -> None:
        """this is the setter that encapsulates the private __running attribute

        Args:
            value (bool): the value to set 
        """
        self.__running = value

    @staticmethod
    def get_prompt() -> str:
        """
        a static method for the prompt message
        """
        results: List[str] = ["©Copyright 2023 - dontascii - All Rights " +
                              "Reserved  ",
                              "MultiValue Dictionary Interactive CLI",
                              "\nTo get help with a command, " +
                              "type `HELP {COMMAND}` and press ENTER.",
                              "to quit, press the escape key or QUIT"]
        return '\n'.join(results)


    def auto_complete(self) -> None:
        """
        this is the implemetation of the auto_complete 
        abstract method from the base class. 
        """
        # get the current location of the cursor
        y, x = self.terminal.get_location()
        user_input = self.user_input
        user_inputs: List[str] = user_input.split(' ')
        # split the input into words 
        if len(user_inputs) > 1 and user_inputs[0] == "HELP":
            # if "HELP" has already been typed, we are auto-completing the next word
            user_input = user_inputs[1]
        # this is the location of the cursor at the beginning of the word we are auto-completing
        start_x = x - len(user_input)
        # set our format function - in this case, the text will be bold and yellow
        fmt_func = self.terminal.bold_yellow
        if not len(user_input):
            return
        completions = self.command_service.auto_complete(user_input)

        for i, cmd in enumerate(completions):
            if i == 0:
                # if this is the top suggestion
                with self.terminal.location(x=x, y=y):
                    # move the cursor to the location at x, y 
                    print(fmt_func(cmd[len(user_input):]))
                    # print the rest of the command suggestion that the
                    # user has yet to type using our format function
                    # and increment y so the cursor jumps to the next line
                    y += 1
            else:
                # for the rest of the suggestions
                with self.terminal.location(x=start_x, y=y):
                    # move the cursor so its directly underneath the 
                    # start of word the user has already typed
                    print(self.terminal.bold(cmd))
                    # print the suggestion in bold and increment y 
                    # to jump tothe next line
                    y += 1

    def parse_input(self) -> None:
        """
        the implementation of the parse_input abstract method 
        from the Parsable base class
        """
        params = self.user_input.split(' ')
        self.__out += f"\n>>>{self.user_input}\n"
        self.command_history.appendleft(self.user_input)
        self.user_input = ""
        if params[0] == "QUIT":
            self.running = False
            return
        elif params[0] == "HELP":
            self.__out += self.command_service.render_help(params, self.context)
            return
        elif params[0] in self.command_service.command_list:
            result = self.command_service.invoke_command_with_context(
                params, self.context)
            if result is not None:
                self.__out += result 

    def start(self) -> None:
        """
        starts the interactive CLI by setting running to True and 
        looping until running is False
        """
        if self.running:
            return
        self.running = True

        with self.terminal.fullscreen(), \
             self.terminal.hidden_cursor(), \
             self.terminal.cbreak():
            # enters "rare" mode, (tty.setcbreak) 
            # and activates the secondary tty screen buffer,
            # hides the cursor from being drawn and
            # disables line buffering of input and echoing of input to stdout
            while self.running:
                click.clear()
                print(InteractiveCli.get_prompt(), end="", flush=True)
                print(self.__out, flush=True)
                print('>>>', end="", flush=True)
                print(self.user_input, end="", flush=True)
                self.auto_complete()
                pressed = self.terminal.inkey()
                # wait for the user to type something
                if isinstance(pressed, str) and (pressed.isalnum()
                                                 or pressed in [' ', '-']):
                    # if the key pressed is alpha-numeric or a space or hyphen
                    if ' ' in self.user_input \
                            and not self.user_input.startswith("HELP"):
                        # if they are typing a second word and the first word is
                        # not the "HELP" command, just add it to user_input as-is
                        self.user_input += pressed
                    else:
                        # otherwise, assume its a command and use upper-case
                        self.user_input += pressed.upper()
                elif pressed.code in [self.terminal.KEY_TAB]:
                    # if the tab key was hit, try and auto complete the input
                    self.fill_auto_complete()
                elif pressed.code in [self.terminal.KEY_ENTER]:
                    # process the command(s) that have been entered
                    self.parse_input()
                elif pressed.code in [self.terminal.KEY_BACKSPACE]:
                    self.user_input = self.user_input[:-1]
                elif pressed.code in [self.terminal.KEY_ESCAPE]:
                    # bail out of the loop and close the terminal
                    self.running = False
                elif pressed.code in [self.terminal.KEY_UP,
                                      self.terminal.KEY_DOWN]:
                    self.navigate_history(
                        back=pressed.code == self.terminal.KEY_UP)
