#!/usr/bin/python2.7
import gevent.monkey
gevent.monkey.patch_all()
from gevent import wsgi, pool
import os, webserver

conn_pool = pool.Pool(1000)
port = os.getenv("PORT", 80)
wsgi.WSGIServer(('',int(port)), webserver.app, spawn=conn_pool).serve_forever()

