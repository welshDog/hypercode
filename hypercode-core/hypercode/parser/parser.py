import re
from typing import List, Optional, Tuple, Set
from hypercode.ast.nodes import (
    Program, Statement, DataDecl, SetStmt, PrintStmt, CheckStmt, Block,
    Expr, Literal, Variable, BinaryOp,
    QGate, QMeasure, QuantumCircuitDecl, QuantumOp
)

class Token:
    def __init__(self, type_: str, value: str, line: int, col: int):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    TOKEN_TYPES = [
        ('COMMENT', r'#.*'),
        ('AT_DATA', r'@data'),
        ('AT_SET', r'@set'),
        ('AT_PRINT', r'@print'),
        ('AT_CHECK', r'@check'),
        ('AT_QUANTUM', r'@quantum'),
        ('AT_END', r'@end'),
        ('ARROW', r'->'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('COMMA', r','),
        ('COLON', r':'),
        ('OP', r'(==|>=|<=|>|<|\+|\-|/|\*)'),
        ('QREF', r'q\d+'),  # Matches q0, q1, q99
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
                        # Handle keywords that might be lexed as identifiers if we aren't careful
                        # But since our regexes are ordered, keywords come first.
                        # Wait, 'MEASURE' is not a keyword token, it's an IDENTIFIER in this list.
                        # We'll handle it in the parser or promote it here.
                        # Actually let's just let it be IDENTIFIER and check value in parser.
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
                raise SyntaxError(f"Unexpected character '{self.text[self.pos]}' at line {self.line}, col {self.col}")
                
        return tokens

class Parser:
    GATES = {"H", "X", "Y", "Z", "CX", "CZ", "RX", "RY", "RZ"}

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
        actual = token.type if token else "EOF"
        raise SyntaxError(f"Expected {expected}, got {actual} at line {token.line if token else 'EOF'}")
    
    def match(self, type_: str) -> bool:
        token = self.current()
        if token and token.type == type_:
            self.pos += 1
            return True
        return False

    def parse(self) -> Program:
        statements = []
        while self.current():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Statement:
        token = self.current()
        if token.type == 'AT_DATA':
            return self.parse_data_decl()
        elif token.type == 'AT_SET':
            return self.parse_set_stmt()
        elif token.type == 'AT_PRINT':
            return self.parse_print_stmt()
        elif token.type == 'AT_CHECK':
            return self.parse_check_stmt()
        elif token.type == 'AT_QUANTUM':
            return self.parse_quantum_circuit()
        else:
            raise SyntaxError(f"Unexpected token {token.type} ({token.value}) at start of statement")

    def parse_data_decl(self) -> DataDecl:
        self.consume('AT_DATA')
        name = self.consume('IDENTIFIER').value
        self.consume('COLON')
        value = self.parse_expr()
        return DataDecl(name, value)

    def parse_set_stmt(self) -> SetStmt:
        self.consume('AT_SET')
        name = self.consume('IDENTIFIER').value
        self.consume('COLON')
        value = self.parse_expr()
        return SetStmt(name, value)

    def parse_print_stmt(self) -> PrintStmt:
        self.consume('AT_PRINT')
        self.consume('LPAREN')
        expr = self.parse_expr()
        self.consume('RPAREN')
        return PrintStmt(expr)

    def parse_check_stmt(self) -> CheckStmt:
        self.consume('AT_CHECK')
        self.consume('LPAREN')
        condition = self.parse_expr()
        self.consume('RPAREN')
        self.consume('ARROW')
        
        self.consume('LBRACE')
        # Simplification for v0: Just a list of statements
        block_content = self.parse_block_body()
        return CheckStmt(condition, block_content)

    def parse_block_body(self) -> Block:
        stmts = []
        while self.current() and self.current().type != 'RBRACE':
            stmts.append(self.parse_statement())
        self.consume('RBRACE')
        return Block(stmts)

    # --- Quantum Parsing ---

    def parse_quantum_circuit(self) -> QuantumCircuitDecl:
        self.consume('AT_QUANTUM')
        name = self.consume('IDENTIFIER').value
        
        # Expect 'qubits' keyword (lexed as IDENTIFIER)
        token = self.consume('IDENTIFIER')
        if token.value != 'qubits':
            raise SyntaxError(f"Expected 'qubits', got '{token.value}'")
            
        qubits_count_token = self.consume('NUMBER')
        qubits_count = int(float(qubits_count_token.value)) # Handle 2.0 if typed, though int expected

        ops = []
        while self.current() and self.current().type != 'AT_END':
            # Skip newlines implicitly handled by lexer (WHITESPACE skips)
            # But wait, our lexer skips whitespace/newlines.
            # So we just check for tokens.
            
            token = self.current()
            if token.type == 'IDENTIFIER':
                if token.value == 'MEASURE':
                    ops.append(self.parse_qmeasure())
                elif token.value in self.GATES:
                    ops.append(self.parse_qgate())
                else:
                    raise SyntaxError(f"Unknown quantum operation or gate: {token.value}")
            else:
                 raise SyntaxError(f"Expected gate or MEASURE, got {token.type}")

        self.consume('AT_END')
        return QuantumCircuitDecl(name, qubits_count, ops)

    def parse_qgate(self) -> QGate:
        name_token = self.consume('IDENTIFIER')
        gate_name = name_token.value
        
        # Parse params if present: gate(param) q0
        # OR as per user sketch: GATENAME qref+ param_list?
        # User sketch: H q0; RZ(pi) q0
        # Let's support both for flexibility, but prioritize sketch: RZ(pi) q0 makes sense?
        # Wait, user sketch says: gate_op := GATENAME qref+ param_list?
        # BUT example says: H q0
        # Example for parameterized? The user asked: "Want the syntax to allow inline params like RZ(PI/2) q0?"
        # Let's assume standard is GATENAME (params)? qrefs
        
        # Check for optional params
        params = []
        if self.current().type == 'LPAREN':
            self.consume('LPAREN')
            params.append(self.parse_expr())
            while self.match('COMMA'):
                params.append(self.parse_expr())
            self.consume('RPAREN')

        qubits = []
        while self.current() and self.current().type == 'QREF':
            q_token = self.consume('QREF')
            # q0 -> 0
            q_idx = int(q_token.value[1:])
            qubits.append(q_idx)
        
        if not qubits:
            raise SyntaxError(f"Gate {gate_name} requires at least one qubit")

        return QGate(gate_name, qubits, params)

    def parse_qmeasure(self) -> QMeasure:
        # MEASURE q0 -> c0
        self.consume('IDENTIFIER') # MEASURE (already checked)
        
        q_token = self.consume('QREF')
        q_idx = int(q_token.value[1:])
        
        target = None
        if self.match('ARROW'):
            target_token = self.consume('IDENTIFIER')
            target = target_token.value
            
        return QMeasure(q_idx, target)

    # --- Expression Parsing ---

    def parse_expr(self) -> Expr:
        left = self.parse_term()
        
        if self.current() and self.current().type == 'OP':
            op = self.consume('OP').value
            right = self.parse_term()
            return BinaryOp(left, op, right)
        
        return left

    def parse_term(self) -> Expr:
        token = self.current()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            val = float(token.value)
            if val.is_integer():
                val = int(val)
            return Literal(val)
        elif token.type == 'STRING':
            self.consume('STRING')
            return Literal(token.value.strip('"'))
        elif token.type == 'IDENTIFIER':
            self.consume('IDENTIFIER')
            return Variable(token.value)
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expr()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")

def parse(code: str) -> Program:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
