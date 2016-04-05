#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of running an external program and redirecting STDIN from a file
and STDOUT to a file.

Shell equivalent:
    base64 < /etc/passwd > encoded-passwd.txt \
         || echo base64 failed
"""

from subprocess import check_call, CalledProcessError
try:
    fin=open('/etc/passwd','r')
    fout=open('encoded-passwd.txt','w')
    check_call(["base64"], stdin=fin, stdout=fout)
    fout.close()
    fin.close()
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except CalledProcessError as e:
    sys.exit("base64 failed: %s" % (str(e)))
except OSError as e:
    sys.exit("failed to run 'base64': %s" % (str(e)))
