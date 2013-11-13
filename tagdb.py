'''
The db used to store the USR
'''
import sqlite3
class TagDb:
  db=''
  conn = None

  def __exe(self, sql):
    c = self.conn.cursor()
    c.execute(sql)
    c.close()
  def commit(self):
    self.conn.commit()

  def __fetch_one(self, sql):
    c = self.conn.cursor()
    c.execute(sql)
    for r in c:
      c.close()
      return list(r)
    c.close()
    return None
  def __fetch_all(self, sql):
    c = self.conn.cursor()
    c.execute(sql)
    rows = []
    for r in c:
      rows.append(list(r))
    return rows

  def __init__(self, db='usr.db'):
    self.db = db
    self.conn = sqlite3.connect(self.db)
    sql = 'create table if not exists tb_func_defs (usr text, src text, line integer, offset integer, tag text, is_definition integer)'
    self.__exe(sql)
    sql = 'create index if not exists index_func_defs on tb_func_defs(usr ASC)'
    self.__exe(sql)
    
    sql = 'create table if not exists tb_refs (usr text, src text, offset integer, tag text)'
    self.__exe(sql)
    sql = 'create index if not exists index_refs_usr on tb_refs(usr ASC)'
    self.__exe(sql)
    sql = 'create index if not exists index_refs_src on tb_refs(src,offset, tag)'
    self.__exe(sql)
    
    sql = 'create table if not exists tb_includes (src text, include text, offset integer)'
    self.__exe(sql)

  def add_func_def(self, usr, file_name, line, offset, tag, is_definition):
    sql = 'insert into tb_func_defs values ("%s","%s", %d, %d, "%s", %d)'%(usr, file_name, line,offset,tag, is_definition)
    self.__exe(sql)
  
  def add_ref(self, usr, file_name, offset, tag):
    sql = 'insert into tb_refs values ("%s","%s", %d, "%s")'%(usr, file_name, offset, tag)
    self.__exe(sql)
  
  def add_include(self, src, include, offset):
    sql = 'insert into tb_includes values ("%s","%s", %d)'%(src, include, offset)
    self.__exe(sql)

  def get_defs(self, f, line):
    sql = 'select * from tb_func_defs where src="%s" and line=%d'%(f, line)
    return self.__fetch_all(sql) 

  def get_ref(self, f, offset, tag):
    sql = 'select * from tb_refs where src="%s" and offset=%d and tag="%s"'%(f, offset, tag)
    row = self.__fetch_one(sql)
    #regular reference
    if row is not None:
      sql = 'select src from tb_func_defs where usr="%s"' % row[0]
      r = self.__fetch_one(sql)
      if r is not None:row[1] = r[0]
      return row
    #declare and implement reference
    else:
      sql = 'select * from tb_func_defs where src="%s" and offset=%d and tag="%s" and is_definition=0'%(f, offset, tag)
      row = self.__fetch_one(sql)
      if row is None:
        return None
      sql = 'select src from tb_func_defs where usr="%s" and is_definition=1' % row[0]
      r = self.__fetch_one(sql) 
      if r is None: return None
      row[1] = r[0]
      return row
  
  def get_include(self, src, offset):
    sql = 'select * from tb_includes where src = "%s" and offset=%d'%(src, offset)
    return self.__fetch_one(sql) 
  
  def is_processed(self, src):
    sql = 'select * from tb_includes where src="%s" or include="%s"'%(src, src)
    res = self.__fetch_one(sql)
    return res is not None

  def files(self):
    res = set()
    sql = 'select distinct(src) from tb_func_defs'
    rows = self.__fetch_all(sql)
    for r in rows:
      res.add(r[0])
    sql = 'select distinct(src) from tb_refs'
    rows = self.__fetch_all(sql)
    for r in rows:
      res.add(r[0])
    sql = 'select distinct(src) from tb_includes'
    rows = self.__fetch_all(sql)
    for r in rows:
      res.add(r[0])
    sql = 'select distinct(include) from tb_includes'
    rows = self.__fetch_all(sql)
    for r in rows:
      res.add(r[0])
    
    for f in res:
      yield f
    
  def clear(self):
    sql = 'delete from tb_refs'
    self.__exe(sql)
    sql = 'delete from tb_func_defs'
    self.__exe(sql)
  
  def close(self):
    self.conn.close()

  def dump(self):
    sql = 'select * from tb_refs'
    rows = self.__fetch_all(sql)
    print "tb_refs"
    for r in rows:
      print '[%s]' % ', '.join(map(str, r)) 
    sql = 'select * from tb_func_defs'
    rows = self.__fetch_all(sql)
    print "tb_func_defs"
    for r in rows:
      print '[%s]' % ', '.join(map(str, r)) 
    
    sql = 'select * from tb_includes'
    rows = self.__fetch_all(sql)
    print "tb_includes"
    for r in rows:
      print '[%s]' % ', '.join(map(str, r)) 
'''
db = TagDb()
db.dump()
for f in db.files():
  print f
db.close()
'''
