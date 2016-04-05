#!/usr/bin/env python3

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Resetting SIGPIPE back to default action (terminate process).

Solution suggested by:
http://www.chiark.greenend.org.uk/~cjwatson/blog/python-sigpipe.html

NOTE:
This solution requires Python3.
"""

#!/usr/bin/env python
import signal
from subprocess import check_output

x = check_output("seq 1 0.0001 99999999 | head -n1",
                 restore_signals=True,shell=True)
print ("x = ", x)

