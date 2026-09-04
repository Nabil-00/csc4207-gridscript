# GridScript video walkthrough scripts

One script per project part. Each is sized for 2 to 3 minutes. Follow the
steps in order; the numbered shots line up with the screenshots in
`report/screenshots/`.

## Recording setup (all members)

- Screen recorder that captures terminal + editor, e.g. OBS Studio or
  GNOME's built-in recorder (`Ctrl+Alt+Shift+R`).
- Terminal: dark theme, font size 18 or larger so text is readable.
- Open the repo at `Documents/CSC4207/gridscript/` and the design document
  side by side.
- State your name, registration number, and which part you built at the
  start. Then walk through your own code. Do not read from a script
  word for word; the marker wants to see you explain your own work.

---

## Member A: lexer (src/lexer.py)

Shots:

1. Show the token table in design doc section 2. One sentence: "The lexer
   turns characters into tokens using these regular expressions."
2. Open `src/lexer.py`. Point out the three key pieces:
   - `KEYWORDS` set: reserved words are recognised here, so the DFA only
     needs one identifier pattern.
   - `read_number`, `read_identifier`, `read_string`: longest-match rules.
   - `tokenize()`: the main loop, whitespace and comment skipping.
3. Run the live demo:
   ```
   python3 gridscript.py --tokens tests/valid/patrol.gsc
   ```
   (screenshot: `lexer_output_tokens.png`)
4. Show an error case:
   ```
   python3 gridscript.py tests/invalid/bad_char.gsc
   ```
   Explain: unexpected characters are rejected at lex time, before parsing.

Say: "I built the lexer. It scans the source once, character by character,
and produces a list of tokens with line and column info for error messages."

---

## Member B: parser (src/parser.py)

Shots:

1. Show the BNF grammar in design doc section 3. One sentence: "The parser
   is a direct implementation of this grammar; one function per
   non-terminal."
2. Open `src/parser.py`. Point out:
   - `parse_statement`: dispatches on the keyword.
   - `parse_expression` / `parse_comparison` / `parse_arithmetic` /
     `parse_term` / `parse_factor`: the precedence ladder.
   - `parse_block`: parses statements until `end` or `else`, which is how
     nesting works without extra state.
3. Run:
   ```
   python3 gridscript.py --ast tests/valid/scale.gsc
   ```
   (screenshot: `parser_output_ast.png`)
4. Show:
   ```
   python3 gridscript.py tests/invalid/missing_then.gsc
   ```
   Explain: the parser catches structure errors the lexer cannot see.

Say: "I built the recursive descent parser. It consumes the token stream
and builds an AST; precedence comes from the grammar levels."

---

## Member C: environment and scoping (src/environment.py)

Shots:

1. Show the three scoping rules in design doc section 5.
2. Open `src/environment.py` (about 30 lines). Explain the parent chain:
   - `set()` writes into the current scope only.
   - `get()` walks up the parent chain, which is lexical resolution.
3. Run the shadowing demo:
   ```
   python3 gridscript.py tests/valid/shadowing.gsc
   ```
   (screenshot: `shadowing_gsc_static_scoping_demo.png`)
4. Explain the output: `100`, `7`, `100`. The assignment inside `hide`
   created a local `x`; the global `x` kept its value.

Say: "I built the environment model. Static scoping means a function's
variables resolve where it was defined, not where it is called."

---

## Member D: interpreter (src/interpreter.py)

Shots:

1. Show design doc section 6, the operational semantics rules. One
   sentence: "Each AST node has one evaluation rule; that is what the
   interpreter implements."
2. Open `src/interpreter.py`. Point out:
   - `visit_*` methods: one per AST node, matching section 6.
   - `visit_BinaryOp`: where the dynamic typing rules live.
   - `visit_Call`: closure creation and the new scope per call.
   - `ReturnException`: how `return` unwinds out of nested blocks.
3. Run the patrol demo:
   ```
   python3 gridscript.py tests/valid/patrol.gsc
   ```
   (screenshot: `patrol_gsc_while_if_built_ins.png`)
4. Run a type error:
   ```
   python3 gridscript.py tests/invalid/if_not_bool.gsc
   ```

Say: "I built the evaluator. Every construct from the design document has
a matching visit method; the typing rules in section 4 are enforced here."

---

## Member E: tests and packaging (run_tests.py, test_interpreter.py, report/)

Shots:

1. Show the coverage checklist in design doc section 8.
2. Run the integration suite:
   ```
   python3 run_tests.py
   ```
   (screenshot: `run_tests_full_suite.png`)
3. Run the unit suite:
   ```
   python3 test_interpreter.py
   ```
4. Show the invalid tests folder: each bad program has an expected error.
5. Show `report/screenshots/`: the same runs rendered as images for the
   written report.

Say: "I built the test suite. Valid programs are checked against expected
output; invalid programs must fail with a specific message. 61 unit tests
and 17 integration tests all pass."

---

## One-take checklist

Before you hit record:

- [ ] Repo pulled, tests pass on your machine
- [ ] You can explain every line of your part without notes
- [ ] Your face or voice is on the recording as required
- [ ] 2 to 3 minutes: rehearse once with a timer
- [ ] File named `video_<member>.mp4` in the submission zip
