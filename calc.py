from graph import printTreeGraph

#bloc -> bloc statement | statement
#start -> bloc
#p[0] = p[1]
#eval(p[0])

#Doc lex 4.3 if dans le docx

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'SUP', 'INF', 'SUPEG', 'INFEG',
    'EG', 'NEG', 'SEMICOLON', 'THEN', 'IF', 'ELSE', 'NOT', 'AND', 'OR'
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
t_NOT      = r'!'
#t_AND      = r'and'
t_OR       = r'OR'
t_SEMICOLON= r';'


#global res

reserved = {
   'and': 'AND',
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE'
}

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

    printTreeGraph((p[2], p[1], p[3]))

def p_statement_expr(p):

    '''statement : expression
                 | expression SEMICOLON statement
                 | '''

    #print(eval(p[0]))
    
    for index in range(len(p)):
        if index != 0 and index == 1:
            #print(p[index])
            pass

    #printTreeGraph((p[2], p[1], p[3]))

            
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

    printTreeGraph(p[0])

    print(eval(p[0]))

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

    t = []
    t.append(p[2])
    t.append(p[1])
    t.append(p[3])
    
    p[0] = tuple(t)

    printTreeGraph(p[0])
    print(eval(p[0]))
    
    #if p[2] == '==' : p[0] = p[1] == p[3]
    #elif p[2] == '>': p[0] = p[1] > p[3]
    #elif p[2] == '<': p[0] = p[1] < p[3]
    #elif p[2] == '<=': p[0] = p[1] <= p[3]
    #elif p[2] == '>=': p[0] = p[1] >= p[3]
    #elif p[2] == '!=': p[0] = p[1] != p[3]
    #elif p[2] == 'OR' : p[0] = (p[1] == True) or (p[3] == True)
    #elif p[2] == 'AND' : p[0] = (p[1] == True) and (p[3] == True)
    #elif p[1] == '!' : p[0] = p[2] == False

def eval(t):
    if type(t) is not tuple:
        return t

    if t[0] == '+':
        return eval(t[1]) + eval(t[2])
    elif t[0] == '-':
        return eval(t[1]) - eval(t[2])
    elif t[0] == '*':
        return eval(t[1]) * eval(t[2])
    elif t[0] == '/':
        return eval(t[1]) / eval(t[2])
    
    elif t[0] == '==':
        return eval(t[1]) == eval(t[2])
    elif t[0] == '!=':
        return eval(t[1]) != eval(t[2])
    elif t[0] == '>':
        return eval(t[1]) > eval(t[2])
    elif t[0] == '<':
        return eval(t[1]) < eval(t[2])
    elif t[0] == '<=':
        return eval(t[1]) <= eval(t[2])
    elif t[0] == 'OR':
        return eval(t[1]) or eval(t[2])
    elif t[0] == 'AND':
        return eval(t[1]) and eval(t[2])
    elif t[0] == '!':
        return not eval(t[1])
    

    #print(tulpe[0])
    #print(test)
    #p_expression_binop(test)
    

def p_statement_cond(p):
    '''expression : expression IF expression
                  | expression THEN expression
                  | expression ELSE expression'''

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN
                  | expression'''
    
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
    print("Erreur de syntaxe à : '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('Calculons -> ')   # use input() on Python 3
    except EOFError:
        break
    if s != "":
        yacc.parse(s)
