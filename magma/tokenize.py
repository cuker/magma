
reserved = { 
    'actor': 'ACTOR',
    'role': 'ROLE',
    'action': 'ACTION',
    'task': 'TASK',
    'script': 'SCRIPT',
    'requires': 'REQUIRES',
    'description': 'DESCRIPTION',
    'package' : 'NAMESPACE',
}

tokens = [
    'COMMENT',
    'NEWLINE', 
    'WHITESPACE', 
    'BLOCKSTART', 
    'BLOCKEND', 
    'ID',
    'LPAREN',
    'RPAREN',
    'LISTDELIM',
    'STRING',
] + list(reserved.values())

t_BLOCKSTART = r'{'
t_BLOCKEND = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LISTDELIM = r'\,'
t_DESCRIPTION = r'\:.*'
t_STRING = r'".*"'

def t_WHITESPACE(t):
    r'[ 	]+'
    pass

def t_COMMENT(t):
    r'\#.*'
    pass
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    pass  

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print "Illegal Character: %s" % t.value[0]
    t.lexer.skip(1)

import ply.lex as lex
lex.lex()

if __name__ == "__main__":
    f = open ("blog.magma")
    contents = f.read()
    lex.input(contents)
    while 1:
        tok = lex.token()
        print tok
        if not tok:
             break
