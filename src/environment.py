from src.errors import GridScriptError


class Environment:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def set(self, name, value):
        self.bindings[name] = value

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise GridScriptError(f"undefined variable '{name}'")

    def has_local(self, name):
        return name in self.bindings

    def child(self):
        return Environment(self)