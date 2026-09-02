#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParseError
from src.interpreter import Interpreter, ReturnException
from src.errors import GridScriptError


def run_source(source, filename='<stdin>', dump_tokens=False, dump_ast=False):
    try:
        tokens = Lexer(source, filename).tokenize()
    except LexerError as e:
        print(f"LexError: {e}", file=sys.stderr)
        sys.exit(1)

    if dump_tokens:
        for tok in tokens:
            print(f"  {tok.type:<8} {tok.value!r}")
        return

    try:
        ast = Parser(tokens).parse()
    except ParseError as e:
        print(f"ParseError: {e}", file=sys.stderr)
        sys.exit(1)

    if dump_ast:
        from src.ast_nodes import Program, Assign, Print, If, While, FunctionDef, Return, Call, BinaryOp, UnaryOp, Literal, Variable
        print(_dump_ast(ast))
        return

    try:
        interp = Interpreter()
        interp.interpret(ast)
    except GridScriptError as e:
        print(f"RuntimeError: {e}", file=sys.stderr)
        sys.exit(1)


def _dump_ast(node, indent=0):
    pad = '  ' * indent
    if isinstance(node, list):
        return '\n'.join(_dump_ast(x, indent) for x in node)
    if not hasattr(node, '__dict__'):
        return f"{pad}{node!r}"
    fields = []
    for k, v in vars(node).items():
        if isinstance(v, list):
            if v:
                fields.append(f"{pad}  {k}:")
                fields.append(_dump_ast(v, indent + 1))
            else:
                fields.append(f"{pad}  {k}: []")
        elif hasattr(v, '__dict__'):
            fields.append(f"{pad}  {k}:")
            fields.append(_dump_ast(v, indent + 1))
        else:
            fields.append(f"{pad}  {k}: {v!r}")
    name = type(node).__name__
    return f"{pad}{name}\n" + '\n'.join(fields)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='GridScript interpreter')
    parser.add_argument('file', nargs='?', help='.gsc file to run')
    parser.add_argument('--tokens', action='store_true', help='dump tokens and exit')
    parser.add_argument('--ast', action='store_true', help='dump AST and exit')
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            source = f.read()
        run_source(source, args.file, dump_tokens=args.tokens, dump_ast=args.ast)
    else:
        source = sys.stdin.read()
        run_source(source, dump_tokens=args.tokens, dump_ast=args.ast)


if __name__ == '__main__':
    main()