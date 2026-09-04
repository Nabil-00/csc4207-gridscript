from dataclasses import dataclass
from typing import Any


@dataclass
class Program:
    statements: list


@dataclass
class Assign:
    name: str
    expr: Any


@dataclass
class Print:
    expr: Any


@dataclass
class If:
    condition: Any
    then_body: list
    else_body: list


@dataclass
class While:
    condition: Any
    body: list


@dataclass
class FunctionDef:
    name: str
    params: list
    body: list


@dataclass
class Return:
    expr: Any


@dataclass
class Call:
    name: str
    args: list


@dataclass
class BinaryOp:
    op: str
    left: Any
    right: Any


@dataclass
class UnaryOp:
    op: str
    operand: Any


@dataclass
class Literal:
    value: Any


@dataclass
class Variable:
    name: str
