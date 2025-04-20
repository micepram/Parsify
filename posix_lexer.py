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

    def tokenize(self):
        while self.pos < self.length:
            char = self._current_char()
            
            if char == '\n':
                yield {'type': 'newline', 'value': '\n'}
                self._advance()
                continue
            
            if char in ' \t':
                self._advance()
                continue
            
            collected = ""
            quote_state = None
            
            while self.pos < self.length:
                char = self._current_char()
                
                if quote_state == "'":
                    if char == "'":
                        quote_state = None
                        self._advance()
                    else:
                        collected += char
                        self._advance()
                elif quote_state == '"':
                    if char == '"':
                        quote_state = None
                        self._advance()
                    elif char == '\\':
                        self._advance()
                        peek = self._current_char()
                        if peek is not None:
                            collected += peek
                            self._advance()
                    else:
                        collected += char
                        self._advance()
                else:
                    if char in ' \t\n':
                        break
                    elif char == '\\':
                        self._advance()
                        peek = self._current_char()
                        if peek is not None:
                            collected += peek
                            self._advance()
                    elif char == "'":
                        quote_state = "'"
                        self._advance()
                    elif char == '"':
                        quote_state = '"'
                        self._advance()
                    else:
                        collected += char
                        self._advance()
            
            yield {'type': 'word', 'value': collected}

    def get_all_tokens(self) -> list[dict]:
        return list(self.tokenize())