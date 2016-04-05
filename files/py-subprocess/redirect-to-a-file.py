#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of running an external program and redirecting STDOUT/STDERR
to a file.

Shell equivalent:
    ls -l /etc >files.txt  2>errors.txt || echo ls failed
"""

from subprocess import check_call
try:
    fout = open('files.txt','w')
    ferr = open('errors.txt','w')
    check_call ("ls -l /etc/", shell=True, stdout=fout, stderr=ferr)
    fout.close()
    ferr.close()
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except CalledProcessError as e:
    sys.exit("'ls' failed, returned code %d (check 'errors.txt')" \
             % (e.returncode))
except OSError as e:
    sys.exit("failed to run shell: %s" % (str(e)))

