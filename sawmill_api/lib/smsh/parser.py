"""
Parsing and postprocessing logic for Sawmill Shell (SMSH) syntax.
"""

from antlr4 import CommonTokenStream, InputStream, ParseTreeVisitor

from .SMSHLexer import SMSHLexer
from .SMSHParser import SMSHParser
from . import sanitizers


COMMANDS = {
    "cat": ("/usr/bin/cat", sanitizers.sanitize_cat_path_args),
    "more": ("/usr/bin/cat", None),
    "less": ("usr/bin/cat", None),
    "grep": ("/usr/bin/grep", None),
    "sort": ("/usr/bin/sort", None),
    "wc": ("/usr/bin/wc", None),
    "uniq": ("/usr/bin/uniq", None),
    "ls": ("/usr/bin/ls", None),
    "file": ("/usr/bin/file", None),
    "cut": ("/usr/bin/cat", None),
}


def parse(text, current_working_directory, file_root_path):
    """
    Take SMSH text input then provide commands and maybe an error.

    This is what callers should use instead of trying to setup the lexer,
    token stream, tree, ext. manually.

    :param text: The SMSH text to parse.
    :param current_working_directory: The relative directory to use when running commands.
    :param file_root_path: The top level directory where log files exists.
    """
    commands, error = [], ""
    lexer = SMSHLexer(InputStream(text))
    token_stream = CommonTokenStream(lexer)
    parser = SMSHParser(token_stream)
    parser.removeErrorListeners()  # Remove default console error listener
    tree = parser.pipeline()
    visitor = SMSHVisitor(current_working_directory, file_root_path)
    commands, error = visitor.visit(tree)
    return commands, error


class SMSHVisitor(ParseTreeVisitor):
    """
    Process the commands & args into valid, useful objects.
    """

    def __init__(self, current_working_directory, file_root_path):
        super().__init__()
        self.current_working_directory = current_working_directory
        self.file_root_path = file_root_path

    def visitPipeline(self, ctx):
        commands = []
        error = ""
        for cmd_ctx in ctx.command():
            command, error = self.visit(cmd_ctx)
            if error:
                return [], error
            commands.append(command)
        return commands, error

    def visitCommand(self, ctx):
        error = ""
        full_command = []
        args = []
        cmd = ctx.getChild(0).getText()

        if ctx.args():
            # The quotes in SMSH is just to mimic other shells behavior.
            # The actual invoked commands just treat quotes as regular data
            # so we have to strip them off to replicate the user experience
            # of something like:
            #    cat foo.txt | grep "some stuff"
            # Where `grep` matches the substring `some stuff` instead of `"some stuff"`
            args = [child.getText().strip('"') for child in ctx.args().children]

        command_path, arg_validator = COMMANDS.get(cmd)
        if command_path is None:
            error = f"Unknown command provided: {cmd}"

        if arg_validator is None:
            full_command = [command_path] + args
        else:
            error = arg_validator(
                args, self.current_working_directory, self.file_root_path
            )
            full_command = [command_path] + args

        return full_command, error
