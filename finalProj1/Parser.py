from Interpeter import Interpreter
from Lexer import Lexer


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class ID(AST):
    def __init__(self,name):
        self.name = name

class Assign(AST):
    def __init__(self,id ,expr ):
        self.id = id
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
class If(AST):
    def __init__(self, condition, true_block, elif_blocks, false_block):
        self.condition = condition
        self.true_block = true_block
        self.elif_blocks = elif_blocks if elif_blocks is not None else []
        self.false_block = false_block

class FunctionDeclaration(AST):
    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block = block

class FunctionCall(AST):
    def __init__(self, name, args):
        self.name = name
        self.args = args
class LambdaCall(AST):
    def __init__(self, lambda_expr, args):
        self.lambda_expr = lambda_expr
        self.args = args
class LambdaExpression(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()


    def factor(self):

        token = self.current_token
        if token.type == 'INTEGER':
            self.eat('INTEGER')
            return Num(token)
        elif token.type == 'BOOLEAN':
            self.eat('BOOLEAN')
            return Num(token)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            if self.current_token.type == 'LAMBDA':
                lambda_node = self.lambda_expression()
                self.eat('RPAREN')
                if self.current_token.type == 'LPAREN':
                    return self.lambda_call(lambda_node)
                return lambda_node
            node = self.boolean_expr()
            self.eat('RPAREN')
            return node
        elif token.type == 'ID':
            if self.peek().type == 'LPAREN':
                return self.function_call()
            id = token.value
            self.eat('ID')
            return ID(id)
        elif token.type == 'IF':
            return self.if_statement()

        else:
            self.error(token)


    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in ('MUL', 'DIV', 'MOD'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
            elif token.type == 'DIV':
                self.eat('DIV')
            elif token.type == 'MOD':
                self.eat('MOD')

            node = BinOp(left=node, op=token, right=self.factor())

        return node



    def expr(self):

        node = self.term()

        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')

            node = BinOp(left=node, op=token, right=self.term())

        return node


    def comparison_expr(self):
        """comparison_expr : expr ((GT | LT) expr)*"""
        node = self.expr()

        while self.current_token.type in ('GT', 'LT', 'EQEQ', 'NEQ', 'GTE', 'LTE'):
            token = self.current_token
            if token.type == 'GT':
                self.eat('GT')
            elif token.type == 'LT':
                self.eat('GT')
            elif token.type == 'EQEQ':
                self.eat('EQEQ')
            elif token.type == 'NEQ':
                self.eat('NEQ')
            elif token.type == 'GTE':
                self.eat('GTE')
            elif token.type == 'LTE':
                self.eat('LTE')

            node = BinOp(left=node, op=token, right=self.expr())

        return node


    def boolean_expr(self):
        """boolean_expr : comparison_expr ((AND | OR) comparison_expr)*"""
        node = self.comparison_expr()

        while self.current_token.type in ('AND', 'OR'):
            token = self.current_token
            if token.type == 'AND':
                self.eat('AND')
            elif token.type == 'OR':
                self.eat('OR')

            node = BinOp(left=node, op=token, right=self.comparison_expr())

        return node


    def statement(self):
        """statement : if_statement | function_dec | assign statement | func call | boolean_expr SEMI"""
        if self.current_token.type == 'FUNC':
            return self.function_declaration()
        elif self.current_token.type == 'ID':
            if self.peek().type == 'EQ':
                return self.assignment_statement()
        elif self.current_token.type == 'LBRACE':
            return self.block()
        node = self.boolean_expr()
        if self.current_token.type == 'SEMI':
            self.eat('SEMI')
        else:
            self.error()
        return node



    def statement_list(self):
        statements = []

        while self.current_token.type not in ('RBRACE', 'EOF'):
                statements.append(self.statement())  # נתח פקודה בודדת

        return statements

    def peek(self):

        current_pos = self.lexer.pos
        current_char = self.lexer.current_char

        next_token = self.lexer.get_next_token()

        self.lexer.pos = current_pos
        self.lexer.current_char = current_char

        return next_token

    #
    # def assignment_statement(self):
    #     """assignment_statement : ID ASSIGN boolean_expr SEMI"""
    #     id = self.current_token.value
    #     self.eat('ID')
    #     self.eat('EQ')
    #     expr = self.statement()
    #     return Assign(id,expr)


    # def variable(self):
    #     node = ID(self.current_token)
    #     self.eat('ID')
    #     return node



    def block(self):

        self.eat('LBRACE')
        statements = self.statement_list()
        self.eat('RBRACE')
        return statements


    def if_statement(self):
        """if_statement : IF boolean_expr THEN statement (ELSE statement)?"""
        self.eat('IF')

        condition = self.boolean_expr()

        self.eat('THEN')
        true_block = self.block()

        elif_blocks = []
        while self.current_token.type == 'ELIF':
            self.eat('ELIF')
            elif_condition = self.boolean_expr()
            self.eat('THEN')
            elif_block = self.block()
            elif_blocks.append((elif_condition, elif_block))
        false_block = None
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            false_block = self.block()

        return If(condition, true_block, elif_blocks, false_block)


    def parameter_list(self):

        params = []
        if self.current_token.type == 'ID':
            params.append(self.current_token.value)
            self.eat('ID')

        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            params.append(self.current_token.value)
            self.eat('ID')

        return params


    def function_declaration(self):

        self.eat('FUNC')
        func_name = self.current_token.value
        self.eat('ID')
        self.eat('LPAREN')
        parameters = self.parameter_list()
        self.eat('RPAREN')
        block = self.block()
        return FunctionDeclaration(func_name, parameters, block)

    def argument_list(self):
        """argument_list : expr (COMMA expr)*"""
        args = []
        if self.current_token.type != 'RPAREN':
            args.append(self.boolean_expr())

        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            args.append(self.boolean_expr())

        return args

    def function_call(self):
        """function_call : ID LPAREN argument_list RPAREN"""
        name = self.current_token.value
        self.eat('ID')
        self.eat('LPAREN')
        args = self.argument_list()
        self.eat('RPAREN')
        return FunctionCall(name, args)


    def lambda_expression(self):
        """lambda_expression : LAMBDA parameter_list COLON expr"""
        self.eat('LAMBDA')
        params = self.parameter_list()
        self.eat('COLON')
        body = self.block()
        return LambdaExpression(params, body)


    def lambda_call(self, lambda_expr):
        """Handle calling a lambda function directly"""
        self.eat('LPAREN')
        args = self.argument_list()
        self.eat('RPAREN')
        return LambdaCall(lambda_expr, args)

    def parse(self):
        return self.statement_list()


