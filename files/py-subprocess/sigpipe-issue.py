#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of the problems caused by python's default behaviour
of setting SIGPIPE to 'ignore'.
The following shell command will run for a long time instead of terminating
after printing the first line.
"""

from subprocess import check_output
x = check_output("seq 1 0.0001 99999999 | head -n1",shell=True)
