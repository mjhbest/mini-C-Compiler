from minic_lex import lexer
from minic_yacc import parser
from visitor import *
import re

file = open("main.txt", 'r')
line = file.readlines()
txt = "".join(line)
result = parser.parse(txt, lexer=lexer, tracking=True)

v = Visitor(tracking=True)
v.visit(result)
v.push_main()

while True:
    cmd = input(">> ")

    # mem
    if cmd == "mem":
        v.memory.mem()

    # next
    if cmd == "next":
        v.run(1)
        continue
    m = re.match("next (\d+)", cmd)
    if m:
        v.run(int(m.group(1)))
        continue

    # print
    m = re.match("print (\w+)", cmd)
    if m:
        try:
            value = v.callstack.find(m.group(1))
            print(value["value"])
        except:
            "unimportant"
        continue

    # trace
    m = re.match("trace (\w+)", cmd)
    if m:
        try:
            v.callstack.trace(m.group(1))
        except:
            "unimportant"
        continue