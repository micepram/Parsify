"""POSIX Token Recognition Lexer (IEEE 1003.1-2017 Section 2.3)"""
import sys
import json
import os

version = '1.0.0'

class LexerError(Exception):
    pass

class POSIXLexer:
    KEYWORDS = {'if', 'then', 'else', 'fi', 'for', 'while', 'do', 'done', 'case', 'esac'}
    OPERATORS = {'<<', '>>', '&&', '||', ';;', '<>', '>|', '<&', '>&'}

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

    def _peek_char(self):
        return self.input[self.pos + 1] if self.pos + 1 < self.length else None

    def _scan_operator(self, char: str) -> dict:
        if self.pos + 1 < self.length:
            pair = self.input[self.pos:self.pos+2]
            if pair in self.OPERATORS:
                self._advance(2)
                return {'type': 'operator', 'value': pair}
        self._advance()
        return {'type': 'operator', 'value': char}

    def _scan_comment(self) -> None:
        # Skip until newline
        newline = self.input.find('\n', self.pos)
        if newline == -1:
            self.pos = self.length
        else:
            self.pos = newline

    def _scan_word(self) -> dict:
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
                # Unquoted state
                if char in ' \t\n':
                    break
                if char in '<>|&;()':
                    break
                
                if char == '\\':
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
        return {'type': token_type, 'value': collected}

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

            if char == '#':
                self._scan_comment()
                continue

            if char in '<>|&;()':
                yield self._scan_operator(char)
                continue
            
            # Start of a word (quoted or unquoted)
            yield self._scan_word()

    def get_all_tokens(self) -> list[dict]:
        return list(self.tokenize())

def run_example(file_path: str) -> None:
    with open(file_path, 'r') as f:
        content = f.read()
    lexer = POSIXLexer(content)
    for token in lexer.tokenize():
        print(token)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python posix_lexer.py <input_string_or_file>")
        sys.exit(1)
    
    arg = sys.argv[1]
    if os.path.isfile(arg):
        with open(arg, 'r') as f:
            content = f.read()
    else:
        content = arg

    try:
        lexer = POSIXLexer(content)
        print(json.dumps(lexer.get_all_tokens(), indent=2))
    except LexerError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)