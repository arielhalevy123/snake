###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
(ID, INTEGER, BOOLEAN, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, AND, OR, GT, LT,
    EQ, EQEQ, NEQ, GTE, LTE, SEMI, RBRACE, LBRACE, IF, THEN, ELSE, ELIF, COMMA, COLON, EOF) = (
    'ID', 'INTEGER', 'BOOLEAN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'LPAREN', 'RPAREN', 'AND', 'OR', 'GT', 'LT',
    'EQ', 'EQEQ', 'NEQ', 'GTE', 'LTE', 'SEMI', 'RBRACE', 'LBRACE', 'IF', 'THEN', 'ELSE', 'ELIF', 'COMMA', 'COLON', 'EOF')

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'TRUE': Token('BOOLEAN', True),
    'FALSE': Token('BOOLEAN', False),
    'AND': Token('AND', 'AND'),
    'OR': Token('OR', 'OR'),
    'NOT': Token('NOT', 'NOT'),
    'IF': Token('IF', 'IF'),
    'THEN': Token('THEN', 'THEN'),
    'ELSE': Token('ELSE', 'ELSE'),
    'ELIF': Token('ELIF', 'ELIF'),
    'FUNC': Token('FUNC', 'FUNC'),
    'LAMBDA': Token('LAMBDA', 'LAMBDA'),

}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char.upper()
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def advance(self):
        """Advance the pos pointer and set the current_char variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQEQ, '==')
                else:
                    return Token(EQ, '=')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GTE, '>=')
                else:
                    return Token(GT, '>')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LTE, '<=')
                else:
                    return Token(LT, '<')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NEQ, '!=')
                else:
                    self.error()

            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            self.error()

        return Token(EOF, None)
