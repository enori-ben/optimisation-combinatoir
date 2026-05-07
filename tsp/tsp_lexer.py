import ply.lex as lex

tokens = (
   'NUMBER',
   'DIMENSION',
   'COORDINATION_SECTION',
   'EOF',
   'NAME'
)

reserved = {
    'DIMENSION': 'DIMENSION',
    'NODE_COORD_SECTION': 'COORDINATION_SECTION',
    'DISPLAY_DATA_SECTION': 'COORDINATION_SECTION',
    'EOF': 'EOF',
    'NAME':'NAME',       
}

def t_NAME(t):
    r'NAME\s*:\s*\S+'
    t.value = t.value.split(':', 1)[1].strip()
    return t


def t_NUMBER(t):
    r'(?<=\s|:)[+-]?\d+(\.\d+)?([eE][+-]?\d+)?(?=\s|$)'
    t.value = float(t.value)
    return t



flag = 1

def t_DIMENSION(t):
    r'DIMENSION\s*:\s*'
    return t

t_COORDINATION_SECTION = r'NODE_COORD_SECTION|DISPLAY_DATA_SECTION'

t_EOF = 'EOF'
t_ignore = ' \t' 

def t_error(t):
    
    line_end = t.value.find('\n')
    
    if line_end != -1:
        
        t.lexer.skip(line_end)
    else:
        
        t.lexer.skip(len(t.value))

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def p_error(p):
    if p:
        print(f"Token Error: {p.type} ('{p.value}') at line {p.lineno}")
    else:
        print("Unexpected End of File (EOF)")

# Build the lexer
lexer = lex.lex()




