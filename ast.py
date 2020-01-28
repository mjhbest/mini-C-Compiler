class Expr: pass

class List(list):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)
        self.__dict__.update(kwargs)
    def __new__(self, *args, **kwargs):
        return super(List, self).__new__(self, args, kwargs)
    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)
        return self

class Func(Expr):
    def __init__(self, type, declarator, body, line):
        self.prop = "function"
        self.type = type
        if not isinstance(declarator, Params):
            raise ValueError("function parameters are unrecognizable")
        self.id = declarator.id
        self.param_list = declarator.param_list
        self.body = body
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.type} {self.id} ({self.param_list}) {self.body}]"

class Params(Expr):
    def __init__(self, id, param_list, line):
        self.prop = "params"
        self.id = id
        self.param_list = param_list
        self.line = line
    def __repr__(self):
        return f"{self.prop}: {self.id} {self.param_list}"

class FuncCall(Expr):
    def __init__(self, id, arg_list, line):
        self.prop = "fncall"
        self.id = id
        self.arg_list = arg_list
        self.line = line
    def __repr__(self):
        return f"{self.prop}: {self.id} {self.arg_list}"

class Return(Expr):
    def __init__(self, expr, line):
        self.prop = "return"
        self.expr = expr
        self.line = line

# control stmt
class If(Expr):
    def __init__(self, expr, body, line):
        self.prop = "if"
        self.expr = expr
        self.body = body
        self.line = line
    def __repr__(self):
        return f"{self.prop}: {self.expr} {self.body}"

class For(Expr):
    def __init__(self, pre, cond, post, body, line, running=False):
        self.prop = "for"
        self.pre = pre
        self.cond = cond
        self.post = post
        self.body = body
        self.line = line
        self.running = running

class While(Expr):
    def __init__(self, expr, body, line):
        self.prop = "while"
        self.expr = expr
        self.body = body
        self.line = line

class DoWhile(Expr):
    def __init__(self, expr, body, line):
        self.prop = "do-while"
        self.expr = expr
        self.body = body
        self.line = line

class LT(Expr):
    def __init__(self, left, right, line):
        self.prop = "LT"
        self.left = left
        self.right = right
class LE(Expr):
    def __init__(self, left, right, line):
        self.prop = "LE"
        self.left = left
        self.right = right
class GT(Expr):
    def __init__(self, left, right, line):
        self.prop = "GT"
        self.left = left
        self.right = right
class GE(Expr):
    def __init__(self, left, right, line):
        self.prop = "GE"
        self.left = left
        self.right = right
class EQ(Expr):
    def __init__(self, left, right, line):
        self.prop = "EQ"
        self.left = left
        self.right = right
class NE(Expr):
    def __init__(self, left, right, line):
        self.prop = "NE"
        self.left = left
        self.right = right
# ops
class Add(Expr):
    def __init__(self, left, right, line):
        self.prop = "add"
        self.left = left
        self.right = right
        self.line = line
class Minus(Expr):
    def __init__(self, left, right, line):
        self.prop = "minus"
        self.left = left
        self.right = right
        self.line = line
class Mult(Expr):
    def __init__(self, left, right, line):
        self.prop = "mult"
        self.left = left
        self.right = right
        self.line = line
class Div(Expr):
    def __init__(self, left, right, line):
        self.prop = "div"
        self.left = left
        self.right = right
        self.line = line
class Mod(Expr):
    def __init__(self, left, right, line):
        self.prop = "mod"
        self.left = left
        self.right = right
        self.line = line


class Type(Expr):
    def __init__(self, value, line):
        self.prop = "type"
        self.value = value
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.value}]"

class Array(Expr):
    def __init__(self, id, size, line):
        self.prop = "array"
        self.id = id
        self.size = size
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.id} [{self.size}]]"

class RefArray(Expr):
    def __init__(self, id, size, line):
        self.prop = "ref_array"
        self.id = id
        self.size = size
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.id} [{self.size}]]"


class Pointer(Expr):
    def __init__(self, value, line):
        self.prop = "pointer"
        self.value = value
        self.line = line
    def __repr__(self):
        return f"{self.prop}: {self.value}"

class Id(Expr):
    def __init__(self, id, line):
        self.prop = "id"
        self.id = id
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.id}]"

class Int(Expr):
    def __init__(self, value, line):
        self.prop = "int"
        self.value = value
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.value}]"

class Float(Expr):
    def __init__(self, value, line):
        self.prop = "float"
        self.value = value
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.value}]"


class Const(Expr):
    def __init__(self, value, line):
        self.prop = "const"
        self.value = value
        self.line = line
    def __repr__(self):
        return f"{self.prop}: {self.value}"

# declarations
class Declaration(Expr):
    def __init__(self, type:Type, list, line):
        self.prop = "declaration"
        self.type = type
        self.list = list
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.type} => {self.list}]"

class Assign(Expr):
    def __init__(self, id, value, line):
        self.prop = "assign"
        self.id = id
        self.value = value
        self.line = line
    def __repr__(self):
        return f"[{self.prop}: {self.id} <= {self.value}]"
