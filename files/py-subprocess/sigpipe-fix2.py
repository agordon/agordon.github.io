#!/usr/bin/env python2

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Resetting SIGPIPE back to default action (terminate process).

Solution suggested by:
http://www.chiark.greenend.org.uk/~cjwatson/blog/python-sigpipe.html
"""

#!/usr/bin/env python
import signal
from subprocess import check_output

def sigpipe_fix():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

x = check_output("seq 1 0.0001 99999999 | head -n1",
                 preexec_fn=sigpipe_fix,shell=True)
print "x = ", x
