#!/usr/bin/env python3
"""
GridScript test suite.
Tests lexer, parser, and interpreter independently.
Run: python3 test_interpreter.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParseError
from src.interpreter import Interpreter, GridScriptError
from src.errors import GridScriptError

GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

passed = 0
failed = 0
errors = []


def test(category, name, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print(f"  {GREEN}PASS{RESET}  {category:<18} {name}")
    except AssertionError as e:
        failed += 1
        errors.append((category, name, str(e)))
        print(f"  {RED}FAIL{RESET}  {category:<18} {name}")
        print(f"         {RED}{e}{RESET}")
    except Exception as e:
        failed += 1
        errors.append((category, name, f"EXCEPTION: {e}"))
        print(f"  {RED}ERROR{RESET} {category:<18} {name}")
        print(f"         {RED}{e}{RESET}")


def lex(source):
    return Lexer(source, '<test>').tokenize()


def lex_types(source):
    return [t.type for t in lex(source)]


def parse(source):
    return Parser(lex(source)).parse()


def run(source, stdout_capture=True):
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        interp = Interpreter()
        interp.interpret(parse(source))
    return f.getvalue()


def assert_raises(exc_type, fn):
    try:
        fn()
    except exc_type:
        return
    except Exception as e:
        raise AssertionError(f"expected {exc_type.__name__}, got {type(e).__name__}: {e}")
    raise AssertionError(f"expected {exc_type.__name__}, none raised")


# ============================================================
print(f"\n{BOLD}{'='*50}")
print(f"  LEXER TESTS")
print(f"{'='*50}{RESET}\n")

def test_lex_numbers():
    tokens = lex('100 0 25')
    types = [t.type for t in tokens[:-1]]
    assert types == ['NUMBER', 'NUMBER', 'NUMBER'], types

test("lexer", "tokenizes numbers", test_lex_numbers)

def test_lex_identifiers():
    tokens = lex('health step_forward _x x2')
    types = [t.type for t in tokens[:-1]]
    vals = [t.value for t in tokens[:-1]]
    assert types == ['IDENT', 'IDENT', 'IDENT', 'IDENT'], types

test("lexer", "tokenizes identifiers", test_lex_identifiers)

def test_lex_keywords():
    tokens = lex('set if then else end while do def return print true false')
    types = [t.type for t in tokens[:-1]]
    vals = [t.value for t in tokens[:-1]]
    assert all(t == 'KEYWORD' for t in types), types
    assert vals == ['set','if','then','else','end','while','do','def','return','print','true','false']

test("lexer", "tokenizes keywords", test_lex_keywords)

def test_lex_operators():
    tokens = lex('== != < > + - * / =')
    ops = [t.value for t in tokens[:-1]]
    assert ops == ['==','!=','<','>','+','-','*','/','='], ops

test("lexer", "tokenizes operators", test_lex_operators)

def test_lex_strings():
    tokens = lex('"hello world"')
    assert tokens[0].type == 'STRING'
    assert tokens[0].value == '"hello world"'

test("lexer", "tokenizes strings", test_lex_strings)

def test_lex_comments():
    tokens = lex('set x = 1 // this is a comment\nset y = 2')
    types = [t.type for t in tokens[:-1]]
    assert 'COMMENT' not in types
    assert len(types) == 8  # set x = 1 set y = 2

test("lexer", "skips comments", test_lex_comments)

def test_lex_unexpected_char():
    assert_raises(LexerError, lambda: lex('set x = 100$'))

test("lexer", "rejects unexpected characters", test_lex_unexpected_char)

def test_lex_unterminated_string():
    assert_raises(LexerError, lambda: lex('"hello'))

test("lexer", "rejects unterminated strings", test_lex_unterminated_string)

def test_lex_line_tracking():
    tokens = lex('set x = 1\nset y = 2')
    lines = [t.line for t in tokens if t.type != 'EOF']
    assert lines[0] == 1 and lines[-1] == 2

test("lexer", "tracks line numbers", test_lex_line_tracking)


# ============================================================
print(f"\n{BOLD}{'='*50}")
print(f"  PARSER TESTS")
print(f"{'='*50}{RESET}\n")

def test_parse_assignment():
    ast = parse('set x = 5')
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == 'Assign'
    assert stmt.name == 'x'

test("parser", "parses assignment", test_parse_assignment)

def test_parse_print():
    ast = parse('print 2 + 3')
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == 'Print'

test("parser", "parses print statement", test_parse_print)

def test_parse_if():
    ast = parse('if true then print 1 end')
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == 'If'
    assert len(stmt.then_body) == 1
    assert stmt.else_body == []

test("parser", "parses if without else", test_parse_if)

def test_parse_if_else():
    ast = parse('if true then print 1 else print 2 end')
    stmt = ast.statements[0]
    assert len(stmt.then_body) == 1
    assert len(stmt.else_body) == 1

test("parser", "parses if with else", test_parse_if_else)

def test_parse_while():
    ast = parse('while true do print 1 end')
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == 'While'

test("parser", "parses while loop", test_parse_while)

def test_parse_function_def():
    ast = parse('def f(a, b) return a + b end')
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == 'FunctionDef'
    assert stmt.name == 'f'
    assert stmt.params == ['a', 'b']

test("parser", "parses function definition", test_parse_function_def)

def test_parse_function_no_params():
    ast = parse('def f() return 1 end')
    stmt = ast.statements[0]
    assert stmt.params == []

test("parser", "parses function with no params", test_parse_function_no_params)

def test_parse_call():
    ast = parse('f(1, 2, 3)')
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == 'Call'
    assert stmt.name == 'f'
    assert len(stmt.args) == 3

test("parser", "parses function call with args", test_parse_call)

def test_parse_precedence():
    ast = parse('print 2 + 3 * 4')
    expr = ast.statements[0].expr
    assert expr.op == '+'
    assert expr.right.op == '*'

test("parser", "respects operator precedence", test_parse_precedence)

def test_parse_parens():
    ast = parse('print (2 + 3) * 4')
    expr = ast.statements[0].expr
    assert expr.op == '*'
    assert expr.left.op == '+'

test("parser", "handles parenthesised expressions", test_parse_parens)

def test_parse_nested_if():
    ast = parse('if true then if false then print 1 else print 2 end end')
    stmt = ast.statements[0]
    assert len(stmt.then_body) == 1
    inner = stmt.then_body[0]
    assert inner.__class__.__name__ == 'If'

test("parser", "parses nested if statements", test_parse_nested_if)

def test_parse_missing_then():
    assert_raises(ParseError, lambda: parse('if 1\n    print x\nend'))

test("parser", "rejects missing 'then'", test_parse_missing_then)

def test_parse_missing_end():
    assert_raises(ParseError, lambda: parse('if true then print 1'))

test("parser", "rejects missing 'end'", test_parse_missing_end)

def test_parse_unmatched_paren():
    assert_raises(ParseError, lambda: parse('set x = (2 + 3'))

test("parser", "rejects unmatched parentheses", test_parse_unmatched_paren)

def test_parse_bad_char():
    assert_raises(LexerError, lambda: lex('set x = 100$'))

test("parser", "lexer rejects bad characters early", test_parse_bad_char)


# ============================================================
print(f"\n{BOLD}{'='*50}")
print(f"  INTERPRETER TESTS")
print(f"{'='*50}{RESET}\n")

def test_eval_literal_number():
    out = run('print 42')
    assert out.strip() == '42'

test("interpreter", "evaluates number literal", test_eval_literal_number)

def test_eval_literal_string():
    out = run('print "hello"')
    assert out.strip() == 'hello'

test("interpreter", "evaluates string literal", test_eval_literal_string)

def test_eval_literal_bool():
    out = run('print true')
    assert out.strip() == 'true'
    out = run('print false')
    assert out.strip() == 'false'

test("interpreter", "evaluates boolean literals", test_eval_literal_bool)

def test_eval_arithmetic():
    out = run('print 2 + 3 * 4')
    assert out.strip() == '14'

test("interpreter", "evaluates arithmetic with precedence", test_eval_arithmetic)

def test_eval_subtraction():
    out = run('print 10 - 3')
    assert out.strip() == '7'

test("interpreter", "evaluates subtraction", test_eval_subtraction)

def test_eval_division():
    out = run('print 10 / 3')
    assert out.strip() == '3'  # integer division

test("interpreter", "evaluates integer division", test_eval_division)

def test_eval_division_by_zero():
    assert_raises(GridScriptError, lambda: run('print 1 / 0'))

test("interpreter", "rejects division by zero", test_eval_division_by_zero)

def test_eval_string_concat():
    out = run('print "a" + "b"')
    assert out.strip() == 'ab'

test("interpreter", "concatenates strings", test_eval_string_concat)

def test_eval_type_error_add():
    assert_raises(GridScriptError, lambda: run('print "x" + 1'))

test("interpreter", "rejects adding string and number", test_eval_type_error_add)

def test_eval_type_error_subtract():
    assert_raises(GridScriptError, lambda: run('print "x" - 1'))

test("interpreter", "rejects subtracting strings", test_eval_type_error_subtract)

def test_eval_unary_minus():
    out = run('print -5')
    assert out.strip() == '-5'

test("interpreter", "evaluates unary minus", test_eval_unary_minus)

def test_eval_comparison():
    out = run('print 3 < 5')
    assert out.strip() == 'true'
    out = run('print 5 < 3')
    assert out.strip() == 'false'

test("interpreter", "evaluates comparison operators", test_eval_comparison)

def test_eval_equality():
    out = run('print 1 == 1')
    assert out.strip() == 'true'
    out = run('print 1 == 2')
    assert out.strip() == 'false'

test("interpreter", "evaluates equality", test_eval_equality)

def test_eval_cross_type_equality():
    out = run('print "a" == 1')
    assert out.strip() == 'false'

test("interpreter", "cross-type equality returns false", test_eval_cross_type_equality)

def test_eval_set_and_read():
    out = run('set x = 10\nprint x')
    assert out.strip() == '10'

test("interpreter", "set and read variable", test_eval_set_and_read)

def test_eval_reassign():
    out = run('set x = 1\nset x = 2\nprint x')
    assert out.strip() == '2'

test("interpreter", "reassigns variable", test_eval_reassign)

def test_eval_undefined_var():
    assert_raises(GridScriptError, lambda: run('print x'))

test("interpreter", "rejects undefined variable", test_eval_undefined_var)

def test_eval_if_true():
    out = run('if true then print "yes" end')
    assert out.strip() == 'yes'

test("interpreter", "executes if-true branch", test_eval_if_true)

def test_eval_if_false():
    out = run('if false then print "yes" end')
    assert out.strip() == ''

test("interpreter", "skips if-false branch", test_eval_if_false)

def test_eval_if_else():
    out = run('if false then print "a" else print "b" end')
    assert out.strip() == 'b'

test("interpreter", "executes else branch", test_eval_if_else)

def test_eval_if_condition_not_bool():
    assert_raises(GridScriptError, lambda: run('if 5 then print x end'))

test("interpreter", "rejects non-boolean if condition", test_eval_if_condition_not_bool)

def test_eval_while():
    out = run('set x = 0\nwhile x < 3 do\n    print x\n    set x = x + 1\nend')
    assert out.strip() == '0\n1\n2'

test("interpreter", "evaluates while loop", test_eval_while)

def test_eval_while_not_bool():
    assert_raises(GridScriptError, lambda: run('while 1 do print x end'))

test("interpreter", "rejects non-boolean while condition", test_eval_while_not_bool)

def test_eval_function_def_and_call():
    out = run('def add(a, b)\n    return a + b\nend\nprint add(2, 3)')
    assert out.strip() == '5'

test("interpreter", "function definition and call", test_eval_function_def_and_call)

def test_eval_function_wrong_args():
    assert_raises(GridScriptError, lambda: run('def f(a, b)\n    return a\nend\nprint f(1)'))

test("interpreter", "rejects wrong argument count", test_eval_function_wrong_args)

def test_eval_recursion():
    out = run('def fact(n)\n    if n == 0 then\n        return 1\n    else\n        return n * fact(n - 1)\n    end\nend\nprint fact(5)')
    assert out.strip() == '120'

test("interpreter", "evaluates recursive function", test_eval_recursion)

def test_eval_static_scoping():
    out = run('set x = 100\ndef f()\n    set x = 7\n    return x\nend\nprint x\nprint f()\nprint x')
    lines = out.strip().split('\n')
    assert lines == ['100', '7', '100'], f"expected ['100','7','100'], got {lines}"

test("interpreter", "demonstrates static scoping", test_eval_static_scoping)

def test_eval_global_read_from_function():
    out = run('set bonus = 10\ndef add_bonus(val)\n    return val + bonus\nend\nprint add_bonus(5)')
    assert out.strip() == '15'

test("interpreter", "function reads global variable", test_eval_global_read_from_function)

def test_eval_multiple_statements():
    out = run('set a = 1\nset b = 2\nset c = a + b\nprint c')
    assert out.strip() == '3'

test("interpreter", "chained assignments", test_eval_multiple_statements)

def test_eval_nested_expression():
    out = run('print (2 + 3) * (4 - 1)')
    assert out.strip() == '15'

test("interpreter", "nested parenthesised expressions", test_eval_nested_expression)


# ============================================================
print(f"\n{BOLD}{'='*50}")
print(f"  SCOPING & TYPING EDGE CASES")
print(f"{'='*50}{RESET}\n")

def test_shadowing_preserves_global():
    out = run('set x = 1\ndef g()\n    set x = 2\n    return x\nend\nprint g()\nprint x')
    lines = out.strip().split('\n')
    assert lines == ['2', '1']

test("scoping", "shadowing preserves global", test_shadowing_preserves_global)

def test_nested_function_scopes():
    out = run('def outer()\n    set a = 10\n    def inner()\n        return a\n    end\n    return inner()\nend\nprint outer()')
    assert out.strip() == '10'

test("scoping", "inner function reads outer scope", test_nested_function_scopes)

def test_type_error_in_condition():
    assert_raises(GridScriptError, lambda: run('if "hello" then print 1 end'))

test("typing", "string in condition rejected", test_type_error_in_condition)

def test_type_error_in_loop():
    assert_raises(GridScriptError, lambda: run('while "x" do print 1 end'))

test("typing", "string in while rejected", test_type_error_in_loop)

def test_string_comparison_type_error():
    assert_raises(GridScriptError, lambda: run('print "a" < "b"'))

test("typing", "string comparison with < rejected", test_string_comparison_type_error)

def test_divide_by_string():
    assert_raises(GridScriptError, lambda: run('print 5 / "x"'))

test("typing", "divide by string rejected", test_divide_by_string)

def test_multiply_by_string():
    assert_raises(GridScriptError, lambda: run('print 5 * "x"'))

test("typing", "multiply by string rejected", test_multiply_by_string)


# ============================================================
print(f"\n{BOLD}{'='*50}")
print(f"  SUMMARY")
print(f"{'='*50}{RESET}\n")
total = passed + failed
if failed == 0:
    print(f"  {GREEN}{BOLD}{passed}/{total} passed, all PASS{RESET}")
else:
    print(f"  {passed}/{total} passed, {RED}{failed} failed{RESET}")
    print()
    for cat, name, msg in errors:
        print(f"  {RED}✗{RESET} {cat} / {name}: {msg}")

print()
sys.exit(0 if failed == 0 else 1)