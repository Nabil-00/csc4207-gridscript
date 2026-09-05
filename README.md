# GridScript

GridScript is a small interpreted language for scripting a 2D game actor, written in Python for the CSC4207 (Organization of Programming Languages) group project.

## Layout

```
gridscript/
├── gridscript.py        # CLI: run .gsc files (also: --tokens, --ast)
├── run_tests.py         # integration test runner (stdlib only)
├── test_interpreter.py  # unit test suite: lexer, parser, interpreter
├── GridScript_Design_Document.md  # grammar, semantics, scoping rationale
├── DIVISION_OF_LABOR.md # who owns what, video prep guide
├── src/                 # lexer, parser, AST, environment, interpreter
├── tests/               # valid programs + expected output, invalid + errors
├── examples/            # longer example scripts
├── report/              # report source, PDF, screenshots, evidence
├── tools/               # dev scripts (PDF builder, screenshot generators)
└── docs/                # video plans, scripts, study flashcards
```

## Requirements

Python 3.8+ (standard library only, no pip installs).

## Usage

```bash
python3 gridscript.py examples/quest.gsc      # run a script
python3 gridscript.py --tokens examples/quest.gsc   # dump tokens
python3 gridscript.py --ast   examples/quest.gsc    # dump the AST
python3 run_tests.py          # run the whole test suite
```

## Language at a glance

```text
set health = 100              # variable / assignment
print "low health"            # output
print 2 + 3 * 4               # arithmetic (precedence)
if health < 50 then           # conditional (else optional)
    use_potion()
else
    step_forward()
end
while health > 0 do           # loop
    set health = health - 1
end
def scale(v, f)               # user function (params + return)
    return v * f
end
```

## Language rules (summary)

- Types are Number (int), String, and Boolean. Typing is dynamic and checked at run time.
- Scoping is static (lexical). Only function calls create scopes. `set` binds in the current scope only while reads resolve outward, so an assignment inside a function shadows a global instead of overwriting it.
- `+ - * /` work on numbers, and `+` also concatenates strings. `<` and `>` compare numbers. `==` and `!=` compare same-type values by value; across different types `==` gives `false` and `!=` gives `true`.
- Conditions must be Boolean. `if 5 then ...` fails at run time with a `TypeError`.
- Comments start with `//` and run to the end of the line.
