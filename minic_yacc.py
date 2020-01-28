# Based on ansi-c yacc by ply document
# https://github.com/dabeaz/ply/blob/master/example/ansic
import yacc
import minic_lex as lex
from ast import *

tokens = lex.tokens

# translation-unit:
def p_translation_unit_1(t):
    'translation_unit : external_declaration'
    t[0] = t[1]
def p_translation_unit_2(t):
    'translation_unit : translation_unit external_declaration'
    t[0] = List(t[1], t[2])
    t[0].line = t.lineno(0)

# external-declaration:
def p_external_declaration(t):
    'external_declaration : function_definition'
    t[0] = t[1]
def p_external_declaration_2(t):
    'external_declaration : declaration'
    t[0] = t[1]

# function-definition:
def p_function_definition(t):
    'function_definition : type direct_declarator compound_statement'
    t[0] = Func(type=t[1], declarator=t[2], body=t[3], line=t.lineno(0))

# declaration-list:
def p_declaration_list_1(t):
    'declaration_list : declaration'
    t[0] = List(t[1])
    t[0].line = t.lineno(0)
def p_declaration_list_2(t):
    'declaration_list : declaration_list declaration'
    t[0] = List(t[1] + [t[2]])
    t[0].line = t.lineno(0)

# declaration:
def p_declaration_1(t):
    'declaration : type init_declarator_list SEMI'
    t[0] = Declaration(t[1], t[2], t.lineno(0))

# init-declarator-list:
def p_init_declarator_list_1(t):
    'init_declarator_list : init_declarator'
    t[0] = List(t[1])
    t[0].line = t.lineno(0)
def p_init_declarator_list_2(t):
    'init_declarator_list : init_declarator_list COMMA init_declarator'
    t[0] = List(t[1] + [t[3]])
    t[0].line = t.lineno(0)

# init-declarator
def p_init_declarator_1(t):
    'init_declarator : declarator'
    t[0] = t[1]
def p_init_declarator_2(t):
    'init_declarator : declarator EQUALS assignment_expression'
    t[0] = Assign(t[1], t[3], t.lineno(0))


# declarator:
def p_declarator_1(t):
    'declarator : pointer direct_declarator'
    t[0] = Pointer(t[2], t.lineno(0))
def p_declarator_2(t):
    'declarator : direct_declarator'
    t[0] = t[1]

# direct-declarator:
def p_direct_declarator_1(t):
    'direct_declarator : ID'
    t[0] = Id(t[1], t.lineno(0))
# def p_direct_declarator_2(t):
#     'direct_declarator : LPAREN declarator RPAREN'
#     pass
def p_direct_declarator_3(t):
    'direct_declarator : direct_declarator LBRACKET constant_expression RBRACKET'
    t[0] = Array(t[1], t[3], t.lineno(0))
def p_direct_declarator_4(t):
    'direct_declarator : direct_declarator LPAREN parameter_list RPAREN '
    t[0] = Params(t[1], t[3], t.lineno(0))
def p_direct_declarator_5(t):
    'direct_declarator : direct_declarator LPAREN arg_list RPAREN '
    t[0] = FuncCall(t[1], t[3], t.lineno(0))
    raise NotImplemented("maybe can delete")
def p_direct_declarator_6(t):
    'direct_declarator : direct_declarator LPAREN RPAREN '
    t[0] = FuncCall(t[1], [], t.lineno(0))
    raise NotImplemented("maybe can delete")

# pointer:
def p_pointer_1(t):
    'pointer : TIMES'
    t[0] = t[1]
# def p_pointer_2(t):
#     'pointer : TIMES pointer'
#     t[0] = Pointer(t[1])

# parameter-list:
def p_parameter_list_1(t):
    'parameter_list : parameter_declaration'
    t[0] = List([t[1]])
    t[0].line = t.lineno(0)
def p_parameter_list_2(t):
    'parameter_list : parameter_list COMMA parameter_declaration'
    t[0] = List(t[1] + [t[3]])
    t[0].line = t.lineno(0)
def p_parameter_list_3(t):
    'parameter_list : VOID'
    t[0] = List([])
    t[0].line = t.lineno(0)

# parameter-declaration:
def p_parameter_declaration_1(t):
    'parameter_declaration : type declarator'
    t[0] = List(t[1], t[2])
    t[0].line = t.lineno(0)

# identifier-list:
def p_arg_list_1(t):
    'arg_list : ID'
    t[0] = List(Id(t[1], t.lineno(0)))
    t[0].line = t.lineno(0)
def p_arg_list_2(t):
    'arg_list : arg_list COMMA ID'
    t[0] = List(t[1] + [Id(t[3])])
    t[0].line = t.lineno(0)


# # declarator:
# def p_declarator_1(t):
#     'declarator : TIMES ID'
#     t[0] = Pointer(t[1])
# def p_declarator_2(t):
#     'declarator : ID'
#     t[0] = t[1]
# def p_declarator_3(t):
#     'declarator : LPAREN declarator RPAREN'
#     t[0] = t[2]


# initializer-list:
def p_initializer_list_1(t):
    'initializer_list : assignment_expression'
    t[0] = t[1]
def p_initializer_list_2(t):
    'initializer_list : initializer_list COMMA assignment_expression'
    t[0] = List(t[1], t[3])
    t[0].line = t.lineno(0)

# statement:
def p_statement(t):
    '''
    statement : labeled_statement
              | expression_statement
              | compound_statement
              | selection_statement
              | iteration_statement
              | jump_statement
              '''
    t[0] = t[1]

# labeled-statement:
def p_labeled_statement_2(t):
    'labeled_statement : CASE constant_expression COLON statement'
    pass
def p_labeled_statement_3(t):
    'labeled_statement : DEFAULT COLON statement'
    pass

# expression-statement:
def p_expression_statement(t):
    'expression_statement : expression_opt SEMI'
    t[0] = t[1]

# compound-statement:
def p_compound_statement_1(t):
    'compound_statement : LBRACE declaration_list statement_list RBRACE'
    t[0] = List(t[2], t[3])
    t[0].line = t.lineno(0)
def p_compound_statement_2(t):
    'compound_statement : LBRACE statement_list RBRACE'
    t[0] = t[2]
def p_compound_statement_3(t):
    'compound_statement : LBRACE declaration_list RBRACE'
    t[0] = t[2]
def p_compound_statement_4(t):
    'compound_statement : LBRACE RBRACE'
    pass

# statement-list:
def p_statement_list_1(t):
    'statement_list : statement'
    t[0] = List(t[1])
    t[0].line = t.lineno(0)
def p_statement_list_2(t):
    'statement_list : statement_list statement'
    t[0] = List(t[1] + [t[2]])
    t[0].line = t.lineno(0)

# selection-statement
def p_selection_statement_1(t):
    'selection_statement : IF LPAREN expression RPAREN statement'
    t[0] = If(t[3], t[5], t.lineno(0))
def p_selection_statement_2(t):
    'selection_statement : IF LPAREN expression RPAREN statement ELSE statement '
    pass
def p_selection_statement_3(t):
    'selection_statement : SWITCH LPAREN expression RPAREN statement '
    pass

# iteration_statement:
def p_iteration_statement_1(t):
    'iteration_statement : WHILE LPAREN expression RPAREN statement'
    t[0] = While(t[3], t[5], t.lineno(0))
def p_iteration_statement_2(t):
    'iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement '
    t[0] = For(t[3], t[5], t[7], t[9], t.lineno(0))
def p_iteration_statement_3(t):
    'iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI'
    t[0] = DoWhile(t[5], t[2], t.lineno(0))

# jump
def p_jump_statement_2(t):
    'jump_statement : CONTINUE SEMI'
    pass
def p_jump_statement_3(t):
    'jump_statement : BREAK SEMI'
    pass
def p_jump_statement_4(t):
    'jump_statement : RETURN expression_opt SEMI'
    t[0] = Return(t[2], t.lineno(0))


# expression:
def p_expression_1(t):
    'expression : assignment_expression'
    t[0] = t[1]
def p_expression_2(t):
    'expression : expression COMMA assignment_expression'
    t[0] = List(t[1], t[3])
    t[0].line = t.lineno(0)

def p_expression_opt_1(t):
    'expression_opt : empty'
    t[0] = List([])
    t[0].line = t.lineno(0)
def p_expression_opt_2(t):
    'expression_opt : expression'
    t[0] = t[1]

# assigment_expression:
def p_assignment_expression_1(t):
    'assignment_expression : conditional_expression'
    t[0] = t[1]
def p_assignment_expression_2(t):
    'assignment_expression : unary_expression EQUALS assignment_expression'
    t[0] = Assign(t[1], t[3], t.lineno(0))

# assignment_operator:
# TODO
# def p_assignment_operator(t):
#     '''
#     assignment_operator : EQUALS
#                         | TIMESEQUAL
#                         | DIVEQUAL
#                         | MODEQUAL
#                         | PLUSEQUAL
#                         | MINUSEQUAL
#                         '''
#     pass

# conditional-expression
def p_conditional_expression_1(t):
    'conditional_expression : logical_or_expression'
    t[0] = t[1]

# constant-expression
def p_constant_expression(t):
    'constant_expression : conditional_expression'
    t[0] = t[1]

# logical-or-expression
def p_logical_or_expression_1(t):
    'logical_or_expression : logical_and_expression'
    t[0] = t[1]
def p_logical_or_expression_2(t):
    'logical_or_expression : logical_or_expression LOR logical_and_expression'
    t[0] = t[1]

# logical-and-expression
def p_logical_and_expression_1(t):
    'logical_and_expression : equality_expression'
    t[0] = t[1]
def p_logical_and_expression_2(t):
    'logical_and_expression : logical_and_expression LAND equality_expression'
    t[0] = t[1]

# equality-expression:
def p_equality_expression_1(t):
    'equality_expression : relational_expression'
    t[0] = t[1]
def p_equality_expression_2(t):
    'equality_expression : equality_expression EQ relational_expression'
    t[0] = EQ(t[1], t[3], t.lineno(0))
def p_equality_expression_3(t):
    'equality_expression : equality_expression NE relational_expression'
    t[0] = NE(t[1], t[3], t.lineno(0))

# relational-expression:
def p_relational_expression_1(t):
    'relational_expression : additive_expression'
    t[0] = t[1]
def p_relational_expression_2(t):
    'relational_expression : relational_expression LT additive_expression'
    t[0] = LT(t[1], t[3], t.lineno(0))
def p_relational_expression_3(t):
    'relational_expression : relational_expression GT additive_expression'
    t[0] = GT(t[1], t[3], t.lineno(0))
def p_relational_expression_4(t):
    'relational_expression : relational_expression LE additive_expression'
    t[0] = LE(t[1], t[3], t.lineno(0))
def p_relational_expression_5(t):
    'relational_expression : relational_expression GE additive_expression'
    t[0] = GE(t[1], t[3], t.lineno(0))

# additive-expression
def p_additive_expression_1(t):
    'additive_expression : multiplicative_expression'
    t[0] = t[1]
def p_additive_expression_2(t):
    'additive_expression : additive_expression PLUS multiplicative_expression'
    t[0] = Add(t[1], t[3], t.lineno(0))
def p_additive_expression_3(t):
    'additive_expression : additive_expression MINUS multiplicative_expression'
    t[0] = Minus(t[1], t[3], t.lineno(0))

# multiplicative-expression
def p_multiplicative_expression_1(t):
    'multiplicative_expression : unary_expression'
    t[0] = t[1]
def p_multiplicative_expression_2(t):
    'multiplicative_expression : multiplicative_expression TIMES unary_expression'
    t[0] = Mult(t[1], t[3], t.lineno(0))
def p_multiplicative_expression_3(t):
    'multiplicative_expression : multiplicative_expression DIVIDE unary_expression'
    t[0] = Div(t[1], t[3], t.lineno(0))
def p_multiplicative_expression_4(t):
    'multiplicative_expression : multiplicative_expression MOD unary_expression'
    t[0] = Mod(t[1], t[3], t.lineno(0))

# unary-expression:
def p_unary_expression_1(t):
    'unary_expression : postfix_expression'
    t[0] = t[1]
def p_unary_expression_2(t):
    'unary_expression : PLUSPLUS unary_expression'
    t[0] = Assign(t[2], Add(Int(1, t.lineno(0)), t[2], t.lineno(0)), t.lineno(0))
def p_unary_expression_3(t):
    'unary_expression : MINUSMINUS unary_expression'
    t[0] = Assign(t[2], Minus(Int(1, t.lineno(0)), t[2], t.lineno(0)), t.lineno(0))
def p_unary_expression_4(t):
    'unary_expression : unary_operator postfix_expression'
    t[0] = t[1]
    raise NotImplemented("unsupported format")

# unary-operator
def p_unary_operator(t):
    '''unary_operator : TIMES
                    | PLUS 
                    | MINUS
                    | LNOT '''
    t[0] = t[1]

# postfix-expression:
def p_postfix_expression_1(t):
    'postfix_expression : primary_expression'
    t[0] = t[1]
def p_postfix_expression_2(t):
    'postfix_expression : postfix_expression LBRACKET expression RBRACKET'
    t[0] = RefArray(t[1], t[3], t.lineno(0))
def p_postfix_expression_3(t):
    'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
    t[0] = FuncCall(t[1], t[3], t.lineno(0))
def p_postfix_expression_4(t):
    'postfix_expression : postfix_expression LPAREN RPAREN'
    t[0] = FuncCall(t[1], [], t.lineno(0))
def p_postfix_expression_5(t):
    'postfix_expression : postfix_expression PERIOD ID'
    t[0] = t[1]
def p_postfix_expression_7(t):
    'postfix_expression : postfix_expression PLUSPLUS'
    t[0] = Assign(t[1], Add(t[1], Int(1, t.lineno(0)), t.lineno(0)), t.lineno(0))
def p_postfix_expression_8(t):
    'postfix_expression : postfix_expression MINUSMINUS'
    t[0] = Assign(t[1], Minus(t[1], Int(1, t.lineno(0)), t.lineno(0)), t.lineno(0))

# primary-expression:
def p_primary_expression_1(t):
    'primary_expression : ID'
    t[0] = Id(t[1], line=t.lineno(0))
def p_primary_expression_2(t):
    'primary_expression : ICONST'
    t[0] = Int(t[1], t.lineno(0))
def p_primary_expression_3(t):
    'primary_expression : FCONST'
    t[0] = Float(t[1], t.lineno(0))
def p_primary_expression_4(t):
    'primary_expression : SCONST'
    t[0] = Const(t[1], t.lineno(0))
def p_primary_expression_5(t):
    'primary_expression : LPAREN expression RPAREN'''
    t[0] = t[2]

# argument-expression-list:
def p_argument_expression_list_1(t):
    'argument_expression_list :  assignment_expression'
    t[0] = List(t[1])
    t[0].line = t.lineno(0)
def p_argument_expression_list_2(t):
    'argument_expression_list : argument_expression_list COMMA assignment_expression'
    t[0] = List(t[1] + [t[3]])
    t[0].line = t.lineno(0)

# type
def p_type(t):
    '''type : INT
            | CHAR
            | FLOAT'''
    t[0] = Type(t[1], t.lineno(0))

# empty
def p_empty(t):
    'empty : '
    pass

# error
def p_error(t):
    print(f'Syntax error at line number: {t.lineno}')

parser = yacc.yacc()

if __name__ == "__main__":
    file = open("test.txt", 'r')
    line = file.readlines()
    txt = "".join(line)
    result = parser.parse(txt, lexer=lex.lexer, tracking=True)
    from collections.abc import Iterable
    if isinstance(result, Iterable):
        for i in result:
            print(i)
    else:
        print(result)
