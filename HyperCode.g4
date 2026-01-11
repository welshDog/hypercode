/**
 * HyperCode ANTLR4 Grammar
 * 
 * A formal grammar for HyperCode, a neurodivergent-first programming language
 * designed for quantum, classical, and molecular computing.
 * 
 * Generated: January 2026
 * Based on: hypercode/parser/parser.py + design specification
 * 
 * This grammar defines:
 * - Lexical rules (tokens)
 * - Parser rules (grammar structure)
 * - Support for quantum gates, classical operations, and molecular assembly
 */

grammar HyperCode;

// ============================================================================
// LEXER RULES (Tokens)
// ============================================================================

/**
 * KEYWORDS
 * Reserved words that define language constructs
 */
INIT       : 'init' ;
MEASURE   : 'measure' ;
RETURN    : 'return' ;
HADAMARD  : 'hadamard' ;
PAULI_X   : 'pauli_x' ;
PAULI_Y   : 'pauli_y' ;
PAULI_Z   : 'pauli_z' ;
CNOT      : 'cnot' ;
TOFFOLI   : 'toffoli' ;
SWAP      : 'swap' ;
PHASE     : 'phase' ;
T_GATE    : 't_gate' ;
S_GATE    : 's_gate' ;
RX        : 'rx' ;
RY        : 'ry' ;
RZ        : 'rz' ;
CPHASE    : 'cphase' ;

// Classical / Molecular
FUNCTION  : 'function' ;
IF        : 'if' ;
ELSE      : 'else' ;
FOR       : 'for' ;
WHILE     : 'while' ;
LET       : 'let' ;
CONST     : 'const' ;
TRUE      : 'true' ;
FALSE     : 'false' ;
AND       : 'and' ;
OR        : 'or' ;
NOT       : 'not' ;

// Molecular / DNA
GOLDEN_GATE  : 'golden_gate' ;
PCR          : 'pcr' ;
CRISPR       : 'crispr' ;
DIGEST       : 'digest' ;
LIGATE       : 'ligate' ;
ANNEAL       : 'anneal' ;
REPLICATE    : 'replicate' ;

/**
 * IDENTIFIERS & LITERALS
 */
IDENTIFIER : [a-zA-Z_] [a-zA-Z0-9_]* ;
NUMBER     : [0-9]+ ('.' [0-9]+)? ;
STRING     : '"' (~["\\\r\n] | '\\' .)* '"' 
           | '\'' (~['\\\r\n] | '\\' .)* '\'' 
           ;

/**
 * OPERATORS & PUNCTUATION
 */
LPAREN     : '(' ;
RPAREN     : ')' ;
LBRACE     : '{' ;
RBRACE     : '}' ;
LBRACKET   : '[' ;
RBRACKET   : ']' ;
COMMA      : ',' ;
SEMICOLON  : ';' ;
COLON      : ':' ;
ARROW      : '->' ;
EQUALS     : '=' ;
PLUS       : '+' ;
MINUS      : '-' ;
STAR       : '*' ;
SLASH      : '/' ;
PERCENT    : '%' ;
POWER      : '**' ;
EQ         : '==' ;
NE         : '!=' ;
LT         : '<' ;
GT         : '>' ;
LE         : '<=' ;
GE         : '>=' ;
AMP        : '&' ;
PIPE       : '|' ;
CARET      : '^' ;
TILDE      : '~' ;
QUESTION   : '?' ;
DOT        : '.' ;
AT         : '@' ;

/**
 * WHITESPACE & COMMENTS
 * Skipped during parsing
 */
WS         : [ \t\r\n\u000C]+ -> skip ;
COMMENT    : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

/**
 * ERROR TOKEN
 * Catch-all for unrecognized input (helps with error reporting)
 */
ERROR_CHAR : . ;

// ============================================================================
// PARSER RULES (Grammar)
// ============================================================================

/**
 * PROGRAM: Entry point
 * A HyperCode program is a sequence of statements
 */
program
    : statement* EOF
    ;

/**
 * STATEMENT: Any executable unit
 * Can be a declaration, control flow, expression, or operation
 */
statement
    : variableDeclaration SEMICOLON
    | functionDeclaration
    | ifStatement
    | whileStatement
    | forStatement
    | expressionStatement SEMICOLON
    | blockStatement
    | returnStatement SEMICOLON
    | quantumOperation SEMICOLON
    | molecularOperation SEMICOLON
    ;

/**
 * VARIABLE DECLARATION
 * Syntax: let x: Type = value
 *         const y: Type
 */
variableDeclaration
    : (LET | CONST) IDENTIFIER COLON typeAnnotation (EQUALS expression)?
    ;

/**
 * TYPE ANNOTATION
 * Built-in types for quantum, classical, and molecular computing
 */
typeAnnotation
    : 'qubit'
    | 'qubit' LBRACKET NUMBER RBRACKET                  // qubit[N]
    | 'bit'
    | 'bit' LBRACKET NUMBER RBRACKET                    // bit[N]
    | 'int'
    | 'float'
    | 'bool'
    | 'string'
    | 'void'
    | 'gate'
    | 'circuit'
    | 'plasmid'
    | 'sequence'
    | IDENTIFIER                                         // User-defined types
    ;

/**
 * FUNCTION DECLARATION
 * Syntax: function name(param1: Type, param2: Type) -> ReturnType { body }
 */
functionDeclaration
    : FUNCTION IDENTIFIER LPAREN parameterList? RPAREN ARROW typeAnnotation LBRACE statement* RBRACE
    ;

/**
 * PARAMETER LIST
 * Comma-separated function parameters with types
 */
parameterList
    : parameter (COMMA parameter)*
    ;

parameter
    : IDENTIFIER COLON typeAnnotation
    ;

/**
 * CONTROL FLOW STATEMENTS
 */

ifStatement
    : IF LPAREN expression RPAREN blockStatement (ELSE blockStatement)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN blockStatement
    ;

forStatement
    : FOR LPAREN variableDeclaration SEMICOLON expression SEMICOLON expressionStatement RPAREN blockStatement
    ;

blockStatement
    : LBRACE statement* RBRACE
    ;

returnStatement
    : RETURN expression?
    ;

expressionStatement
    : expression
    ;

/**
 * EXPRESSION: Evaluates to a value
 * Supports arithmetic, logical, and comparison operations
 */
expression
    : logicalOrExpression
    ;

logicalOrExpression
    : logicalAndExpression (OR logicalAndExpression)*
    ;

logicalAndExpression
    : bitwiseOrExpression (AND bitwiseOrExpression)*
    ;

bitwiseOrExpression
    : bitwiseXorExpression (PIPE bitwiseXorExpression)*
    ;

bitwiseXorExpression
    : bitwiseAndExpression (CARET bitwiseAndExpression)*
    ;

bitwiseAndExpression
    : equalityExpression (AMP equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQ | NE) relationalExpression)*
    ;

relationalExpression
    : additiveExpression ((LT | GT | LE | GE) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : powerExpression ((STAR | SLASH | PERCENT) powerExpression)*
    ;

powerExpression
    : unaryExpression (POWER unaryExpression)*
    ;

unaryExpression
    : (MINUS | NOT | TILDE) unaryExpression
    | postfixExpression
    ;

postfixExpression
    : primaryExpression (postfixOperator)*
    ;

postfixOperator
    : LBRACKET expression RBRACKET                      // Array indexing
    | LPAREN argumentList? RPAREN                        // Function call
    | DOT IDENTIFIER                                     // Member access
    ;

primaryExpression
    : NUMBER
    | STRING
    | IDENTIFIER
    | TRUE
    | FALSE
    | LPAREN expression RPAREN
    | quantumGateCall
    | arrayLiteral
    | objectLiteral
    ;

/**
 * FUNCTION CALL / ARGUMENT LIST
 */
argumentList
    : argument (COMMA argument)*
    ;

argument
    : expression
    | IDENTIFIER EQUALS expression                       // Named argument
    ;

/**
 * ARRAY & OBJECT LITERALS
 */
arrayLiteral
    : LBRACKET (expression (COMMA expression)*)? RBRACKET
    ;

objectLiteral
    : LBRACE (objectProperty (COMMA objectProperty)*)? RBRACE
    ;

objectProperty
    : IDENTIFIER COLON expression
    ;

/**
 * QUANTUM OPERATIONS
 * Syntax: operation(args)
 * Examples: init(5), hadamard(q0), cnot(q0, q1), measure(q0)
 */
quantumOperation
    : initOperation
    | singleQubitGate
    | twoQubitGate
    | threeQubitGate
    | measureOperation
    | rotationGate
    ;

initOperation
    : INIT LPAREN NUMBER RPAREN                         // init(5) -> 5 qubits
    | INIT LPAREN IDENTIFIER RPAREN                     // init(num_qubits)
    ;

/**
 * QUANTUM GATE CALL
 * Used in expressions or standalone statements
 */
quantumGateCall
    : singleQubitGate
    | twoQubitGate
    | threeQubitGate
    | measureOperation
    | rotationGate
    ;

/**
 * SINGLE QUBIT GATES
 * Syntax: gate(qubit)
 */
singleQubitGate
    : (HADAMARD | PAULI_X | PAULI_Y | PAULI_Z | T_GATE | S_GATE) LPAREN qubitRef RPAREN
    ;

/**
 * TWO QUBIT GATES
 * Syntax: gate(control, target)
 */
twoQubitGate
    : (CNOT | SWAP | CPHASE) LPAREN qubitRef COMMA qubitRef RPAREN
    ;

/**
 * THREE QUBIT GATES
 * Syntax: gate(control1, control2, target)
 */
threeQubitGate
    : TOFFOLI LPAREN qubitRef COMMA qubitRef COMMA qubitRef RPAREN
    ;

/**
 * ROTATION GATES
 * Syntax: gate(qubit, angle)
 * Angle in radians or degrees
 */
rotationGate
    : (RX | RY | RZ) LPAREN qubitRef COMMA expression RPAREN
    ;

/**
 * MEASURE OPERATION
 * Syntax: measure(qubit) or measure(qubit_array)
 */
measureOperation
    : MEASURE LPAREN qubitRef RPAREN
    | MEASURE LPAREN qubitRef COMMA bitRef RPAREN
    ;

/**
 * QUBIT & BIT REFERENCES
 * q0, q1, b0, etc.
 */
qubitRef
    : IDENTIFIER                                         // q0, q1, qubits, etc.
    | IDENTIFIER LBRACKET NUMBER RBRACKET               // q0[5], array indexing
    | IDENTIFIER LBRACKET IDENTIFIER RBRACKET           // q0[i], dynamic indexing
    ;

bitRef
    : IDENTIFIER                                         // b0, b1, bits, etc.
    | IDENTIFIER LBRACKET NUMBER RBRACKET               // b0[5], array indexing
    ;

/**
 * MOLECULAR OPERATIONS
 * DNA assembly, PCR, CRISPR/Cas9 operations
 */
molecularOperation
    : goldenGateOperation
    | pcrOperation
    | crisprOperation
    | digestOperation
    | ligateOperation
    ;

/**
 * GOLDEN GATE ASSEMBLY
 * Syntax: golden_gate(parts, overhangs)
 */
goldenGateOperation
    : GOLDEN_GATE LPAREN expression (COMMA expression)* RPAREN
    ;

/**
 * PCR (Polymerase Chain Reaction)
 * Syntax: pcr(template, primers, cycles)
 */
pcrOperation
    : PCR LPAREN expression (COMMA expression)* RPAREN
    ;

/**
 * CRISPR/Cas9
 * Syntax: crispr(target, guide_rna, donor_dna)
 */
crisprOperation
    : CRISPR LPAREN expression (COMMA expression)* RPAREN
    ;

/**
 * DIGEST (Restriction enzyme digestion)
 * Syntax: digest(plasmid, enzyme)
 */
digestOperation
    : DIGEST LPAREN expression (COMMA expression)* RPAREN
    ;

/**
 * LIGATE (DNA ligation)
 * Syntax: ligate(fragment1, fragment2)
 */
ligateOperation
    : LIGATE LPAREN expression (COMMA expression)* RPAREN
    ;

// ============================================================================
// END OF GRAMMAR
// ============================================================================
