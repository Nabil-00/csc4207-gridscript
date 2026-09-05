# Group 1: division of labour

| Member | Registration number | Responsibility | Main files | Course topic |
|---|---|---|---|---|
| Nabil Ismail Abdulkadir | UG22CSC1047 | Interpreter, built-ins, and errors | `src/interpreter.py`, `src/builtins.py`, `src/errors.py` | Operational semantics and type systems |
| Ahmad Auwal Abubakar | UG22CSC1075 | Parser and grammar | `src/parser.py`, BNF grammar in the design document | Context-free grammars |
| Abubakar Muhammad Sulaiman | UG22CSC1046 | Lexer and token rules | `src/lexer.py` | Regular expressions and finite automata |
| Rukayya Musbahu Imam | UG22CSC1040 | AST and environment model | `src/ast_nodes.py`, `src/environment.py` | Names, binding, and lexical scoping |
| Muhammad Salisu | UG20CSC1005 | Tests and written report | `run_tests.py`, `test_interpreter.py`, `tests/`, report | Testing across all topics |

The group verified the complete pipeline together: source code is tokenised by the lexer, parsed into an AST, and evaluated by the interpreter. Evidence links in the written report lead to the parser output, static-scoping demonstration, and passing integration suite.
