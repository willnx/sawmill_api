# Generated from SMSH.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,
        1,
        5,
        30,
        2,
        0,
        7,
        0,
        2,
        1,
        7,
        1,
        2,
        2,
        7,
        2,
        2,
        3,
        7,
        3,
        1,
        0,
        1,
        0,
        1,
        0,
        5,
        0,
        12,
        8,
        0,
        10,
        0,
        12,
        0,
        15,
        9,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        3,
        1,
        21,
        8,
        1,
        1,
        2,
        4,
        2,
        24,
        8,
        2,
        11,
        2,
        12,
        2,
        25,
        1,
        3,
        1,
        3,
        1,
        3,
        0,
        0,
        4,
        0,
        2,
        4,
        6,
        0,
        1,
        1,
        0,
        2,
        3,
        28,
        0,
        8,
        1,
        0,
        0,
        0,
        2,
        18,
        1,
        0,
        0,
        0,
        4,
        23,
        1,
        0,
        0,
        0,
        6,
        27,
        1,
        0,
        0,
        0,
        8,
        13,
        3,
        2,
        1,
        0,
        9,
        10,
        5,
        4,
        0,
        0,
        10,
        12,
        3,
        2,
        1,
        0,
        11,
        9,
        1,
        0,
        0,
        0,
        12,
        15,
        1,
        0,
        0,
        0,
        13,
        11,
        1,
        0,
        0,
        0,
        13,
        14,
        1,
        0,
        0,
        0,
        14,
        16,
        1,
        0,
        0,
        0,
        15,
        13,
        1,
        0,
        0,
        0,
        16,
        17,
        5,
        0,
        0,
        1,
        17,
        1,
        1,
        0,
        0,
        0,
        18,
        20,
        5,
        1,
        0,
        0,
        19,
        21,
        3,
        4,
        2,
        0,
        20,
        19,
        1,
        0,
        0,
        0,
        20,
        21,
        1,
        0,
        0,
        0,
        21,
        3,
        1,
        0,
        0,
        0,
        22,
        24,
        3,
        6,
        3,
        0,
        23,
        22,
        1,
        0,
        0,
        0,
        24,
        25,
        1,
        0,
        0,
        0,
        25,
        23,
        1,
        0,
        0,
        0,
        25,
        26,
        1,
        0,
        0,
        0,
        26,
        5,
        1,
        0,
        0,
        0,
        27,
        28,
        7,
        0,
        0,
        0,
        28,
        7,
        1,
        0,
        0,
        0,
        3,
        13,
        20,
        25,
    ]


class SMSHParser(Parser):

    grammarFileName = "SMSH.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "'|'"]

    symbolicNames = ["<INVALID>", "COMMAND", "ESCAPED_STRING", "UNQUOTED", "PIPE", "WS"]

    RULE_pipeline = 0
    RULE_command = 1
    RULE_args = 2
    RULE_argument = 3

    ruleNames = ["pipeline", "command", "args", "argument"]

    EOF = Token.EOF
    COMMAND = 1
    ESCAPED_STRING = 2
    UNQUOTED = 3
    PIPE = 4
    WS = 5

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(
            self, self.atn, self.decisionsToDFA, self.sharedContextCache
        )
        self._predicates = None

    class PipelineContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def command(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(SMSHParser.CommandContext)
            else:
                return self.getTypedRuleContext(SMSHParser.CommandContext, i)

        def EOF(self):
            return self.getToken(SMSHParser.EOF, 0)

        def PIPE(self, i: int = None):
            if i is None:
                return self.getTokens(SMSHParser.PIPE)
            else:
                return self.getToken(SMSHParser.PIPE, i)

        def getRuleIndex(self):
            return SMSHParser.RULE_pipeline

    def pipeline(self):

        localctx = SMSHParser.PipelineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_pipeline)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.command()
            self.state = 13
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 4:
                self.state = 9
                self.match(SMSHParser.PIPE)
                self.state = 10
                self.command()
                self.state = 15
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 16
            self.match(SMSHParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CommandContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMAND(self):
            return self.getToken(SMSHParser.COMMAND, 0)

        def args(self):
            return self.getTypedRuleContext(SMSHParser.ArgsContext, 0)

        def getRuleIndex(self):
            return SMSHParser.RULE_command

    def command(self):

        localctx = SMSHParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_command)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            self.match(SMSHParser.COMMAND)
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 2 or _la == 3:
                self.state = 19
                self.args()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgsContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(SMSHParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(SMSHParser.ArgumentContext, i)

        def getRuleIndex(self):
            return SMSHParser.RULE_args

    def args(self):

        localctx = SMSHParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_args)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 22
                self.argument()
                self.state = 25
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la == 2 or _la == 3):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgumentContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ESCAPED_STRING(self):
            return self.getToken(SMSHParser.ESCAPED_STRING, 0)

        def UNQUOTED(self):
            return self.getToken(SMSHParser.UNQUOTED, 0)

        def getRuleIndex(self):
            return SMSHParser.RULE_argument

    def argument(self):

        localctx = SMSHParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_argument)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            _la = self._input.LA(1)
            if not (_la == 2 or _la == 3):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
