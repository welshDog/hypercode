grammar HyperCode;

// v0 Vertical Slice Grammar
// Focus: Minimal noise, neurodivergent-friendly

program: statement* EOF;

statement
    : dataDecl
    | setStmt
    | printStmt
    | checkStmt
    | COMMENT
    ;

// @data name: value
dataDecl: '@data' IDENTIFIER ':' expr;

// @set name: value
setStmt: '@set' IDENTIFIER ':' expr;

// @print(expr)
printStmt: '@print' '(' expr ')';

// @check(expr) -> { ... }
checkStmt: '@check' '(' expr ')' '->' block;

block: '{' statement* '}';

expr
    : IDENTIFIER
    | STRING
    | NUMBER
    | binaryExpr
    ;

binaryExpr: expr OP expr;

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+;
STRING: '"' .*? '"';
COMMENT: '#' ~[\r\n]*;
OP: '>' | '<' | '==' | '+' | '-';
WHITESPACE: [ \t\r\n]+ -> skip;
