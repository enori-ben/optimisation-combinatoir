import ply.lex as lex
 
 
tokens = (
    "INSTANCE_NAME",
    "COLON",
    "NUMBER",
)
 
 
# INSTANCE_NAME: starts with a letter or digit, may contain letters, digits,
# and underscores (covers names like kroA100, dantzig42, linhp318, …)
def t_INSTANCE_NAME(t):
    r"[A-Za-z][A-Za-z0-9_]*|[0-9]+[A-Za-z][A-Za-z0-9_]*"
    return t
 
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t
 
t_COLON = r":"
 
# Ignore whitespace and newlines
t_ignore = " \t\n\r"
 
def t_error(t):
    print(f"[Lexer] Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)
 
 
lexer = lex.lex()