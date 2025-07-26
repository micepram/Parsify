import unittest
from posix_lexer import POSIXLexer, LexerError

class TestPOSIXLexer(unittest.TestCase):
    def test_empty_input(self):
        lexer = POSIXLexer('')
        self.assertEqual(lexer.get_all_tokens(), [])

    def test_quoted_blanks(self):
        lexer = POSIXLexer("'hello world' \"foo bar\"")
        expected = [
            {'type': 'word', 'value': 'hello world'},
            {'type': 'word', 'value': 'foo bar'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_mixed_quotes(self):
        lexer = POSIXLexer('"foo"\'bar\' unquoted')
        expected = [
            {'type': 'word', 'value': 'foobar'},
            {'type': 'word', 'value': 'unquoted'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_escapes_in_double(self):
        lexer = POSIXLexer(r'"\""')
        expected = [{'type': 'word', 'value': '"'}]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_single_quotes_literal(self):
        lexer = POSIXLexer(r"'\t'")
        expected = [{'type': 'word', 'value': '\\t'}]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_escaped_unquoted(self):
        lexer = POSIXLexer(r'foo\ bar')
        expected = [{'type': 'word', 'value': 'foo bar'}]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_quoted_operator(self):
        lexer = POSIXLexer(r"'>' '&'")
        expected = [
            {'type': 'word', 'value': '>'},
            {'type': 'word', 'value': '&'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_escaped_operator(self):
        lexer = POSIXLexer(r'\> \&')
        expected = [
            {'type': 'word', 'value': '>'},
            {'type': 'word', 'value': '&'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_unclosed_quote(self):
        lexer = POSIXLexer("'open quote")
        with self.assertRaises(LexerError):
            lexer.get_all_tokens()

if __name__ == '__main__':
    unittest.main()