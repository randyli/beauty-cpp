#!/usr/bin/python
# -*- coding:utf-8 -*-
import cgi
print "Content-Type: text/html\n\n"

projects = [
	('/memcached/', 'memcached')
]

form = cgi.FieldStorage()

directory = ''
if form.has_key('dir'):
	directory = form['dir'].value 

if directory == '/':
  print '<ul class="jqueryFileTree" style="display: none;">',
  print '<li class="directory collapsed"><a href="#" rel="/memcached/">memcached</a></li>'
  print '</ul>'

elif directory == '/memcached/':
  print '<ul class="jqueryFileTree" style="display: none;">',
  print '<li class="file ext_h"><a href="/data/__assoc_h.html" rel="/memcached/__assoc_h.html" target="content">assoc.h</a></li>'
  print '<li class="file ext_c"><a href="/data/assoc_c.html" rel="/memcached/assoc_c.html" target="content">assoc.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__cache_h.html" rel="/memcached/__cache_h.html" target="content">cache.h</a></li>'
  print '<li class="file ext_c"><a href="/data/cache_c.html" rel="/memcached/cache_c.html" target="content">cache.c</a></li>'
  print '<li class="file ext_c"><a href="/data/daemon_c.html" rel="/memcached/daemon_c.html" target="content">daemon.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__hash_h.html" rel="/memcached/__hash_h.html" target="content">hash.h</a></li>'
  print '<li class="file ext_c"><a href="/data/hash_c.html" rel="/memcached/hash_c.html" target="content">hash.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__items_h.html" rel="/memcached/__items_h.html" target="content">items.h</a></li>'
  print '<li class="file ext_c"><a href="/data/items_c.html" rel="/memcached/items_c.html" target="content">items.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__memcached_h.html" rel="/memcached/__memcached_h.html" target="content">memcached.h</a></li>'
  print '<li class="file ext_c"><a href="/data/memcached_c.html" rel="/memcached/memcached_c.html" target="content">memcached.c</a></li>'
  print '<li class="file ext_c"><a href="/data/sasl_defs_c.html" rel="/memcached/sasl_defs_c.html" target="content">sasl_defs.c</a></li>'
  print '<li class="file ext_c"><a href="/data/sizes_c.html" rel="/memcached/sizes_c.html" target="content">sizes.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__slabs_h.html" rel="/memcached/__slabs_h.html" target="content">slabs.h</a></li>'
  print '<li class="file ext_c"><a href="/data/slabs_c.html" rel="/memcached/slabs_c.html" target="content">slabs.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__stats_c.html" rel="/memcached/__stats_h.html" target="content">stats.h</a></li>'
  print '<li class="file ext_c"><a href="/data/stats_c.html" rel="/memcached/stats_c.html" target="content">stats.c</a></li>'
  print '<li class="file ext_c"><a href="/data/thread_c.html" rel="/memcached/thread_c.html" target="content">thread.c</a></li>'
  print '<li class="file ext_c"><a href="/data/timed_c.html" rel="/memcached/timedrun_c.html" target="content">timedrun.c</a></li>'
  print '<li class="file ext_h"><a href="/data/__util_c.html" rel="/memcached/__util_h.html" target="content">util.h</a></li>'
  print '<li class="file ext_c"><a href="/data/utile_c.html" rel="/memcached/util_c.html" target="content">util.c</a></li>'
  print '</ul>'
