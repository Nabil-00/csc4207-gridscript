from src.environment import Environment
from src.builtins import make_builtins
from src.errors import GridScriptError


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.env = Environment()
        builtins = make_builtins()
        for name, fn in builtins.items():
            self.env.set(name, fn)

    def error(self, msg):
        raise GridScriptError(msg)

    def interpret(self, node):
        return self.visit(node)

    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        return getattr(self, method)(node)

    def visit_Program(self, node):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result

    def visit_Assign(self, node):
        value = self.visit(node.expr)
        self.env.set(node.name, value)
        return value

    def visit_Print(self, node):
        value = self.visit(node.expr)
        print(str(value).lower() if isinstance(value, bool) else value)
        return value

    def visit_If(self, node):
        cond = self.visit(node.condition)
        if not isinstance(cond, bool):
            self.error(f"if condition must be a Boolean, got {self._type_name(cond)}")
        if cond:
            return self._run_block(node.then_body)
        else:
            return self._run_block(node.else_body)

    def visit_While(self, node):
        result = None
        while True:
            cond = self.visit(node.condition)
            if not isinstance(cond, bool):
                self.error(f"while condition must be a Boolean, got {self._type_name(cond)}")
            if not cond:
                break
            result = self._run_block(node.body)
        return result

    def visit_FunctionDef(self, node):
        closure = (node.params, node.body, self.env)
        self.env.set(node.name, closure)
        return None

    def visit_Return(self, node):
        value = self.visit(node.expr)
        raise ReturnException(value)

    def visit_Call(self, node):
        callee = self.env.get(node.name)
        args = [self.visit(a) for a in node.args]

        if callable(callee):
            return callee(*args)

        if isinstance(callee, tuple):
            params, body, def_env = callee
            if len(args) != len(params):
                self.error(
                    f"function '{node.name}' expects {len(params)} arguments, got {len(args)}"
                )
            old_env = self.env
            self.env = Environment(def_env)
            for p, a in zip(params, args):
                self.env.set(p, a)
            try:
                result = self._run_block(body)
                self.env = old_env
                return 0 if result is None else result
            except ReturnException as e:
                self.env = old_env
                return e.value

        self.error(f"'{node.name}' is not callable")

    def _type_name(self, val):
        if isinstance(val, bool):
            return 'Boolean'
        if isinstance(val, int):
            return 'Number'
        if isinstance(val, str):
            return 'String'
        return type(val).__name__

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == '+':
            if isinstance(left, int) and isinstance(right, int):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            self.error(f"cannot add {self._type_name(left)} and {self._type_name(right)}")

        elif node.op == '-':
            if isinstance(left, int) and isinstance(right, int):
                return left - right
            self.error(f"cannot subtract {self._type_name(left)} and {self._type_name(right)}")

        elif node.op == '*':
            if isinstance(left, int) and isinstance(right, int):
                return left * right
            self.error(f"cannot multiply {self._type_name(left)} and {self._type_name(right)}")

        elif node.op == '/':
            if isinstance(left, int) and isinstance(right, int):
                if right == 0:
                    self.error("division by zero")
                return left // right
            self.error(f"cannot divide {self._type_name(left)} and {self._type_name(right)}")

        elif node.op == '<':
            if isinstance(left, int) and isinstance(right, int):
                return left < right
            self.error(f"cannot compare {self._type_name(left)} and {self._type_name(right)} with '<'")

        elif node.op == '>':
            if isinstance(left, int) and isinstance(right, int):
                return left > right
            self.error(f"cannot compare {self._type_name(left)} and {self._type_name(right)} with '>'")

        elif node.op == '==':
            return left == right

        elif node.op == '!=':
            return left != right

        self.error(f"unknown operator '{node.op}'")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if node.op == '-':
            if not isinstance(operand, int):
                self.error(f"cannot negate {self._type_name(operand)}")
            return -operand
        self.error(f"unknown unary operator '{node.op}'")

    def visit_Literal(self, node):
        return node.value

    def visit_Variable(self, node):
        return self.env.get(node.name)

    def _run_block(self, statements):
        result = None
        for stmt in statements:
            result = self.visit(stmt)
        return result