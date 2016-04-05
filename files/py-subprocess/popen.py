#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of subprocess.Popen (with shell=False).
"""

from subprocess import Popen,PIPE
from random import choice
import sys
try:
    prog  = choice( ["seq", "seqXX" ] )
    param = choice( ["foo", "10" ] )

    p = Popen([prog,param],stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()

    if p.returncode == 0:
        print ("command '%s %s' succeeded, returned: %s" \
               % (prog, param, str(out)))
    else:
        print ("command '%s %s' failed, exit-code=%d error = %s" \
               % (prog, param, p.returncode, str(err)))
except OSError as e:
    sys.exit("failed to execute program '%s': %s" % (prog, str(e)))
