import Interpeter
import Lexer
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################
# from Lexer import Lexer
# from Parser import Parser

# global_Var = {}
function_table = {}





class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.function_table = function_table;

    def visit(self, node):

        # if the node is a list of statements, visit each statement in turn
        if isinstance(node, list):
            results = []
            for statement in node:
                result = self.visit(statement)
                if result is not None:
                    results.append(result)
            return results

        # otherwise visit the node by its type (get method name visit_NODENAME at runtime)

        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    # if node has no corresponding visit_node function

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    # visit functions for various nodes

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        # Check if either operand is a function call and evaluate accordingly
        if callable(left):
            left = left()
        if callable(right):
            right = right()



        if isinstance(left, list) and len(left) > 1:
            raise Exception("Error: Left operand has more than one value.")
        if isinstance(right, list) and len(right) > 1:
            raise Exception("Error: Right operand has more than one value.")

        if isinstance(left, list) and len(left) == 1:
            while isinstance(left, list):
                left = left[0]

        if isinstance(right, list) and len(right) == 1:
            while isinstance(right, list):
                right = right[0]

        if node.op.type == 'PLUS':
            return left + right
        elif node.op.type == 'MINUS':
            return left - right
        elif node.op.type == 'MUL':
            return left * right
        elif node.op.type == 'DIV':
            return int(left / right)
        elif node.op.type == 'MOD':
            return left % right
        elif node.op.type == 'GT':
            return left > right
        elif node.op.type == 'LT':
            return left < right
        elif node.op.type == 'EQEQ':
            return left == right
        elif node.op.type == 'NEQ':
            return left != right
        elif node.op.type == 'GTE':
            return left >= right
        elif node.op.type == 'LTE':
            return left <= right
        elif node.op.type == 'AND':
            return left and right
        elif node.op.type == 'OR':
            return left or right

    def visit_Num(self, node):
        return node.value

    def visit_ID(self, node):
        if hasattr(self, 'local_scope') and node.name in self.local_scope:
            return self.local_scope[node.name]
        # if node.name in global_Var:
        #     return global_Var[node.name]
        elif node.name in function_table:
            return function_table[node.name]

    # def visit_Assign(self, node):
    #     name = node.id
    #     expr = self.visit(node.expr)
    #     global_Var[name] = expr

    def visit_If(self, node):
        if self.visit(node.condition):
            return self.visit(node.true_block)
        for elif_condition, elif_block in node.elif_blocks:
            if self.visit(elif_condition):
                return self.visit(elif_block)
        if node.false_block:
            return self.visit(node.false_block)

    def visit_FunctionDeclaration(self, node):
        # save function to function table
        self.function_table[node.name] = node

    def visit_FunctionCall(self, node):
        function = self.function_table.get(node.name)
        if not function:
            raise Exception(f"Function '{node.name}' not found")

        if len(node.args) != len(function.params):
            raise Exception(
                f"Function '{node.name}' expected {len(function.params)} arguments but got {len(node.args)}")

        # Evaluate arguments
        evaluated_args = [self.visit(arg) for arg in node.args]

        local_vars = {param: value for param, value in zip(function.params, evaluated_args)}

        # Save and set local scope for function execution
        previous_scope = getattr(self, 'local_scope', {})
        self.local_scope = local_vars

        result = []
        for statement in function.block:
            result.append(self.visit(statement))

        self.local_scope = previous_scope
        return result

    def visit_LambdaExpression(self, node):
        def lambda_function(*args):
            if len(args) != len(node.params):
                raise Exception(f"Expected {len(node.params)} arguments but got {len(args)}")

            local_vars = {param: arg for param, arg in zip(node.params, args)}

            previous_scope = self.local_scope if hasattr(self, 'local_scope') else {}
            self.local_scope = local_vars

            result = self.visit(node.body)

            self.local_scope = previous_scope
            return result

        return lambda_function

    def visit_LambdaCall(self, node):
        lambda_function = self.visit(node.lambda_expr)

        if not callable(lambda_function):
            raise Exception("Expected a lambda function")

        evaluated_args = [self.visit(arg) for arg in node.args]

        return lambda_function(*evaluated_args)

    # create AST and visit its root

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

