#!/usr/bin/env python3
import sys
import os
from pprint import pprint

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParseError
from src.interpreter import Interpreter, ReturnException
from src.errors import GridScriptError


def run_source(source, filename='<stdin>', dump_tokens=False, dump_ast=False):
    try:
        tokens = Lexer(source, filename).tokenize()
    except LexerError as e:
        sys.exit(f"LexError: {e}")

    if dump_tokens:
        for tok in tokens:
            print(f"  {tok.type:<8} {tok.value!r}")
        return

    try:
        ast = Parser(tokens).parse()
    except ParseError as e:
        sys.exit(f"ParseError: {e}")

    if dump_ast:
        pprint(ast.statements)
        return

    try:
        Interpreter().interpret(ast)
    except GridScriptError as e:
        sys.exit(f"RuntimeError: {e}")


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
        run_source(sys.stdin.read(), dump_tokens=args.tokens, dump_ast=args.ast)


if __name__ == '__main__':
    main()