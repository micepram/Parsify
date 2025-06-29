"""POSIX Token Recognition Lexer (IEEE 1003.1-2017 Section 2.3)"""

class POSIXLexer:
    KEYWORDS = {'if', 'then', 'else', 'fi', 'for', 'while', 'do', 'done', 'case', 'esac'}

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
            
            # 1. Operators
            if char in '<>|&;()':
                if self.pos + 1 < self.length:
                    next_char = self.input[self.pos + 1]
                    pair = char + next_char
                    if pair in ('<<', '>>', '&&', '||', ';;', '<>', '>|', '<&', '>&'):
                        yield {'type': 'operator', 'value': pair}
                        self._advance(2)
                        continue
                yield {'type': 'operator', 'value': char}
                self._advance()
                continue
            
            # 2. Quotes / Escapes (Start of word)
            # 3. Comments
            # 4. Words (General)
            is_word_start = False
            
            if char in ('\\', "'", '"'):
                is_word_start = True
            elif char == '#':
                while self.pos < self.length:
                    if self._current_char() == '\n':
                        break
                    self._advance()
                continue
            elif char not in ' \t\n':
                is_word_start = True
            
            if is_word_start:
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
                        elif char in '<>|&;()':
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
                
                token_type = 'keyword' if collected in self.KEYWORDS else 'word'
                yield {'type': token_type, 'value': collected}
                continue

            # 5. Blanks / Newline
            if char == '\n':
                yield {'type': 'newline', 'value': '\n'}
                self._advance()
            else:
                self._advance()

    def get_all_tokens(self) -> list[dict]:
        return list(self.tokenize())