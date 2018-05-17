# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'SUP', 'INF', 'SUPEG', 'INFEG',
    'EG', 'NEG', 'OR', 'AND', 'SEMICOLON', 'SI', 'ALORS', 'SINON'
    )

# Tokens


t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_EQUALS   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_NAME     = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SUP      = r'>'
t_INF      = r'<'
t_SUPEG    = r'>='
t_INFEG    = r'<='
t_EG       = r'=='
t_NEG      = r'!='
t_OR       = r'OR'
t_AND      = r'AND'
t_SEMICOLON= r';'
t_SI       = r'SI'
t_ALORS    = r'ALORS'
t_SINON    = r'SINON'

global res


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caractére non autorisé : '%s'" % t.value[0])
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

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):

    '''statement : expression
                 | expression SEMICOLON statement
                 | '''
    for index in range(len(p)):
        if index != 0 and index == 1:
            print(p[index])
    #eval(p)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

    
    print("Résultat '%s'" % p[0])
    t = []
    t.append(p[2])
    t.append(p[1])
    t.append(p[3])
    p[0] = tuple(t)#remontée
    
    #print(p[0])
    

def p_expression_aff(p):
    'expression : expression EQUALS expression'
    p[0] = p[3]
    print(p[0])

def p_expression_bool(p):
    '''expression : expression SUP expression
                  | expression INF expression
                  | expression SUPEG expression
                  | expression INFEG expression
                  | expression EG expression
                  | expression NEG expression
                  | expression OR expression
                  | expression AND expression'''
    
    if p[2] == '==' : p[0] = p[1] == p[3]
    elif p[2] == '>': p[0] = p[1] > p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '<=': p[0] = p[1] <= p[3]
    elif p[2] == '>=': p[0] = p[1] >= p[3]
    elif p[2] == '!=': p[0] = p[1] != p[3]
    elif p[2] == 'OR' : p[0] = (p[1] == True) or (p[3] == True)
    elif p[2] == 'AND' : p[0] = (p[1] == True) and (p[3] == True)
    elif p[1] == '!' : p[0] = p[2] == False

    #print(p[0])
    
    #t = []
    #t.append(p[2])
    #t.append(p[1])
    #t.append(p[3])
    #p[0] = tuple(t)

    #print(p[0])

def eval(tulpe):
    #test = [tulpe[1][1], tulpe[1][0], tulpe[1][2]]

    if tulpe[1][0] == '+'  : tulpe[0] = tulpe[1][1] + tulpe[1][2]
    elif tulpe[1][0] == '-'  : tulpe[0] = tulpe[1][1] - tulpe[1][2]
    elif tulpe[1][0] == '*'  : tulpe[0] = tulpe[1][1] * tulpe[1][2]
    elif tulpe[1][0] == '/'  : tulpe[0] = tulpe[1][1] / tulpe[1][2]
    print(tulpe[0])
    #print(test)
    #p_expression_binop(test)
   

def p_statement_cond(p):
    '''expression : expression SI expression
                  | expression ALORS expression
                  | expression SINON expression'''

    if[2] == 'SI' : print("SI envoyé")
    if[1] == 'SI' : print("si en 1")
    

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
        print("Caractère non connu : '%s'" % p[1])
        p[0] = 0

def p_error(p):
    print("Erreure de syntaxe à : '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('Calculons -> ')   # use input() on Python 3
    except EOFError:
        break
    if s != "":
        yacc.parse(s)

