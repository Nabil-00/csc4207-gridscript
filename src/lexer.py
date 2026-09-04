from typing import NamedTuple


KEYWORDS = {
    'set', 'if', 'then', 'else', 'end', 'while', 'do',
    'def', 'return', 'print', 'true', 'false',
}

SINGLE_CHARS = {'(': 'LPAREN', ')': 'RPAREN', ',': 'COMMA'}

TWO_CHAR_OPS = ('==', '!=', '<=', '>=')


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source, filename='<unknown>'):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.col = 1

    def error(self, msg):
        raise LexerError(f"{self.filename}:{self.line}:{self.col}: {msg}")

    def peek(self):
        return self.source[self.pos] if self.pos < len(self.source) else '\0'

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def read_while(self, predicate):
        start = self.pos
        while predicate(self.peek()):
            self.advance()
        return self.source[start:self.pos]

    def read_string(self):
        self.advance()
        start = self.pos
        while self.peek() != '"':
            if self.peek() == '\0':
                self.error("unterminated string")
            if self.peek() == '\n':
                self.error("newline in string literal")
            self.advance()
        value = self.source[start:self.pos]
        self.advance()
        return value

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            self.read_while(str.isspace)
            if self.pos >= len(self.source):
                break

            ch = self.peek()
            line, col = self.line, self.col

            if self.source[self.pos:self.pos + 2] == '//':
                self.read_while(lambda c: c != '\n')
                continue
            if ch.isdigit():
                tokens.append(Token('NUMBER', self.read_while(str.isdigit), line, col))
            elif ch.isalpha() or ch == '_':
                word = self.read_while(lambda c: c.isalnum() or c == '_')
                tokens.append(Token('KEYWORD' if word in KEYWORDS else 'IDENT', word, line, col))
            elif ch == '"':
                tokens.append(Token('STRING', f'"{self.read_string()}"', line, col))
            elif ch in SINGLE_CHARS:
                self.advance()
                tokens.append(Token(SINGLE_CHARS[ch], ch, line, col))
            elif ch in '=!<>+-*/':
                two = self.source[self.pos:self.pos + 2]
                if two in ('<=', '>='):
                    self.error(f"operator '{two}' is not supported (use < or > only)")
                if two in TWO_CHAR_OPS:
                    self.advance()
                    self.advance()
                    tokens.append(Token('OP', two, line, col))
                else:
                    self.advance()
                    tokens.append(Token('OP', ch, line, col))
            else:
                self.error(f"unexpected character '{ch}'")

        tokens.append(Token('EOF', None, self.line, self.col))
        return tokens
