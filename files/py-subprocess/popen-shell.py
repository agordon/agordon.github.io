#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of subprocess.Popen (with shell=True).
"""

from subprocess import Popen,PIPE
from random import choice
import sys
try:
    prog  = choice( ["seq", "seqXX" ] )
    param = choice( ["foo", "10" ] )
    # WARNING: constructing shell commands without input validation
    #          could lead to security issues!
    cmd = "%s %s" % (prog, param)

    p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()

    if p.returncode == 0:
        print ("command '%s %s' succeeded, returned: %s" \
               % (prog, param, str(out)))
    elif p.returncode <= 125:
        print ("command '%s %s' failed, exit-code=%d error = %s" \
               % (prog, param, p.returncode, str(err)))
    elif p.returncode == 127:
        print ("program '%s' not found: %s" % (prog, str(err)))
    else:
        # Things get hairy and unportable - different shells return
        # different values for coredumps, signals, etc.
        sys.exit("'%s' likely crashed, shell retruned code %d" % (cmd,e.returncode))
except OSError as e:
    # unlikely, but still possible: the system failed to execute the shell
    # itself (out-of-memory, out-of-file-descriptors, and other extreme cases).
    sys.exit("failed to run shell: '%s'" % (str(e)))
