# Generated from HyperCode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .HyperCodeParser import HyperCodeParser
else:
    from HyperCodeParser import HyperCodeParser

# This class defines a complete generic visitor for a parse tree produced by HyperCodeParser.

class HyperCodeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HyperCodeParser#program.
    def visitProgram(self, ctx:HyperCodeParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#functionDef.
    def visitFunctionDef(self, ctx:HyperCodeParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#type.
    def visitType(self, ctx:HyperCodeParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#block.
    def visitBlock(self, ctx:HyperCodeParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#statement.
    def visitStatement(self, ctx:HyperCodeParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#circuitStmt.
    def visitCircuitStmt(self, ctx:HyperCodeParser.CircuitStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#letStmt.
    def visitLetStmt(self, ctx:HyperCodeParser.LetStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#returnStmt.
    def visitReturnStmt(self, ctx:HyperCodeParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#exprStmt.
    def visitExprStmt(self, ctx:HyperCodeParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#expr.
    def visitExpr(self, ctx:HyperCodeParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#functionCall.
    def visitFunctionCall(self, ctx:HyperCodeParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#domainDirective.
    def visitDomainDirective(self, ctx:HyperCodeParser.DomainDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HyperCodeParser#backendDirective.
    def visitBackendDirective(self, ctx:HyperCodeParser.BackendDirectiveContext):
        return self.visitChildren(ctx)



del HyperCodeParser