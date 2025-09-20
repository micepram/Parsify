# Parsify

[![CI](https://github.com/micepram/parsify/actions/workflows/ci.yml/badge.svg)](https://github.com/micepram/parsify/actions/workflows/ci.yml)

## Overview
Parsify is a minimal, POSIX-compliant shell lexer written in Python 3. It is designed to implement the Token Recognition rules defined in IEEE Std 1003.1-2017 Section 2.3. It scans shell script input and breaks it down into a stream of tokens, correctly identifying words, operators, and reserved keywords while respecting quoting and escaping rules.

## Features

*   Token Types: Identifies Words, Operators, Keywords, and Newlines.
*   Quoting Support: Handles single quotes (`'...'`) for literals and double quotes (`"..."`) with escape processing.
*   Operator Recognition: Recognizes standard POSIX operators (e.g., `|`, `&`, `;`) and multi-character operators (e.g., `&&`, `||`, `<<`, `>>`).
*   Escaping: Supports backslash escapes in unquoted and double-quoted contexts.
*   Comments: Strips `#` comments until the end of the line.
*   Keywords: Detects reserved words like `if`, `then`, `while`, `done`.

## Usage

The lexer can be run directly from the command line, accepting either a raw string or a file path. It outputs the list of tokens in JSON format.

**Scan a string:**

```bash
python posix_lexer.py "echo 'hello world'"
```

**Scan a file:**

```bash
python posix_lexer.py examples/basic.sh
```

## Examples
Input (`examples/basic.sh`):

```bash
echo 'hi' "there" # comment
ls -l | grep ".py"
val=123; echo $val
if true; then echo yes; fi
cat <<EOF
```

Output (abbreviated JSON):

```json
[
  { "type": "word", "value": "echo" },
  { "type": "word", "value": "hi" },
  { "type": "word", "value": "there" },
  { "type": "newline", "value": "\n" },
  { "type": "word", "value": "ls" },
  { "type": "word", "value": "-l" },
  { "type": "operator", "value": "|" },
  ...
]
```

## Testing
The project includes a comprehensive unit test suite covering edge cases, mixed quotes, and operator precedence.

Run the tests with:

```bash
python -m unittest test_posix_lexer.py
```

## Limitations
*   **No Expansion**: Variable expansion (`$var`) and command substitution (`$(...)`) are tokenized as words or parts of words. The lexer does not perform the actual expansion or execution.
*   **No AST**: This is strictly a lexical scanner; it does not parse the tokens into an Abstract Syntax Tree.