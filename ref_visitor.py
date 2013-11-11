from clang.cindex import Index
from clang.cindex import Cursor
from clang.cindex import CursorKind
from optparse import OptionParser, OptionGroup
from tagdb import TagDb

class RefVisitor:
  tagdb = None
  tu = None 
  def __init__(self, tagdb):
    self.tagdb = tagdb
  
  def __visit(self, node):
    if node.kind is CursorKind.CALL_EXPR:
      self.__visit_call(node)
    elif node.kind is CursorKind.FUNCTION_DECL:
      self.__visit_function_decl(node)
    elif node.kind is CursorKind.STRUCT_DECL:
      self.__visit_class_decl(node)
    elif node.kind is CursorKind.ENUM_DECL:
      self.__visit_class_decl(node)
    elif node.kind is CursorKind.UNION_DECL:
      self.__visit_class_decl(node)
    elif node.kind is CursorKind.TYPEDEF_DECL:
      self.__visit_class_decl(node)
    elif node.kind is CursorKind.TYPE_REF:
      self.__visit_decl_ref(node)

  def __visit_call(self, node):
    for n in node.get_children():
      if n.kind is not CursorKind.UNEXPOSED_EXPR:
        return
      for d in n.get_children():
        self.__visit_decl_ref(d)
        break;
    
  def __visit_function_decl(self, node):
    f = node.location.file
    l = node.location.line
    if self.tagdb.is_processed(node.location.file):
      return
    self.tagdb.add_func_def(node.get_usr(), f, l,node.location.offset, node.spelling, node.is_definition())
   
  def __visit_class_decl(self, node):
    f = node.location.file
    l = node.location.line
    if self.tagdb.is_processed(node.location.file):
      return
    self.tagdb.add_func_def(node.get_usr(), f, l,node.location.offset, node.spelling, node.is_definition())
  
  def __visit_decl_ref(self, node):
    ref = node.referenced
    if ref is None:
      return
    f = node.location.file
    offset = node.location.offset
    if ref.get_usr() == "" or ref.kind is CursorKind.PARM_DECL:
      return False
    self.tagdb.add_ref(ref.get_usr(), f, offset, ref.spelling)
    return False
   
  def run(self, tu):
    self.tu = tu
    self.__recusive_visit(self.tu.cursor)
    for f in self.tu.get_includes():
      self.tagdb.add_include(f.source, f.include, f.location.offset)

  def __recusive_visit(self, node):
    if self.__visit(node) is False:
      return
    for c in node.get_children():
      self.__recusive_visit(c)

def main():
  global opts
  parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")
  parser.disable_interspersed_args()
  (opts, args) = parser.parse_args()

  if len(args) == 0:
      parser.error('invalid number arguments')

  index = Index.create()
  args.append('-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/clang/5.0/include')
  args.append('-I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include')
  args.append('-I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include')
  args.append('-I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/System/Library/Frameworks')
  args.append('-DHAVE_CONFIG_H')
  args.append('-I.')
  args.append('-DNDEBUG')
  args.append('-I/usr/local/include')
  tu = index.parse(None, args)
  if not tu:
    parser.error("unable to load input")
  db = TagDb()
  v = RefVisitor(db) 
  v.run(tu)
  db.dump()

if __name__ == '__main__':
    main()
