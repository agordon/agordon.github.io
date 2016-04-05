#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of subprocess.check_output (with shell=False).
"""

from subprocess import check_output, CalledProcessError
from random import choice
import sys

try:
    cmd =   choice( ["seq", "seqXX" ] )
    param = choice( ["foo", "10" ] )
    numbers = check_output([cmd,param])
    print ("'%s %s' succeeded, result=%s" % (cmd,param,str(numbers)))
except CalledProcessError as e:
    sys.exit("'%s %s' failed, returned code %d" % (cmd,param,e.returncode))
except OSError as e:
    sys.exit("failed to execute program '%s': '%s'" % (cmd, str(e)))
