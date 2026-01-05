grammar HyperCode;

options {
    language=Python3;
}

@parser::members {
    def __init__(self, input, output=sys.stdout):
        super().__init__(input, output)
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
}

@lexer::members {
    def __init__(self, input=None, output=sys.stdout):
        super().__init__(input, output)
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
}


// Parser rules
program
    : (functionDef | domainDirective | backendDirective | COMMENT | WHITESPACE)* EOF
    ;

functionDef
    : '@' 'quantum_function' ':' IDENTIFIER '(' ')' '->' type block
    | '@' 'function' ':' IDENTIFIER '(' ')' ( '->' type )? block
    ;

type
    : 'Bits'
    | 'Qubit'
    | 'Int'
    | 'Float'
    | 'String'
    | 'Void'
    ;

block
    : '{' statement* '}'
    | statement+
    ;

statement
    : circuitStmt
    | letStmt
    | returnStmt
    | exprStmt
    ;

circuitStmt
    : '@' 'circuit' ':' IDENTIFIER block
    ;

letStmt
    : '@' 'let' ':' IDENTIFIER '=' expr
    ;

returnStmt
    : '@' 'return' ':' expr
    ;

exprStmt
    : expr
    ;

expr
    : IDENTIFIER
    | NUMBER
    | STRING
    | functionCall
    ;

functionCall
    : IDENTIFIER '(' ( expr ( ',' expr )* )? ')'
    ;

// Directives
domainDirective
    : '#:' 'domain' ':' IDENTIFIER
    ;

backendDirective
    : '#:' 'backend' ':' IDENTIFIER
    ;

// Lexer rules
WHITESPACE : [ \t\r\n]+ -> skip ;

// Comments start with '#' and go to the end of the line
COMMENT : '#' ~[\r\n]* -> skip ;

IDENTIFIER : [a-zA-Z_] [a-zA-Z0-9_]* ;
NUMBER : [0-9]+ ('.' [0-9]+)? ;
STRING : '"' .*? '"' ;

// Keywords
QUANTUM : 'quantum' ;
CLASSICAL : 'classical' ;
MOLECULAR : 'molecular' ;

// Operators
ASSIGN : '=' ;
PLUS : '+' ;
MINUS : '-' ;
MUL : '*' ;
DIV : '/' ;

LPAREN : '(' ;
RPAREN : ')' ;
LBRACE : '{' ;
RBRACE : '}' ;
LBRACK : '[' ;
RBRACK : ']' ;
COLON : ':' ;
COMMA : ',' ;
DOT : '.' ;
AT : '@' ;
ARROW : '->' ;
