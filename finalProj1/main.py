from Interpeter import Interpreter
from Lexer import Lexer
from Parser import Parser


def main():
    while True:
        try:
            try:
                text = input('> ')
            except NameError:  # Python3
                text = input('> ')
        except EOFError:
            break
        if not text:
            continue
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(f"Error: {e}")




if __name__ == '__main__':
    main()

# BNF:

# FACTOR : INTEGER | BOOLEAN | LPAREN BOOLEAN_EXPR RPAREN | LPAREN LAMBDA_EXPRESSION RPAREN | LPAREN LAMBDA_EXPRESSION RPAREN LAMBDA_CALL | FUNCTION_CALL | IF_STATEMENT
# TERM : FACTOR (( MUL | DIV | MOD ) FACTOR)*
# EXPR : TERM ((PLUS | MINUS) TERM)*
# COMPARISON_EXPR : EXPR (( GT | LT | EQEQ | NEQ | GTE | LTE) EXPR)*
# BOOLEAN_EXPR : COMPARISON_EXPR ((AND|OR) COMPARISON_EXPR)*
# STATEMENT : FUNC FUNCTION_DECLARATION | BLOCK | BOOLEAN_EXPR SEMI
# STATEMENT_LIST : STATEMENT* ( RBRACE | EOF )
# ARGUMENT_LIST : BOOLEAN_EXPR (COMMA BOOLEAN_EXPR)*
# BLOCK : LBRACE STATEMENT_LIST RBRACE
# IF_STATEMENT : IF BOOLEAN_EXPR THEN BLOCK (ELIF BOOLEAN_EXPR THEN BLOCK)* (ELSE BLOCK)?
# PARAMETER_LIST : ID (COMMA ID)*
# FUNCTION_DECLARATION : FUNC ID LPAREN PARARMETER_LIST RPAREN BLOCK
# FUNCTION_CALL : ID LPAREN argument_list RPAREN
# LAMBDA_EXPRESSION : LAMBDA parameter_list COLON block
# LAMBDA_CALL : LPAREN argument_list RPAREN
# INTEGER : (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0) (INTEGER)*
# BOOLEAN : 'TRUE' | 'FALSE'
# PLUS : '+'
# MINUS : '-'
# MUL : '*'
# DIV : '/'
# MOD : '%'
# LPAREN : '('
# RPAREN : ')'
# LBRACE : '{'
# RBRACE : '}'
# AND : 'AND'
# OR : 'OR'
# GT : '>'
# LT : '<'
# GTE : '>='
# LTE : '<='
# EQEQ : '=='
# NEQ : '!='
# SEMI : ';'
# COMMA : ','
# IF : 'IF'
# THEN : 'THEN'
# ELIF : 'ELIF'
# ELSE : 'ELSE'
# ID : (a-z | A-Z) (ID | INTEGER)*
# EOF : ''

