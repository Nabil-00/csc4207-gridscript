KEYWORDS = {
    'set', 'if', 'then', 'else', 'end', 'while', 'do',
    'def', 'return', 'print', 'true', 'false',
}

TOKEN_NAMES = {
    'KEYWORD': 'KEYWORD',
    'IDENT': 'IDENT',
    'NUMBER': 'NUMBER',
    'STRING': 'STRING',
    'OP': 'OP',
    'LPAREN': 'LPAREN',
    'RPAREN': 'RPAREN',
    'COMMA': 'COMMA',
    'EOF': 'EOF',
}


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


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
        if self.pos >= len(self.source):
            return '\0'
        return self.source[self.pos]

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def skip_whitespace(self):
        while self.peek() in (' ', '\t', '\n', '\r'):
            self.advance()

    def skip_comment(self):
        while self.peek() not in ('\n', '\0'):
            self.advance()

    def read_number(self):
        start = self.pos
        while self.peek().isdigit():
            self.advance()
        return self.source[start:self.pos]

    def read_identifier(self):
        start = self.pos
        while self.peek().isalnum() or self.peek() == '_':
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
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break

            ch = self.peek()
            line = self.line
            col = self.col

            if ch == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                self.skip_comment()
                continue

            if ch.isdigit():
                num = self.read_number()
                tokens.append(Token('NUMBER', num, line, col))
                continue

            if ch.isalpha() or ch == '_':
                ident = self.read_identifier()
                if ident in KEYWORDS:
                    tokens.append(Token('KEYWORD', ident, line, col))
                else:
                    tokens.append(Token('IDENT', ident, line, col))
                continue

            if ch == '"':
                s = self.read_string()
                tokens.append(Token('STRING', f'"{s}"', line, col))
                continue

            if ch == '(':
                self.advance()
                tokens.append(Token('LPAREN', '(', line, col))
                continue

            if ch == ')':
                self.advance()
                tokens.append(Token('RPAREN', ')', line, col))
                continue

            if ch == ',':
                self.advance()
                tokens.append(Token('COMMA', ',', line, col))
                continue

            if ch in '=!<>+-*/':
                two_char = self.source[self.pos:self.pos + 2]
                if two_char in ('==', '!=', '<=', '>='):
                    if two_char in ('<=', '>='):
                        self.error(f"operator '{two_char}' is not supported (use < or > only)")
                    self.advance()
                    self.advance()
                    tokens.append(Token('OP', two_char, line, col))
                else:
                    self.advance()
                    tokens.append(Token('OP', ch, line, col))
                continue

            self.error(f"unexpected character '{ch}'")

        tokens.append(Token('EOF', None, self.line, self.col))
        return tokens