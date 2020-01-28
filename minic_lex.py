# Grammar from http://www2.ufersa.edu.br/portal/view/uploads/setores/184/AppendixA.pdf
# with few modifications
# 
# Based on ansi-c lexer by ply document
# https://github.com/dabeaz/ply/blob/master/example/ansic
#
# do not support
#   type qualifier, storage class specifier (volatile, const, static, typedef ...)
#   ternary operator ( <expr> ? <expr> : <expr> )
#   bitwise operator (|, &, ~, ^, >>, ^= ...)
#   comments (//, /* .. */)
#   types except float, int, char (not support for long, void, double, short ...)
#   label, struct, union, enum, varargs
#   pointers and there operation except malloc(), free()
#   other complex specs (this is minic!)

import lex

#########################################################
# token description
#########################################################

# Literal token must not contain these words
reserved = (
    'BREAK', 'CHAR', 'CONTINUE', 'DO', 'WHILE', 'VOID',
    'ELSE', 'FLOAT', 'FOR', 'IF', 'INT', 'RETURN', 'SWITCH', 'CASE', 'DEFAULT'
)
reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

tokens = reserved + (
    # Literals
    'ID', 'ICONST', 'FCONST', 'SCONST',

    # Operators (+,-,*,/,%, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'LOR', 'LAND', 'LNOT', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=, *=, /=, %=, +=, -=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',

    # Increment/decrement (++,--)
    'PLUSPLUS', 'MINUSMINUS',

    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',
)


#########################################################
# lexer description
#########################################################

# Completely ignored characters
t_ignore = ' \t\x0c'

# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Literals
def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t

# number
t_ICONST = r'(\d+)'
t_FCONST = r'(\d+)\.(\d+)'

# String literal
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Assignment
t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='

# Increment/decrement
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# Delimeters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'

def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()