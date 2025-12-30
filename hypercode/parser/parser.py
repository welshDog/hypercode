"""HyperCode parser implementation."""
from pathlib import Path
import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

# Import generated parser
from .HyperCodeLexer import HyperCodeLexer
from .HyperCodeParser import HyperCodeParser
from .HyperCodeVisitor import HyperCodeVisitor

from ..ast import *


class HyperCodeParserError(Exception):
    """Custom exception for parser errors."""
    pass


class HyperCodeVisitor(HyperCodeVisitor):
    """Visitor that builds an AST from the parse tree."""
    
    def __init__(self):
        super().__init__()
        self._current_function = None
        self._current_circuit = None
    
    def visitProgram(self, ctx):
        """Visit a program node."""
        functions = []
        directives = []
        
        for child in ctx.getChildren():
            if hasattr(child, 'accept'):
                result = child.accept(self)
                if isinstance(result, Function):
                    functions.append(result)
                elif isinstance(result, tuple) and len(result) == 2:
                    directives.append(result)
        
        return Program(functions=functions, directives=directives)
    
    def visitFunctionDef(self, ctx):
        """Visit a function definition."""
        try:
            # Check if it's a quantum function by looking for the @quantum_function decorator
            is_quantum = any(
                child.getText().startswith('@quantum_function') 
                for child in ctx.getChildren() 
                if hasattr(child, 'getText')
            )
            
            name = ctx.IDENTIFIER().getText() if ctx.IDENTIFIER() else "<anonymous>"
            
            # Handle return type
            return_type = Type('Void')
            if hasattr(ctx, 'type_') and ctx.type_():
                return_type = self.visitType(ctx.type_())
            
            # Handle parameters
            parameters = []
            if hasattr(ctx, 'parameterList') and ctx.parameterList():
                parameters = self.visitParameterList(ctx.parameterList())
            
            # Handle function body
            body = []
            if hasattr(ctx, 'block') and ctx.block():
                body = self.visitBlock(ctx.block())
            
            # Create and return the function node
            function_node = Function(
                name=name,
                is_quantum=is_quantum,
                parameters=parameters,
                return_type=return_type,
                body=body
            )
            
            # Store the current function context for nested function support
            self._current_function = function_node
            return function_node
            
        except Exception as e:
            line = ctx.start.line if hasattr(ctx, 'start') and ctx.start else 'unknown'
            raise HyperCodeParserError(f"Error in function definition at line {line}: {str(e)}")
    
    def visitType(self, ctx):
        """Visit a type node."""
        if not ctx:
            return Type('Void')
        return Type(ctx.getText())


def parse(source: str) -> Program:
    """Parse HyperCode source code into an AST."""
    input_stream = InputStream(source)
    lexer = HyperCodeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HyperCodeParser(stream)
    
    # Parse the input
    tree = parser.program()
    
    # Create visitor and visit the parse tree
    visitor = HyperCodeVisitor()
    return visitor.visit(tree)
