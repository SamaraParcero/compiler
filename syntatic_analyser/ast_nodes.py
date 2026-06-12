
# NÓS DA AST 
class Program:
    def __init__(self, commands):
        self.commands = commands

    def __repr__(self):
        return f"Program({self.commands})"


class Declaration:
    def __init__(self, type, name):
        self.type = type   
        self.name = name

    def __repr__(self):
        return f"Declaration(type='{self.type}', name='{self.name}')"


class Assignment:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"Assignment(name='{self.name}', expression={self.expression})"


class If:
    def __init__(self, condition, code_block, else_block=None):
        self.condition = condition
        self.code_block = code_block
        self.else_block = else_block

    def __repr__(self):
        return (
            f"If(condition={self.condition}, "
            f"code_block={self.code_block}, "
            f"else_block={self.else_block})"
        )


class While:
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block

    def __repr__(self):
        return f"While(condition={self.condition}, code_block={self.code_block})"


class Read:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Read(name='{self.name}')"


class Write:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Write(expression={self.expression})"


class Code_Block:
    def __init__(self, commands):
        self.commands = commands

    def __repr__(self):
        return f"Code_Block({self.commands})"


class Condition:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Condition({self.left} {self.operator} {self.right})"


class BinaryOperation:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOperation({self.left} {self.operator} {self.right})"


class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier('{self.name}')"


class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"