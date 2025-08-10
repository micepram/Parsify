"""POSIX Token Recognition Lexer (IEEE 1003.1-2017 Section 2.3)"""

class LexerError(Exception):
    pass

class POSIXLexer:
    KEYWORDS = {'if', 'then', 'else', 'fi', 'for', 'while', 'do', 'done', 'case', 'esac'}

    def __init__(self, input_str: str):
        self.input = input_str
        self.length = len(input_str)
        self.pos = 0
        self.tokens = []

    def __str__(self) -> str:
        return f"<POSIXLexer pos={self.pos} len={self.length}>"

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
                    # Optimization: Slice for potential 2-char operator
                    pair = self.input[self.pos:self.pos+2]
                    if pair in ('<<', '>>', '&&', '||', ';;', '<>', '>|', '<&', '>&'):
                        yield {'type': 'operator', 'value': pair}
                        self._advance(2)
                        continue
                yield {'type': 'operator', 'value': char}
                self._advance()
                continue
            
            # 2. Quotes / Escapes / Comments / Words
            is_word_start = False
            
            if char in ('\\', "'", '"'):
                is_word_start = True
            elif char == '#':
                # Optimization: Find newline to skip comment
                newline = self.input.find('\n', self.pos)
                if newline == -1:
                    self.pos = self.length
                else:
                    self.pos = newline
                continue
            elif char not in ' \t\n':
                is_word_start = True
            
            if is_word_start:
                collected_parts = []
                quote_state = None
                
                while self.pos < self.length:
                    char = self._current_char()
                    
                    if quote_state == "'":
                        if char == "'":
                            quote_state = None
                            self._advance()
                        else:
                            collected_parts.append(char)
                            self._advance()
                    elif quote_state == '"':
                        if char == '"':
                            quote_state = None
                            self._advance()
                        elif char == '\\':
                            self._advance()
                            peek = self._current_char()
                            if peek is not None:
                                collected_parts.append(peek)
                                self._advance()
                        else:
                            collected_parts.append(char)
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
                                collected_parts.append(peek)
                                self._advance()
                        elif char == "'":
                            quote_state = "'"
                            self._advance()
                        elif char == '"':
                            quote_state = '"'
                            self._advance()
                        else:
                            collected_parts.append(char)
                            self._advance()
                
                if quote_state is not None:
                    raise LexerError("Unclosed quote")

                collected = "".join(collected_parts)
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

def run_example(file_path: str) -> None:
    with open(file_path, 'r') as f:
        content = f.read()
    lexer = POSIXLexer(content)
    for token in lexer.tokenize():
        print(token)