grammar SMSH;

pipeline
    : command (PIPE command)* EOF
    ;

command
    : COMMAND args?
    ;

args
    : argument+
    ;

argument
    : ESCAPED_STRING
    | UNQUOTED
    ;

COMMAND: [a-zA-Z_][a-zA-Z0-9_]*;

ESCAPED_STRING
    : '"' (ESC_SEQ | ~["\\])* '"'
    ;

fragment ESC_SEQ
    : '\\' ['"\\|]
    ;

UNQUOTED: ~[ \t\r\n|"]+;

PIPE: '|';
WS: [ \t\r\n]+ -> skip;
