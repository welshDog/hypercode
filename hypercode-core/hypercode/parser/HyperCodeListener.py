# Generated from HyperCode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .HyperCodeParser import HyperCodeParser
else:
    from HyperCodeParser import HyperCodeParser

# This class defines a complete listener for a parse tree produced by HyperCodeParser.
class HyperCodeListener(ParseTreeListener):

    # Enter a parse tree produced by HyperCodeParser#program.
    def enterProgram(self, ctx:HyperCodeParser.ProgramContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#program.
    def exitProgram(self, ctx:HyperCodeParser.ProgramContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#functionDef.
    def enterFunctionDef(self, ctx:HyperCodeParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#functionDef.
    def exitFunctionDef(self, ctx:HyperCodeParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#type.
    def enterType(self, ctx:HyperCodeParser.TypeContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#type.
    def exitType(self, ctx:HyperCodeParser.TypeContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#block.
    def enterBlock(self, ctx:HyperCodeParser.BlockContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#block.
    def exitBlock(self, ctx:HyperCodeParser.BlockContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#statement.
    def enterStatement(self, ctx:HyperCodeParser.StatementContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#statement.
    def exitStatement(self, ctx:HyperCodeParser.StatementContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#circuitStmt.
    def enterCircuitStmt(self, ctx:HyperCodeParser.CircuitStmtContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#circuitStmt.
    def exitCircuitStmt(self, ctx:HyperCodeParser.CircuitStmtContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#letStmt.
    def enterLetStmt(self, ctx:HyperCodeParser.LetStmtContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#letStmt.
    def exitLetStmt(self, ctx:HyperCodeParser.LetStmtContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#returnStmt.
    def enterReturnStmt(self, ctx:HyperCodeParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#returnStmt.
    def exitReturnStmt(self, ctx:HyperCodeParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#exprStmt.
    def enterExprStmt(self, ctx:HyperCodeParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#exprStmt.
    def exitExprStmt(self, ctx:HyperCodeParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#expr.
    def enterExpr(self, ctx:HyperCodeParser.ExprContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#expr.
    def exitExpr(self, ctx:HyperCodeParser.ExprContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#functionCall.
    def enterFunctionCall(self, ctx:HyperCodeParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#functionCall.
    def exitFunctionCall(self, ctx:HyperCodeParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#domainDirective.
    def enterDomainDirective(self, ctx:HyperCodeParser.DomainDirectiveContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#domainDirective.
    def exitDomainDirective(self, ctx:HyperCodeParser.DomainDirectiveContext):
        pass


    # Enter a parse tree produced by HyperCodeParser#backendDirective.
    def enterBackendDirective(self, ctx:HyperCodeParser.BackendDirectiveContext):
        pass

    # Exit a parse tree produced by HyperCodeParser#backendDirective.
    def exitBackendDirective(self, ctx:HyperCodeParser.BackendDirectiveContext):
        pass



del HyperCodeParser