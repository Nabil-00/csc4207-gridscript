# GridScript

A small interpreter for a tiny language that scripts a 2D game actor.
Built for the CSC4207 (Organization of Programming Languages) group project.

## Layout

```
gridscript/
├── gridscript.py        # CLI: run .gsc files (also: --tokens, --ast)
├── run_tests.py         # integration test runner (stdlib only)
├── test_interpreter.py  # unit test suite: lexer, parser, interpreter
├── src/
│   ├── ast_nodes.py     # AST node dataclasses
│   ├── lexer.py         # tokenizer (regular expressions -> tokens)
│   ├── parser.py        # recursive descent parser (BNF -> AST)
│   ├── environment.py   # lexical scope chains
│   ├── builtins.py      # grid world + built-in actor actions
│   ├── interpreter.py   # evaluates the AST (operational semantics)
│   └── errors.py        # shared error type
├── tests/
│   ├── valid/           # programs that must run + .expected output
│   └── invalid/         # programs that must fail + .error substring
├── examples/            # longer example scripts
├── report/              # screenshots for the written report
└── tools/               # dev-only scripts (screenshot generators)
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

- **Types**: `Number` (int), `String`, `Boolean`. Dynamic typing, checked at
  run time.
- **Scoping**: static/lexical. Only function calls create scopes. `set` binds in
  the *current* scope only; reads resolve outward lexically. Assignment inside a
  function can never clobber a global (it shadows).
- **Operators**: `+ - * /` (numbers), `+` (string concat), `< >` (numbers),
  `== !=` (any same-type values; different types compare `false`).
- **Conditions** must be Boolean (`if 5 then ...` is a run-time `TypeError`).
- **Comments**: `//` to end of line.
