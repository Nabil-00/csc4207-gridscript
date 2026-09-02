from src.ast_nodes import (
    Program, Assign, Print, If, While, FunctionDef, Return,
    Call, BinaryOp, UnaryOp, Literal, Variable,
)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def error(self, msg):
        tok = self.peek()
        raise ParseError(f"{tok.line}:{tok.column}: {msg}")

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_, value=None):
        tok = self.peek()
        if value is not None:
            if tok.type != type_ or tok.value != value:
                self.error(f"expected '{value}', got '{tok.value}'")
        elif tok.type != type_:
            self.error(f"expected {type_}, got {tok.type} ({tok.value})")
        return self.advance()

    def parse(self):
        statements = self.parse_block(['EOF'])
        self.expect('EOF')
        return Program(statements)

    def parse_block(self, terminators):
        statements = []
        while self.peek().type != 'EOF':
            if self.peek().value in terminators:
                break
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements

    def parse_statement(self):
        tok = self.peek()
        if tok.type == 'KEYWORD':
            if tok.value == 'set':
                return self.parse_assignment()
            elif tok.value == 'print':
                return self.parse_print()
            elif tok.value == 'if':
                return self.parse_if()
            elif tok.value == 'while':
                return self.parse_while()
            elif tok.value == 'def':
                return self.parse_function_def()
            elif tok.value == 'return':
                return self.parse_return()
            elif tok.value in ('else', 'end', 'then', 'do'):
                self.error(f"unexpected '{tok.value}'")
        elif tok.type == 'IDENT':
            name = self.advance().value
            if self.peek().type == 'LPAREN':
                return self.parse_call_inner(name)
            self.error(f"expected '(' after function name, got '{self.peek().value}'")
        self.error(f"unexpected token '{tok.value}'")

    def parse_assignment(self):
        self.expect('KEYWORD', 'set')
        name = self.expect('IDENT').value
        self.expect('OP', '=')
        expr = self.parse_expression()
        return Assign(name, expr)

    def parse_print(self):
        self.expect('KEYWORD', 'print')
        expr = self.parse_expression()
        return Print(expr)

    def parse_if(self):
        self.expect('KEYWORD', 'if')
        condition = self.parse_expression()
        self.expect('KEYWORD', 'then')
        then_body = self.parse_block(['else', 'end'])
        else_body = []
        if self.peek().value == 'else':
            self.advance()
            else_body = self.parse_block(['end'])
        self.expect('KEYWORD', 'end')
        return If(condition, then_body, else_body)

    def parse_while(self):
        self.expect('KEYWORD', 'while')
        condition = self.parse_expression()
        self.expect('KEYWORD', 'do')
        body = self.parse_block(['end'])
        self.expect('KEYWORD', 'end')
        return While(condition, body)

    def parse_function_def(self):
        self.expect('KEYWORD', 'def')
        name = self.expect('IDENT').value
        self.expect('LPAREN')
        params = self.parse_param_list()
        self.expect('RPAREN')
        body = self.parse_block(['end'])
        self.expect('KEYWORD', 'end')
        return FunctionDef(name, params, body)

    def parse_return(self):
        self.expect('KEYWORD', 'return')
        expr = self.parse_expression()
        return Return(expr)

    def parse_call_inner(self, name):
        self.expect('LPAREN')
        args = self.parse_arg_list()
        self.expect('RPAREN')
        return Call(name, args)

    def parse_param_list(self):
        params = []
        if self.peek().type == 'IDENT':
            params.append(self.advance().value)
            while self.peek().type == 'COMMA':
                self.advance()
                params.append(self.expect('IDENT').value)
        return params

    def parse_arg_list(self):
        args = []
        if self.peek().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.peek().type == 'COMMA':
                self.advance()
                args.append(self.parse_expression())
        return args

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_arithmetic()
        if self.peek().type == 'OP' and self.peek().value in ('==', '!=', '<', '>'):
            op = self.advance().value
            right = self.parse_arithmetic()
            return BinaryOp(op, left, right)
        return left

    def parse_arithmetic(self):
        left = self.parse_term()
        while self.peek().type == 'OP' and self.peek().value in ('+', '-'):
            op = self.advance().value
            right = self.parse_term()
            left = BinaryOp(op, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek().type == 'OP' and self.peek().value in ('*', '/'):
            op = self.advance().value
            right = self.parse_factor()
            left = BinaryOp(op, left, right)
        return left

    def parse_factor(self):
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.advance()
            return Literal(int(tok.value))
        elif tok.type == 'STRING':
            self.advance()
            return Literal(tok.value[1:-1])
        elif tok.type == 'KEYWORD' and tok.value == 'true':
            self.advance()
            return Literal(True)
        elif tok.type == 'KEYWORD' and tok.value == 'false':
            self.advance()
            return Literal(False)
        elif tok.type == 'IDENT':
            name = self.advance().value
            if self.peek().type == 'LPAREN':
                return self.parse_call_inner(name)
            return Variable(name)
        elif tok.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        elif tok.type == 'OP' and tok.value == '-':
            self.advance()
            operand = self.parse_factor()
            return UnaryOp('-', operand)
        self.error(f"unexpected token '{tok.value}'")