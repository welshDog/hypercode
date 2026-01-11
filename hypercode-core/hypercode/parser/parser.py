import re
from typing import List, Optional
from hypercode.ast.nodes import (
    Program, Statement,
    Expr, Literal, Variable,
    QGate, QMeasure, QuantumCircuitDecl, Directive, QRegDecl, QubitRef
)

class Token:
    def __init__(self, type_: str, value: str, line: int, col: int):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self) -> str:
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    TOKEN_TYPES = [
        ('DIRECTIVE', r'#:\s*\w+'), # #:domain, #:backend
        ('COMMENT', r'#.*'),
        ('AT_CMD', r'@\w+'),        # @circuit, @init, @hadamard, etc.
        ('ARROW', r'->'),
        ('LBRACK', r'\['),
        ('RBRACK', r'\]'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('COMMA', r','),
        ('COLON', r':'),
        ('ASSIGN', r'='),
        ('OP', r'(==|>=|<=|>|<|\+|\-|/|\*)'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('STRING', r'"[^"]*"'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('WHITESPACE', r'[ \t\r\n]+'),
    ]

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
    
    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.text):
            match = None
            for type_, pattern in self.TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    if type_ != 'WHITESPACE' and type_ != 'COMMENT':
                        tokens.append(Token(type_, value, self.line, self.col))
                    
                    # Update position
                    lines = value.count('\n')
                    self.line += lines
                    if lines > 0:
                        self.col = len(value.split('\n')[-1]) + 1
                    else:
                        self.col += len(value)
                    
                    self.pos += len(value)
                    break
            
            if not match:
                # Skip unknown characters (like BOM or weird whitespace)
                # print(f"Warning: Skipping unexpected character '{self.text[self.pos]}'")
                self.pos += 1
                self.col += 1
                
        return tokens

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def peek(self) -> Optional[Token]:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def consume(self, type_: str) -> Token:
        token = self.current()
        if token and token.type == type_:
            self.pos += 1
            return token
        expected = type_
        found = token.type if token else "EOF"
        raise SyntaxError(f"Expected {expected}, found {found} at line {token.line if token else '?'}")

    def parse(self) -> Program:
        statements: List[Statement] = []
        while self.current():
            token = self.current()
            if not token:
                break
                
            if token.type == 'DIRECTIVE':
                statements.append(self.parse_directive())
            elif token.type == 'AT_CMD':
                cmd = token.value
                if cmd == '@circuit':
                    statements.append(self.parse_circuit())
                else:
                    # Top-level statement or error
                    # For now, assume it's part of a global script if valid
                    stmt = self.parse_statement()
                    if stmt:
                        statements.append(stmt)
            else:
                self.pos += 1 # Skip stray tokens? Or raise error?
                # raise SyntaxError(f"Unexpected token {self.current()}")
        return Program(statements=statements)

    def parse_directive(self) -> Directive:
        # #:domain
        token = self.consume('DIRECTIVE')
        kind = token.value.split(':')[1].strip()
        # Expect generic identifier next? 
        # bell_pair.hc: #:domain quantum
        # Lexer sees #:domain as DIRECTIVE. Next token is IDENTIFIER "quantum"
        
        curr = self.current()
        if curr and curr.type == 'COLON': # Handle optional colon
            self.consume('COLON')
             
        value = self.consume('IDENTIFIER').value
        return Directive(kind=kind, value=value)

    def parse_circuit(self) -> QuantumCircuitDecl:
        self.consume('AT_CMD') # @circuit
        self.consume('COLON')
        name = self.consume('IDENTIFIER').value
        
        body: List[Statement] = []
        # Parse until next @circuit or EOF
        while self.current():
            token = self.current()
            if not token:
                break
                
            if token.type == 'AT_CMD' and token.value == '@circuit':
                break
            if token.type == 'DIRECTIVE':
                break # Should directives be inside?
                
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # If stmt is None (e.g. @doc), continue loop

                
        return QuantumCircuitDecl(name=name, body=body)

    def parse_statement(self) -> Optional[Statement]:
        token = self.current()
        if not token: return None
        
        if token.type == 'AT_CMD':
            cmd = token.value
            if cmd == '@doc':
                self.consume('AT_CMD')
                self.consume('COLON')
                self.consume('STRING')
                return None # Ignore doc strings for AST? Or add DocStmt?
            elif cmd == '@init':
                return self.parse_init()
            elif cmd == '@measure':
                return self.parse_measure()
            else:
                return self.parse_gate()
        
        # Fallback for expressions or other statements
        self.pos += 1
        return None

    def parse_init(self) -> QRegDecl:
        self.consume('AT_CMD') # @init
        self.consume('COLON')
        name = self.consume('IDENTIFIER').value
        self.consume('ASSIGN')
        
        type_name = self.consume('IDENTIFIER').value # QReg or CReg
        is_quantum = type_name == 'QReg'
        
        self.consume('LPAREN')
        size = int(self.consume('NUMBER').value)
        self.consume('RPAREN')
        
        return QRegDecl(name=name, size=size, is_quantum=is_quantum)

    def parse_gate(self) -> QGate:
        # @hadamard: q[0]
        # @rz(3.14): q[0]
        gate_token = self.consume('AT_CMD')
        gate_name = gate_token.value[1:] # strip @
        
        params: List[Expr] = []
        curr = self.current()
        if curr and curr.type == 'LPAREN':
            self.consume('LPAREN')
            while True:
                curr_inner = self.current()
                if not curr_inner or curr_inner.type == 'RPAREN':
                    break
                params.append(self.parse_expr())
                if self.current() and self.current().type == 'COMMA': # type: ignore
                    self.consume('COMMA')
            self.consume('RPAREN')
            
        self.consume('COLON')
        
        qubits: List[QubitRef] = []
        qubits.append(self.parse_qubit_ref())
        while self.current() and self.current().type == 'COMMA': # type: ignore
            self.consume('COMMA')
            qubits.append(self.parse_qubit_ref())
            
        return QGate(name=gate_name, qubits=qubits, params=params)

    def parse_measure(self) -> QMeasure:
        # @measure: q -> c
        # Or @measure: q[0] -> c[0]
        self.consume('AT_CMD')
        self.consume('COLON')
        
        source = self.parse_qubit_ref()
        self.consume('ARROW')
        target = self.parse_qubit_ref()
        
        return QMeasure(qubit=source, target=target)

    def parse_qubit_ref(self) -> QubitRef:
        # q or q[0]
        name = self.consume('IDENTIFIER').value
        index = -1 # All?
        
        curr = self.current()
        if curr and curr.type == 'LBRACK':
            self.consume('LBRACK')
            index = int(self.consume('NUMBER').value)
            self.consume('RBRACK')
            
        return QubitRef(register=name, index=index)

    def parse_expr(self) -> Expr:
        # Simple expression parser
        token = self.current()
        if not token:
             raise SyntaxError("Unexpected EOF in expr")
             
        if token.type == 'NUMBER':
            val = float(token.value) if '.' in token.value else int(token.value)
            self.consume('NUMBER')
            return Literal(value=val)
        elif token.type == 'IDENTIFIER':
            # Could be variable or constant like PI
            name = self.consume('IDENTIFIER').value
            curr = self.current()
            if curr and curr.type == 'OP' and curr.value == '/':
                 # Handle PI/2 roughly
                 self.consume('OP')
                 denom_token = self.consume('NUMBER')
                 denom = float(denom_token.value)
                 # Assume name was PI or something
                 return Literal(value=3.14159/denom)
            return Variable(name=name)
        elif token.type == 'STRING':
             val = self.consume('STRING').value
             return Literal(value=val)
        
        raise SyntaxError(f"Unexpected token in expr: {token}")

def parse(text: str) -> Program:
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
