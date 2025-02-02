"""POSIX Token Recognition Lexer (IEEE 1003.1-2017 Section 2.3)"""

class POSIXLexer:
    def __init__(self, input_str: str):
        self.input = input_str
        self.length = len(input_str)
        self.pos = 0
        self.tokens = []

    def _advance(self, n=1):
        self.pos += n
        if self.pos > self.length:
            self.pos = self.length

    def _current_char(self):
        return self.input[self.pos] if self.pos < self.length else None

    def tokenize(self) -> list[dict]:
        self.tokens = []
        while self.pos < self.length:
            char = self._current_char()
            
            if char in ' \t':
                self._advance()
            elif char.isalnum() or char == '_':
                collected = ""
                while char is not None and (char.isalnum() or char == '_'):
                    collected += char
                    self._advance()
                    char = self._current_char()
                self.tokens.append({'type': 'word', 'value': collected})
            else:
                self._advance()
                
        return self.tokens