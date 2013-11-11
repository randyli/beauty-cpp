import ply.lex as lex
keywords = {
"alignas":2, "alignof":2, "anda":2, "and_eq":2, "asm":2, "auto":2, "bitand":2,
"bitor":2, "bool":2, "break":1, "case":1, "catch":1, "char":2, "char16_t":2,
"char32_t":2, "class":2, "compl":2, "const":1, "constexpr":1, "const_cast":1,
"continue":1, "decltype":2, "default":1, "delete":1, "do":1, "double":2,
"dynamic_cast":2, "else":1, "enum":2, "explicit":1, "export":2, "extern":1,
"false":1, "float":2, "for":1, "friend":1, "goto":1, "if":1, "inline":1, "int":2,
"long":2, "mutable":1, "namespace":2, "new":1, "noexcept":2, "not":1, "not_eq":1,
"nullptr":2, "operator":1, "or":1, "or_eq":1, "private":1, "protected":1, "public":1,
"register":1, "reinterpret_cast":2, "return":1, "short":2, "signed":2, "sizeof":2,
"static":1, "static_assert":1, "static_cast":2, "struct":2, "switch":1, 
"template":2, "this":1, "thread_local":2, "throw":1, "true":1, "try":1, "typedef":2,
"typeid":2, "typename":1, "union":2, "unsigned":2, "using":1, "virtual":1,
"void":2, "volatile":1, "wchar_t":2, "while":1, "xor":1, "xor_eq":1,"size_t":2,
"uint64_t":1, "unit32_t":1
}

tokens = (
  'HEX',
  'FLOAT',
  'NUMBER',
  'KEYWORD',
  'ID',
  'INCLUDE',
  'STRING',
  'SCOMMENT',
  'MCOMMENT',
  'COMMENT_END',
  'BLACK',
  'TAB',
  'NEWLINE'
)
literals = "+-*/{}[]()<>;?\:\\&^%$#@!~|.,='"

states = (('mcomment', 'exclusive'),)

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  keyword_type = keywords.get(t.value) 
  if keyword_type is not None:
    t.html = '<span class="bc_keyword_%d">%s</span>'%(keyword_type,t.value)
    t.type = 'KEYWORD'
  else:
    t.type = 'ID'
  return t

def t_HEX(t):
  r'0[xX][0-9a-fA-F]+'
  t.html = '<span class="bc_number">%s</span>'%t.value
  return t

def t_FLOAT(t):
  r'(\d+)(\.\d+)+'
  t.html = '<span class="bc_number">%s</span>'%t.value
  return t

def t_NUMBER(t):
  r'\d+' 
  t.html = '<span class="bc_number">%s</span>'%t.value
  return t

def t_STRING(t):
  r'\"([^\\\n]|(\\.))*?\"'
  t.html = '<span class="bc_string">%s</span>'%t.value
  return t

def t_INCLUDE(t):
  r'\#include[ \t]*((<.+>)|(\".+\"))'
  inc_type = '<' 
  start = t.value.find('<')
  if start == -1:
    start = t.value.find('"')
    inc_type = '"'
  end = t.value.find('>')
  if end == -1:
    end = t.value.find('"', start+1)
  f = t.value[start+1:end].strip()
  t.inc_type = inc_type
  t.inc = f
  t.lexpos = t.lexpos + t.value.find(f) - 1
  return t

def t_SCOMMENT(t):
  r'//.*'
  t.html = '<span class="bc_comment">%s</span>'%t.value
  return t

def t_MCOMMENT(t):
  r'/\*'
  t.lexer.comment_start = t.lexer.lexpos - 2
  t.lexer.begin('mcomment')

def t_mcomment_COMMENTEND(t):
  r'\*/'
  t.value = t.lexer.lexdata[t.lexer.comment_start:t.lexer.lexpos]
  t.type = 'MCOMMENT'
  t.lexer.begin('INITIAL')
  lines = t.value.split('\n')
  t.html = []
  for l in lines:
    h = '<span class="bc_comment">%s</span>'%l
    t.html.append(h)
  t.lexer.lineno+=len(t.html) - 1
  if len(t.html) == 1:
    t.html = t.html[0]
  return t

def t_mcomment_nonspace(t):
  r'(?!\*/).'

def t_mcomment_error(t):
  t.lexer.skip(1)

def t_NEWLINE(t):
  r'\n'
  t.lexer.lineno += 1
  return t

def t_BLACK(t):
  r'[ ]'
  t.html = '&nbsp;'
  return t

def t_TAB(t):
  r'\t'
  t.html = '&emsp;'
  return t

def t_error(t):
  print 'Illegal character %s'%t.value
  quit()
  t.lexer.skip(1)
'''
lexer = lex.lex()
f = open('test.cpp')
data = f.read()
lexer.input(data)
while True:
  t = lexer.token()
  if not t: break
  print t
'''
