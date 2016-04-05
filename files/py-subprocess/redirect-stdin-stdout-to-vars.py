#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of running an external program and redirecting STDIN from a python
variable and STDOUT to a python variable.

shell (almost) equivalent:
  out=$(printf "Hello World" | base64 2>err) || echo base64 failed

"""

import sys
from subprocess import Popen,PIPE

try:
    p = Popen(["base64"], stdin=PIPE, stdout=PIPE,stderr=PIPE)

    input = "Hello World"
    (out,err) = p.communicate(input)

    if p.returncode==0:
        print ("encoded value = %s" % (str(out)))
    else:
        print ("failed to encode, exit-code=%d, error=%s" % (p.returncode,str(err)))
except OSError as e:
    sys.exit("failed to run 'base64': %s" % (str(e)))
