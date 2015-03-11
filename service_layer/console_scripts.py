#!/usr/bin/env python

import sys
import os
from inspect import getmembers, isfunction
import pwd
from celery.__main__ import main

def _abate():
  if(os.getuid() == 0):
    pw = pwd.getpwnam('nobody')
    os.setgid(pw.pw_gid)
    os.setuid(pw.pw_uid)

def worker():
  _abate()
  # sudo -u nobody celery -A service_layer.tasks worker --loglevel=info
  sys.argv = ['', '-A', 'service_layer.tasks', 'worker', '--loglevel=info']
  sys.exit(main())

def beat():
  _abate()
  # sudo -u nobody celery -A service_layer.tasks worker -B --loglevel=info -s /tmp/celerybeat-schedule
  sys.argv = ['', '-A', 'service_layer.tasks', 'worker', '-B', '--loglevel=info', '-s', '/tmp/celerybeat-schedule']
  sys.exit(main())

def flower():
  _abate()
  # sudo -u nobody celery -A service_layer.tasks flower --loglevel=info
  sys.argv = ['', '-A', 'service_layer.tasks', 'flower', '--loglevel=info']
  sys.exit(main())

# This dictionary comprehension works but is just too ugly.
# {x[0]: x[1] for x in getmembers(sys.modules[__name__], isfunction) if x[0][0] != '_' and x[1].__module__ == __name__}
callable_functions = {}
if __name__ == '__console__':
  print "This does not work with bpython"
else:
  for func_tuple in getmembers(sys.modules[__name__], isfunction):
    if func_tuple[0][0] != '_': # name beginning with an underscore indicates private
      if func_tuple[1].__module__ == __name__: # make sure the function is coming from this module
        callable_functions.update({func_tuple[0]: func_tuple[1]})

if __name__ == '__main__':
  try:
    if sys.argv[1] in callable_functions.keys():
      sys.exit(callable_functions[sys.argv[1]]())
  except (IndexError,):
    pass
  print "Usage: {name} [{commands}]".format(name=__file__, commands='|'.join(callable_functions.keys()))
