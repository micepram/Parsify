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

    # --- Comprehensive POSIX Section 2.3 Tests ---

    def test_simple_args(self):
        # Basic command arguments
        lexer = POSIXLexer("ls -l /tmp")
        expected = [
            {'type': 'word', 'value': 'ls'},
            {'type': 'word', 'value': '-l'},
            {'type': 'word', 'value': '/tmp'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_pipeline(self):
        # Pipeline operator separation
        lexer = POSIXLexer("cat file|grep search")
        expected = [
            {'type': 'word', 'value': 'cat'},
            {'type': 'word', 'value': 'file'},
            {'type': 'operator', 'value': '|'},
            {'type': 'word', 'value': 'grep'},
            {'type': 'word', 'value': 'search'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_assignment_word(self):
        # Assignments are just words at the lexing stage (unless separated)
        lexer = POSIXLexer("KEY=value VAR=123")
        expected = [
            {'type': 'word', 'value': 'KEY=value'},
            {'type': 'word', 'value': 'VAR=123'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_concatenation(self):
        # Adjacent quoted/unquoted parts form a single word
        lexer = POSIXLexer("abc'def'\"ghi\"")
        expected = [{'type': 'word', 'value': 'abcdefghi'}]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_keywords_control(self):
        # Reserved words recognition
        lexer = POSIXLexer("while true; do echo yes; done")
        expected = [
            {'type': 'keyword', 'value': 'while'},
            {'type': 'word', 'value': 'true'},
            {'type': 'operator', 'value': ';'},
            {'type': 'keyword', 'value': 'do'},
            {'type': 'word', 'value': 'echo'},
            {'type': 'word', 'value': 'yes'},
            {'type': 'operator', 'value': ';'},
            {'type': 'keyword', 'value': 'done'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_expansion_basic(self):
        # $ is not an operator, so it sticks to the word
        lexer = POSIXLexer("echo $VAR ${VAR}")
        expected = [
            {'type': 'word', 'value': 'echo'},
            {'type': 'word', 'value': '$VAR'},
            {'type': 'word', 'value': '${VAR}'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_command_substitution_tokens(self):
        # $ is a word char, ( is an operator -> split happens
        lexer = POSIXLexer("echo $(date)")
        expected = [
            {'type': 'word', 'value': 'echo'},
            {'type': 'word', 'value': '$'},
            {'type': 'operator', 'value': '('},
            {'type': 'word', 'value': 'date'},
            {'type': 'operator', 'value': ')'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_heredoc_op(self):
        # Multi-character operator recognition
        lexer = POSIXLexer("cat <<EOF")
        expected = [
            {'type': 'word', 'value': 'cat'},
            {'type': 'operator', 'value': '<<'},
            {'type': 'word', 'value': 'EOF'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_and_or_ops(self):
        # Logical operators
        lexer = POSIXLexer("true && false || true")
        expected = [
            {'type': 'word', 'value': 'true'},
            {'type': 'operator', 'value': '&&'},
            {'type': 'word', 'value': 'false'},
            {'type': 'operator', 'value': '||'},
            {'type': 'word', 'value': 'true'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

    def test_comment_strip_end(self):
        # Comment at end of complex line
        lexer = POSIXLexer("ls -l # list files")
        expected = [
            {'type': 'word', 'value': 'ls'},
            {'type': 'word', 'value': '-l'}
        ]
        self.assertEqual(lexer.get_all_tokens(), expected)

if __name__ == '__main__':
    unittest.main()