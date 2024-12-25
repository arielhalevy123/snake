# Project: Custom Programming Language Interpreter

## Overview
This project implements a **custom programming language interpreter** from scratch. The interpreter parses, interprets, and evaluates expressions and statements written in the custom language. It supports arithmetic operations, boolean expressions, conditional statements, functions, lambda expressions, and more.

The interpreter is built using Python and is divided into distinct components following the **lexical analysis, parsing, and interpretation pipeline**:

1. **Lexer**: Tokenizes the input code.
2. **Parser**: Converts tokens into an Abstract Syntax Tree (AST).
3. **Interpreter**: Evaluates the AST to execute the code.

---

## Features
- **Arithmetic Operations**: Supports `+`, `-`, `*`, `/`, and `%`.
- **Boolean Logic**: Implements `AND`, `OR`, and comparison operators (`>`, `<`, `>=`, `<=`, `==`, `!=`).
- **Conditionals**: Supports `IF`, `ELIF`, `ELSE` blocks for conditional logic.
- **Functions**: User-defined functions with parameters and return values.
- **Lambda Expressions**: Inline anonymous functions.
- **Code Blocks**: Enclosed in `{}` for grouping statements.
- **Error Handling**: Provides meaningful error messages for invalid syntax or runtime issues.

---

## Project Structure

- **main.py**:
  - Entry point of the application.
  - Reads input code and processes it through the interpreter pipeline.

- **Lexer.py**:
  - Tokenizes input code into a series of tokens for parsing.
  - Recognizes keywords, operators, identifiers, and other language constructs.

- **Parser.py**:
  - Converts tokens into an Abstract Syntax Tree (AST).
  - Implements grammar rules for the custom language.

- **Interpreter.py**:
  - Traverses the AST and evaluates expressions and statements.
  - Maintains a function table and supports scoped variable resolution.

- **2024-08-25-5.py**:
  - Utility file showcasing examples of higher-order functions, lambda expressions, and functional programming principles.

---

## Grammar Definition
The grammar of the language is defined using Backus-Naur Form (BNF):

```
FACTOR          : INTEGER | BOOLEAN | (BOOLEAN_EXPR) | (LAMBDA_EXPRESSION) | FUNCTION_CALL | IF_STATEMENT
TERM            : FACTOR ((MUL | DIV | MOD) FACTOR)*
EXPR            : TERM ((PLUS | MINUS) TERM)*
COMPARISON_EXPR : EXPR ((GT | LT | EQEQ | NEQ | GTE | LTE) EXPR)*
BOOLEAN_EXPR    : COMPARISON_EXPR ((AND | OR) COMPARISON_EXPR)*
STATEMENT       : FUNC FUNCTION_DECLARATION | BLOCK | BOOLEAN_EXPR SEMI
STATEMENT_LIST  : STATEMENT* (RBRACE | EOF)
ARGUMENT_LIST   : BOOLEAN_EXPR (COMMA BOOLEAN_EXPR)*
BLOCK           : LBRACE STATEMENT_LIST RBRACE
IF_STATEMENT    : IF BOOLEAN_EXPR THEN BLOCK (ELIF BOOLEAN_EXPR THEN BLOCK)* (ELSE BLOCK)?
PARAMETER_LIST  : ID (COMMA ID)*
FUNCTION_DECLARATION : FUNC ID (PARAMETER_LIST) BLOCK
FUNCTION_CALL   : ID (ARGUMENT_LIST)
LAMBDA_EXPRESSION : LAMBDA PARAMETER_LIST : BLOCK
```

---

## How to Use
### Prerequisites
- **Python 3.8+**

### Running the Project
1. Clone the repository.
2. Navigate to the project directory.
3. Run `main.py`:
   ```bash
   python main.py
   ```
4. Enter your custom language code in the prompt.

### Example Usage
```bash
> FUNC add(x, y) { x + y; }
> add(5, 10);
15
> IF (10 > 5) THEN { TRUE; } ELSE { FALSE; }
TRUE
```

---

## Technical Details
### Lexical Analysis (Lexer)
- Tokenizes input code into meaningful symbols (e.g., `+`, `IF`, `TRUE`).
- Ignores whitespace and identifies reserved keywords.

### Parsing (Parser)
- Builds an Abstract Syntax Tree (AST) using recursive descent parsing.
- Implements error handling for invalid syntax.

### Interpretation (Interpreter)
- Traverses the AST to execute code.
- Supports:
  - Variable scoping and function calls.
  - Error handling for runtime issues.

---

## Future Improvements
- **Enhanced Error Reporting**: Provide detailed line and column information.
- **Support for Loops**: Add constructs like `FOR` and `WHILE`.
- **Type Checking**: Enforce strong typing for variables and function arguments.
- **Optimizations**: Improve the interpreter's efficiency with caching mechanisms.
- **Debugger**: Add step-by-step execution for debugging.

---

## Contributors
- **Your Name**: Design and development

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
Special thanks to open-source resources and programming communities for their support.

