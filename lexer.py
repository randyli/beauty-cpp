import ply.lex as lex
keywords = {
"alignas":"alignas", "alignof":"alignof", "anda":"anda", "and_eq":"and_eq", "asm":"asm", "auto":"auto", "bitand":"bitand",
"bitor":"bitor", "bool":"bool", "break":"break", "case":"case", "catch":"catch", "char":"char", "char16_t":"char16_t",
"char32_t":"char32_t", "class":"class", "compl":"compl", "const":"const", "constexpr":"constexpr", "const_cast":"const_cast",
"continue":"continue", "decltype":"decltype", "default":"default", "delete":"delete", "do":"do", "double":"double",
"dynamic_cast":"dynamic_cast", "else":"else", "enum":"enum", "explicit":"explicit", "export":"export", "extern":"extern",
"false":"false", "float":"float", "for":"for", "friend":"friend", "goto":"goto", "if":"if", "inline":"inline", "int":"int",
"long":"long", "mutable":"mutable", "namespace":"namespace", "new":"new", "noexcept":"noexcept", "not":"not", "not_eq":"not_eq",
"nullptr":"nullptr", "operator":"operator", "or":"or", "or_eq":"or_eq", "private":"private", "protected":"protected", "public":"public",
"register":"register", "reinterpret_cast":"reinterpret_cast", "return":"return", "short":"short", "signed":"signed", "sizeof":"sizeof",
"static":"static", "static_assert":"static_assert", "static_cast":"static_cast", "struct":"struct", "switch":"switch", 
"template":"template", "this":"this", "thread_local":"thread_local", "throw":"throw", "true":"true", "try":"try", "typedef":"typedef",
"typeid":"typeid", "typename":"typename", "union":"union", "unsigned":"unsigned", "using":"using", "virtual":"virtual",
"void":"void", "volatile":"volatile", "wchar_t":"wchar_t", "while":"while", "xor":"xor", "xor_eq":"xor_eq","size_t":"size_t",
"uint64_t":"uint64_t"
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
  if keywords.get(t.value) is not None:
    t.html = '<span class="bc_keyword">%s</span>'%t.value 
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
