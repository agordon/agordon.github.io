#!/usr/bin/env python

"""
Python-Subprocess tutorial
Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>
License: MIT

See: http://crashcourse.housegordon.org/python-subprocess.html

Example of detecting errors by examining the content of STDERR
(instead of relying on the program's exit code).
Needed for some programs which do not properly set non-zero exit code
upon failure.

NOTE: 'openssl sha1X' is incorrect usage, yet openssl will exit with code 0.

Shell Equivalent:

    A=$(openssl sha1X < /etc/passwd 2>tmp.err) \
         || echo "openssl failed (should not happen)"
    if test -s tmp.err ; then
         echo "Openssl failed, error = "
         cat tmp.err
         exit 1
    fi
    echo "OpenSSL succeeded, output = $A"


"""

import sys
from subprocess import Popen, PIPE
try:
    fin=open('/etc/passwd','r')

    p = Popen(["openssl","sha1X"], stdin=fin, stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate();
    fin.close()

    if p.returncode!=0:
        ## NOTE: This will never happen (in this example), as openssl
        ##       does not return non-zero on errors.
        ##       We'll have to detect errors in a different way.
        sys.exit("openssl failed, exit code=%d, error=%s" \
                 % (p.returncode, str(err)))

    # OpenSSL will write errors messages to STDERR. If it's not empty,
    # there was an error.
    err = err.strip();
    if len(err) != 0:
        sys.exit("openssl failed, error = %s" % (str(err)))

    out = out.strip();
    print ("OpenSSL succeeded, output = %s" % (str(out)))
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except OSError as e:
    sys.exit("failed to execute command 'base64': %s" % (str(e)))
