import unittest
from posix_lexer import POSIXLexer

class TestPOSIXLexer(unittest.TestCase):
    def test_empty_input(self):
        lexer = POSIXLexer('')
        self.assertEqual(lexer.tokenize(), [])

if __name__ == '__main__':
    unittest.main()