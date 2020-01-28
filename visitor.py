import math
from ast import *
from callstack import *
from memory import *

# TODO
# 1. add implicit type conversion :
#   coerse with respect to their type when assign and declare inside visitor
# 2. pointer
# 3. fix next command on list (with function call?)

class Visitor():
    def __init__(self, tracking=False):
        self.callstack = Callstack()
        self.fn_table = {}
        self.running = None
        self.tracking = tracking
        self.memory = Memory()

    def visit(self, node, line=math.inf, parent_line=None):
        method_name = type(node).__name__
        route = getattr(self, method_name, self.error)
        if self.tracking:
            print(method_name)
        if parent_line != None:
            line -= node.line - parent_line
        if line <= 0:
            return node
        return route(node, line)

    def push_main(self):
        main = self.fn_table.get("main")
        if main == None:
            print("main function must be needed")
            exit(1)
        self.callstack.push()
        self.running = main['node'].body

    def run(self, line=1):
        if self.running == None:
            print("End of program")
            exit(0)

        self.running = self.visit(self.running, line)
        if self.tracking:
            print("visit>>> ", self.running)

    def error(self, node, line):
        raise NotImplemented(type(node).__name__ + " is not implemented")

    def value(self, node):
        value = self.visit(node)
        if type(value) == str:
            return self.callstack.find(value)["value"]
        return value

    def NoneType(self, node, line): pass
    def str(self, node, line=None): pass

    def List(self, node, line):
        result = List()
        result.line = node.line

        # FIXME
        toggle = True

        for i in node:
            r = self.visit(i, line, node.line)
            if r != None:
                result.append(r)
                if toggle:
                    result.line = i.line
                    toggle = False
        if result == []:
            return None
        return result

    # nodes
    def Declaration(self, node, line):
        type = self.visit(node.type)
        for i in node.list:
            self.visit(i)
            id = self.visit(i.id)
            quiet = isinstance(i, Array)
            self.callstack.add(id, { 'id': id, 'line': node.line, 'type': type }, quiet=quiet)

    def Assign(self, node, line):
        # special treatment for array
        if isinstance(node.id, RefArray):
            ref = node.id
            id = self.visit(ref.id)
            value = self.visit(node.value)
            size = self.visit(ref.size)
            s = self.callstack.find(id)
            s["value"].update({size: value})
            s["trace"].append({"value": s["value"].copy(), "line": ref.line})
            return None

        id = self.visit(node.id)
        value = self.value(node.value)
        self.callstack.add(id, { 'id': id, 'value': value, 'line': node.line })
        return None

    def Func(self, node, line):
        # save node and apply again if called
        id = self.visit(node.id)
        type = self.visit(node.type)
        param_list = self.visit(node.param_list)
        self.fn_table[id] = { 'id': id, 'type': type, 'param_list': param_list, 'node': node }
        return None

    # TODO line
    def FuncCall(self, node, line):
        # lookup fn_table
        id = self.visit(node.id)

        # built-ins
        if id == "printf":
            if len(node.arg_list) == 1:
                return print(self.visit(node.arg_list[0]))
            arg = ()
            for i in node.arg_list[1:]:
                r = self.value(i)
                arg += (r,)
            return print(self.visit(node.arg_list[0]) % arg)
        elif id == "malloc":
            return self.memory.alloc(self.value(node.arg_list[0]))
        elif id == "free":
            self.memory.free(self.value(node.arg_list[0]))
            return None

        fn = self.fn_table.get(id)
        if fn == None:
            raise ValueError("try to call undefined function")

        # check number of args
        param_list = fn['param_list']
        if param_list == None: param_list = []
        if len(node.arg_list) != len(param_list):
            raise ValueError(f'try to call funcation: {id} with different size of argument, expected {len(param_list)}, given {len(node.arg_list)}')

        # check type of args
        to_push = []
        for (arg, [type, id]) in zip(node.arg_list, param_list):
            if isinstance(arg, Id):
                symbol = self.callstack.find(arg.id)
                if symbol['type'] != type:
                    raise ValueError(f'try to call function: {id} with wrong type, expected {type}, given {symbol["type"]}')
                value = symbol['value']
            elif isinstance(arg, Int):
                if type != 'int':
                    raise ValueError(f'try to call function: {id} with wrong type, expected {type}, given int')
                value = arg.value
            elif isinstance(arg, Float):
                if type != 'float':
                    raise ValueError(f'try to call function: {id} with wrong type, expected {type}, given float')
                value = arg.value
            else:
                raise ValueError(f'unsupported argument type for function: {arg}')
            to_push.append((type, id, value))

        # accepted function
        # add new callstack -> push variable to stack -> run saved node
        self.callstack.push()
        for (type, id, value) in to_push:
            self.callstack.add(id, { 'id': id, 'line': line, 'type': type, 'line': node.line})
        return self.visit(fn["node"].body)[0]

    def Return(self, node, line):
        self.callstack.pop()
        return self.value(node.expr)

    def If(self, node, line):
        value = self.value(node.expr)
        if value:
            return self.visit(node.body)

    def For(self, node, line):
        if not node.running:
            self.visit(node.pre)
        if self.value(node.cond):
            self.visit(node.body)
            self.visit(node.post)
            return For(node.pre, node.cond, node.post, node.body, node.line, running=True)
        return None

    def While(self, node, line):
        if self.value(node.expr):
            self.visit(node.body)
            return While(node.expr, node.body, node.line)
        return None

    def DoWhile(self, node, line):
        self.visit(node.body)
        if self.value(node.expr):
            return While(node.expr, node.body, node.line)
        return None

    # cond
    def LT(self, node, line):
        return int(self.value(node.left) < self.value(node.right))
    def LE(self, node, line):
        return int(self.value(node.left) <= self.value(node.right))
    def GT(self, node, line):
        return int(self.value(node.left) > self.value(node.right))
    def GE(self, node, line):
        return int(self.value(node.left) >= self.value(node.right))
    def EQ(self, node, line):
        return int(self.value(node.left) == self.value(node.right))
    def NE(self, node, line):
        return int(self.value(node.left) != self.value(node.right))

    def Add(self, node, line):
        return self.value(node.left) + self.value(node.right)
    def Minus(self, node, line):
        return self.value(node.left) - self.value(node.right)
    def Mult(self, node, line):
        return self.value(node.left) * self.value(node.right)
    def Div(self, node, line):
        return self.value(node.left) / self.value(node.right)
    def Mod(self, node, line):
        return self.value(node.left) % self.value(node.right)

    def Array(self, node, line):
        # array assign is done here, only empty form is allowed. i.e. int a[5];
        id = self.visit(node.id)
        size = self.visit(node.size)
        self.callstack.add(id, {
            'id': id, 'value': {}, 'line': node.line,
            'trace': [{"value": {}, "line": node.line}]
        }, quiet=True)
        return id

    def RefArray(self, node, line):
        # find value from callstack
        id = self.visit(node.id)
        size = self.visit(node.size)
        return self.callstack.find(id)["value"][size]

    def Id(self, node, line):
        return node.id
    def Type(self, node, line):
        return node.value
    def Int(self, node, line):
        return int(node.value)
    def Float(self, node, line):
        return float(node.value)
    def Const(self, node, line):
        return node.value

    def Pointer(self, node, line):
        return self.visit(node.value)