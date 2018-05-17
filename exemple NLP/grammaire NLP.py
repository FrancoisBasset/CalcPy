# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'NOM', 'VERBE', 'DET'
    )

# Tokens

 

def t_NOM(t):
    r'chat|chien'
    return t
    
def t_VERBE(t):
    r'mangeait|chassait'
    return t
    
def t_DET(t):
    r'le|un'
    return t
# Ignored characters
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

 

# dictionary of names (for storing variables)
names = { }
def p_phrase(p):
    'phrase : GroupeNom VERBE GroupeNom'
    p[0]=(p[1], p[2], p[3])
    print(p[0])
    
    
def p_GroupeNominal(p):
    'GroupeNom : DET NOM'
    #p[0]=(p[1], p[2])
    print(p[1], p[2])
    
 

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('calc > ')   # use input() on Python 3
    except EOFError:
        break
    if(s is 'stop'): break
    yacc.parse(s)