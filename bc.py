#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from clang.cindex import *
from tagdb import TagDb
import ply.lex as lex
import lexer
from ref_visitor import RefVisitor
import sys

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

'''
The source files
Each one will be processed as a clang translation unit
srcs = [
'assoc.c',
'cache.c',
'daemon.c',
'hash.c',
'items.c',
'memcached.c',
'sasl_defs.c',
'sizes.c',
'slabs.c',
'solaris_priv.c',
'stats.c',
'testapp.c',
'thread.c',
'timedrun.c',
'util.c'
    ]
'''
'''
The arguments
the first 4 args are the system include path in my mac
you should get your real path with the command: "cpp -v"
args = [
   '-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/clang/5.0/include',
   '-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
   '-I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include',
   '-I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/System/Library/Frameworks',
   '-DHAVE_CONFIG_H',
   '-I.',
   '-DNDEBUG',
   '-I/usr/local/include'
    ]
'''
srcs = [
'global.c',
'ctime.c',
'status.c',
'date.c',
'os.c',
'fault.c',
'mem0.c',
'mem1.c',
'mem2.c',
'mem3.c',
'mem5.c',
'mutex.c',
'mutex_noop.c',
'mutex_unix.c',
'mutex_w32.c',
'malloc.c',
'printf.c',
'random.c',
'utf.c',
'util.c',
'hash.c',
'opcodes.c',
'os_unix.c',
'os_win.c',
'bitvec.c',
'pcache.c',
'pcache1.c',
'rowset.c',
'pager.c',
'wal.c',
'btmutex.c',
'btree.c',
'backup.c',
'vdbemem.c',
'vdbeaux.c',
'vdbeapi.c',
'vdbetrace.c',
'vdbe.c',
'vdbeblob.c',
'vdbesort.c',
'journal.c',
'memjournal.c',
'walker.c',
'resolve.c',
'expr.c',
'alter.c',
'analyze.c',
'attach.c',
'auth.c',
'build.c',
'callback.c',
'delete.c',
'func.c',
'fkey.c',
'insert.c',
'legacy.c',
'loadext.c',
'pragma.c',
'prepare.c',
'select.c',
'table.c',
'trigger.c',
'update.c',
'vacuum.c',
'vtab.c',
'where.c',
'parse.c',
'tokenize.c',
'complete.c',
'main.c',
'notify.c',
'fts3.c',
'fts3_aux.c',
'fts3_expr.c',
'fts3_hash.c',
'fts3_porter.c',
'fts3_tokenizer.c',
'fts3_tokenizer1.c',
'fts3_tokenize_vtab.c',
'fts3_write.c',
'fts3_snippet.c',
'fts3_unicode.c',
'fts3_unicode2.c',
'rtree.c',
'icu.c',
'fts3_icu.c'
    ]
args = [
    '-DSQLITE_OS_UNIX=1',
    '-I.',
    '-I./src',
    '-I./ext/rtree',
    '-D_HAVE_SQLITE_CONFIG_H',
    '-DBUILD_sqlite',
    '-DNDEBUG',
    '-DSQLITE_THREADSAFE=1',
    '-DSQLITE_OMIT_LOAD_EXTENSION=1',
    '-DSQLITE_TEMP_STORE=1'
    ]
def main():
  reload(sys)
  sys.setdefaultencoding('utf-8') 
  '''
  global args
  for f in srcs:
    index = Index.create()
    print f
    tu = index.parse(f, args)
    if not tu:
      print "cannot parse: %s"%f
    db = TagDb()
    v = RefVisitor(db) 
    v.run(tu)
    '''
  for f in db.files():
    if f == 'None':
      continue
    print f
    fd = open(f, 'r')
    code = fd.read()
    html = parse(f, code)
    html_file = wrapper_file_name(f) 
    wfd = open(html_file, 'w')
    wfd.write(html)
    wfd.close()
if __name__ == '__main__':
    main()
