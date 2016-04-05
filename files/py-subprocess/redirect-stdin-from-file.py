#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of running an external program and redirecting STDIN from a file.


Shell equivalent:
  b=$(base64 < /etc/passwd) || echo base64 failed
"""

from subprocess import check_output
import sys
try:
    fin=open('/etc/passwd','r')
    b=check_output(["base64"], stdin=fin)
    fin.close()
    print ("encoded passwd: %s" % str(b))
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except CalledProcessError as e:
    sys.exit("base64 failed: %s" % (str(e)))
except OSError as e:
    sys.exit("failed to run 'base64': %s" % (str(e)))
