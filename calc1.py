#-----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------
from ast import literal_eval as make_tuple

tokens = (
   'NAME','NUMBER',
   'PLUS','MINUS','TIMES','DIVIDE',
   'LPAREN','RPAREN', 'SEMICOLON'
   )

# Tokens


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SEMICOLON=r';'

def t_NUMBER(t):
   r'\d+'
   t.value = int(t.value)
   return t

t_ignore = " \t"

def t_newline(t):
   r'\n+'
   t.lexer.lineno += t.value.count("\n")

def t_error(t):
   print("Illegal character '%s'" % t.value[0])
   t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
   ('left','PLUS','MINUS'),
   ('left','TIMES','DIVIDE'),
   ('right','UMINUS')
   )

def p_statement_expr(p):
   '''statement : expression
             | statement SEMICOLON statement SEMICOLON'''
   print(p[1])

def p_expression_binop(p):
   '''expression : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression'''
   
   t = []
   t.append(p[2])
   t.append(p[1])
   t.append(p[3])

   p[0] = tuple(t)

def p_expression_uminus(p):
   'expression : MINUS expression %prec UMINUS'
   p[0] = -p[2]

def p_expression_group(p):
   'expression : LPAREN expression RPAREN'
   p[0] = p[2]

def p_expression_number(p):
   'expression : NUMBER'
   p[0] = p[1]

def p_expression_name(p):
   'expression : NAME'
   try:
       p[0] = names[p[1]]
   except LookupError:
       print("Undefined name '%s'" % p[1])
       p[0] = 0

def p_error(p):
   print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

while True:
   try:
       s = input('calc > ')   # use input() on Python 3

   except EOFError:
       break
   yacc.parse(s)
