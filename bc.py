#!/usr/bin/env python

from clang.cindex import *
from pprint import pprint
from optparse import OptionParser, OptionGroup
from tagdb import TagDb
import ply.lex as lex
import lexer

html_header = '''
<!DOCTYPE html>
<html>
<head>
  <title>Beauty Cpp</title>
  <script type="text/javascript" src="/js/jquery.min.js"></script>
  <link rel="stylesheet" type="text/css" href="/css/main.css">
</head>
<body class="question-page">
'''

html_footer = '''
</body>
'''

db = TagDb()

def wrapper_file_name(f):
  return "data/"+f.replace('/', '_').replace('.', '_')+".html"

def wrapper_def(f, lineno):
  defines = db.get_defs(f, lineno)
  if len(defines) == 0:
    return lineno
  define = defines[0]
  html = '<span id="%s">%d</span>'%(define[0], lineno)
  for define in defines[1:]:
    html += '<span id="%s"></span>'%(define[0])
  return html

def wrapper_ref(f, offset, tag):
  ref = db.get_ref(f, offset, tag)
  if ref is not None:
    html_file = wrapper_file_name(ref[1])
    html = '<a href="../%s#%s">%s</a>'%(html_file, ref[0], tag)
  else:
    html = tag
  return html

def wrapper_include(f, inc_tag):
  inc = db.get_include(f, inc_tag.lexpos)
  
  if inc is None:
    if inc_tag.inc_type == '<':
      return '#include &lt;%s&gt;'%(inc_tag.inc)
    else:
      return '#include "%s"'%(inc_tag.inc)

  html_file = wrapper_file_name(inc[1])
  if inc_tag.inc_type == '<':
    html = '#include &lt;<a href="../%s">%s</a>&gt;'%(html_file, inc_tag.inc)
  else:
    html = '#include "<a href="../%s">%s</a>"'%(html_file, inc_tag.inc)
  return html

def parse(f, code):
  l = lex.lex(module=lexer)
  l.input(code)
  html = html_header + '<table><tr><td>%s</td><td>'%wrapper_def(f, 1)
  
  while True:
    t = l.token()
    if t is None: 
      break
    elif t.type == '<':
      html += '&lt;'
    elif t.type == '>':
      html += '&gt;'
    elif t.type == 'NEWLINE':
      html += '</td></tr>\n<tr><td class="bc_lineno">%s</td><td>'%wrapper_def(f,t.lineno+1)
    elif t.type == 'INCLUDE':
      html += wrapper_include(f, t)
    elif t.type == 'ID':
      html += wrapper_ref(f, t.lexpos, t.value)
    elif hasattr(t, 'html'):
      if type(t.html) is list:
        comment_line = t.lineno
        for h in t.html:
          html += h
          comment_line+=1
          html += '</td></tr><tr><td>%d</td><td>'%comment_line
      else:
        html += t.html
    else:
      html += t.value

  html += '</td></tr>' + html_footer
  return html



def main():
  for f in db.files():
    if f == 'None':
      continue
    fd = open(f, 'r')
    code = fd.read()
    html = parse(f, code)
    html_file = wrapper_file_name(f) 
    wfd = open(html_file, 'w')
    wfd.write(html)
    wfd.close()
if __name__ == '__main__':

    main()
