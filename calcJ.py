# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN' , 'SEMICOLON','EQUALS_EQUALS','SUPERIOR','SUPERIOR_EQUALS','INFERIOR','INFERIOR_EQUALS','DIFFERENT','NOT'
    )

# Tokens


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SEMICOLON = r';'
t_EQUALS_EQUALS = r'=='
t_SUPERIOR = r'>'
t_SUPERIOR_EQUALS = r'>='
t_INFERIOR = r'<'
t_INFERIOR_EQUALS = r'<='
t_DIFFERENT = r'!='
t_NOT = r'!'

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

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    #'''statement : statement expression SEMICOLON
     #            | expression SEMICOLON '''
    #if len(p) == 3: print(p[1])
    #if len(p) == 4: print(p[2])

    
    '''statement : expression
                 | expression SEMICOLON statement
                 | '''
    for index in range(len(p)):
        if index != 0 and index == 1:
            print(p[index])
    eval(p)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = (p[2], p[1], p[3])
 
  

def p_expression_bool(p):
    
    '''expression : expression EQUALS_EQUALS expression
                  | expression SUPERIOR expression
                  | expression SUPERIOR_EQUALS expression
                  | expression INFERIOR expression
                  | expression DIFFERENT expression
                  | NOT expression
                  | expression INFERIOR_EQUALS expression
                  | expression NAME expression'''
    if p[2] == '==' : p[0] = p[1] == p[3]
    elif p[2] == '<' : p[0] = p[1] < p[3]
    elif p[2] == '<=' : p[0] = p[1] <= p[3]
    elif p[2] == '>' : p[0] = p[1] > p[3]
    elif p[2] == '>=' : p[0] = p[1] >= p[3]
    elif p[2] == '!=' : p[0] = p[1] != p[3]
    elif p[2] == 'OR' : p[0] = (p[1] == True) or (p[3] == True)
    elif p[2] == 'AND' : p[0] = (p[1] == True) and (p[3] == True)
    elif p[1] == '!' : p[0] = p[2] == False
   
    
def eval(tulpe):
    #test = [tulpe[1][1], tulpe[1][0], tulpe[1][2]]

    if tulpe[1][0] == '+'  : tulpe[0] = tulpe[1][1] + tulpe[1][2]
    elif tulpe[1][0] == '-'  : tulpe[0] = tulpe[1][1] - tulpe[1][2]
    elif tulpe[1][0] == '*'  : tulpe[0] = tulpe[1][1] * tulpe[1][2]
    elif tulpe[1][0] == '/'  : tulpe[0] = tulpe[1][1] / tulpe[1][2]
    print(tulpe[0])
    #print(test)
    #p_expression_binop(test)
   

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
