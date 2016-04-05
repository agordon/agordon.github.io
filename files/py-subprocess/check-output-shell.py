#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of subprocess.check_output (with shell=True).
"""

from subprocess import check_output, CalledProcessError
from random import choice
import sys
try:
    prog  = choice( ["seq", "seqXX" ] )
    param = choice( ["foo", "10" ] )

    # WARNING: constructing shell commands without input validation
    #          could lead to security issues!
    cmd = "%s %s" % (prog, param)
    numbers = check_output(cmd, shell=True)
    print ("command '%s' succeeded, returned: %s" % (cmd,str(numbers)))
except CalledProcessError as e:
    if e.returncode==127:
        sys.exit("program '%s' not found" % (prog))
    elif e.returncode<=125:
        sys.exit("'%s' failed, returned code %d" % (cmd,e.returncode))
    else:
        # Things get hairy and unportable - different shells return
        # different values for coredumps, signals, etc.
        sys.exit("'%s' likely crashed, shell retruned code %d" % (cmd,e.returncode))
except OSError as e:
    # unlikely, but still possible: the system failed to execute the shell
    # itself (out-of-memory, out-of-file-descriptors, and other extreme cases).
    sys.exit("failed to run shell: '%s'" % (str(e)))
