---
title: Python Exception Handling Tips
date: 2015-08-14
layout: post
---

## {{ page.title }}

This post show contains recommendations for python exception handling in
user-facing programs (e.g. which exceptions to handle and how to report
them).

**TL;DR**

1. DO NOT raise or catch the generic `Exception`.
2. Use user-defined exceptions for application-level errors.

<sub>
Disclaimer: I'm not a python fan (and certainly not an expert).
Comments, feedback, suggestions and improvements are welcomed.
</sub>

## without catching exceptions

This typical python code:

    #!/usr/bin/env python
    import sys
    a = open("/non/existing/file","r")

Will result in this output:

    $ ./bad0.py
    Traceback (most recent call last):
      File "./bad0.py", line 3, in <module>
        a = open("/non/existing/file","r")
    IOError: [Errno 2] No such file or directory: '/non/existing/file'

This is *bad* output. Since the error is NOT a programming error, there is no need
to confuse the user with useless messages and source-code stack trace.

## Catch generic Exception

The simple (but wrong) option is to catch all exceptions:

    import sys
    try:
        a = open("/non/existing/file","r")
    except Exception as e:
        sys.exit("failed to open file: %s" % (str(e)))

Will print a better informative message:

    $ ./bad1.py
    failed to open file: [Errno 2] No such file or directory: '/non/existing/file'

Now a different program. This time, it's a programming error (missing second
value for the '%s'):

    import sys
    try:
        filename = "hello"
        extension = "txt"
        path="/non/existging/%s.%s" % ( filename )
        a = open(path,'r')
    except Exception as e:
        sys.exit("failed to open file: %s" % (str(e)))

But since we're catching *all* exceptions, the error will be shown like so:

    $ ./bad2.py
    failed to open file: not enough arguments for format string

This is *extremely* unhelpful, both to the user, and more so to the programmer.
For programming errors, we actually *want* to see the full traceback.

A third example: an input error - a file containing an unexpected value.
This is partially a programming error: the code is not robust enough
to handle invalid input. But the default error is not helpful to anyone
(not the user and not the programmer):

    #!/usr/bin/env python
    import sys
    
    try:
        # Get the username of the first user (usually 'root')
        a = open("/etc/passwd","r").readline().split(":")[0]
        # Converting string to int - will raise ValueError exception
        b = int(a)
    except Exception as e:
        sys.exit("failed to open file: %s" % (str(e)))

Will result in this output:

    $ ./bad3.py
    failed to open file: invalid literal for int() with base 10: 'root'

This output doesn't help the user to know what's wrong,
or the programmer to know where it went wrong and why.

## Generic Exceptions in Large Programs

In a large program/script, there will be a mixture of these errors (especially
programming errors during development/debugging). Catching them generically
will make it hard for the programmer to debug what's wrong.
Imagine the following code (using randomness to simulate the complexity of
the script - so we can't tell in advance which error will happen):

    #!/usr/bin/env python
    import sys, random
    
    def generate_runtime_error():
        # Raise I/O error
        a = open("/non/existing/file","r")
    
    def generate_value_error():
        a = open("/etc/passwd","r")
        # Get the username of the first user (usually 'root')
        b = a.readline().split(":")[0]
        # Convert to a number - this will fail with ValueError exception
        c = int(b)
    
    def generate_attribute_error():
        a = open("/etc/passwd","r")
        # Programming error: 'a' doesn't have function 'readdline'
        # (type with two 'd')
        # will raise AttributeError
        b = a.readdline().split(":")[0]
        c = int(b)
    
    def generate_type_error():
        # Invalid Python code, will raise TypeError exception
        a = "hello"
        b = "%s %s %s " % ( a )
    
    try:
        r = random.randint(1,4)
        if r==1:
            generate_runtime_error()
        elif r==2:
            generate_value_error()
        elif r==3:
            generate_attribute_error()
        else:
            generate_type_error()
    except Exception as e:
        sys.exit("program failed: %s" % ( str(e) ) )
    

Running this multiple times will give the various errors:

        $ ./bad4.py
        program failed: [Errno 2] No such file or directory: '/non/existing/file'
        $ ./bad4.py
        program failed: invalid literal for int() with base 10: 'root'
        $ ./bad4.py
        program failed: not enough arguments for format string
        $ ./bad4.py
        program failed: 'file' object has no attribute 'readdline'

1. The first error is informative: it's a user/runtime error.
2. The second error is a runtime error (user/input error), but not informative
   for troubleshooting.
3. The third and fourth errors are programming errors - literally bugs
   in the source code - but not helpful at all for debugging.


## Catching Exceptions by type

Instead of catching all exceptions, it's better to catch only
specific exceptions: `IOError` indicates I/O errors (obviously...),
`ValueError` indicates conversion errors (and other issues).
In the right context, they indicate user-facing errors, not programming errors.
It is expected that a script will encounter those when a user misuses the
program. We want to catch them, and print a friendly,informative message,
with no stacktrace.

`AttributeError` and `TypeError` are bugs/programming errors - we don't want
to catch them at all - when they happen (if if they happen to a user), they
indicate bugs, and we want to show a full stacktrace (hopefully the user will
copy&paste the stacktrace and sent it to the developer).

Here's an improved version:

    #!/usr/bin/env python
    import sys, random
    
    def generate_runtime_error():
        # Raise I/O error
        a = open("/non/existing/file","r")
    
    def generate_value_error():
        a = open("/etc/passwd","r")
        # Get the username of the first user (usually 'root')
        b = a.readline().split(":")[0]
        # Convert to a number - this will fail with ValueError exception
        c = int(b)
    
    def generate_attribute_error():
        a = open("/etc/passwd","r")
        # Programming error: 'a' doesn't have function 'readdline'
        # (type with two 'd')
        # will raise AttributeError
        b = a.readdline().split(":")[0]
        c = int(b)
    
    def generate_type_error():
        # Invalid Python code, will raise TypeError exception
        a = "hello"
        b = "%s %s %s " % ( a )
    
    try:
        r = random.randint(1,4)
        if r==1:
            generate_runtime_error()
        elif r==2:
            generate_value_error()
        elif r==3:
            generate_attribute_error()
        else:
            generate_type_error()
    except IOError as e:
        sys.exit("program failed: Input/Output error: %s" % ( str(e) ) )
    except ValueError as e:
        sys.exit("program failed: Input/Output: %s" % ( str(e) ) )

With this version, user-errors will be succint:

    $ ./better1.py
    program failed: Input/Output: invalid literal for int() with base 10: 'root'
    $ ./better1.py
    program failed: Input/Output error: [Errno 2] No such file or directory: '/non/existing/file'

And programming errors will be informative:

    $ ./better1.py
    Traceback (most recent call last):
      File "./better1.py", line 35, in <module>
        generate_attribute_error()
      File "./better1.py", line 20, in generate_attribute_error
        b = a.readdline().split(":")[0]
    AttributeError: 'file' object has no attribute 'readdline'

    $ ./better1.py
    Traceback (most recent call last):
      File "./better1.py", line 37, in <module>
        generate_type_error()
      File "./better1.py", line 26, in generate_type_error
        b = "%s %s %s " % ( a )
    TypeError: not enough arguments for format string

## Catching exceptions as close to origin as possible

Catching an error in the 'main' section might miss some information
(e.g. "ValueError" could originate from many different places in the code
from many different inputs).
It might be considered better to catch the error as close as possible
to the source (but - only user/runtime errors, not programming errors):

This versions catches application-level (user/runtime) exceptions as close as
possible to the source, and terminates immediate using `sys.exit`.
Other exceptions will be shown with a full stacktrace:

    #!/usr/bin/env python
    import sys, random

    def generate_runtime_error():
        # Raise I/O error
        try:
            a = open("/non/existing/file","r")
        except IOError as e:
            sys.exit("program failed: Input/Output error: %s" % ( str(e) ) )

    def generate_value_error():
        filename = "/etc/passwd"
        try:
            a = open(filename,"r")
            # Get the username of the first user (usually 'root')
            b = a.readline().split(":")[0]
            # Convert to a number - this will fail with ValueError exception
            c = int(b)
        except IOError as e:
            sys.exit("program failed: Input/Output error: %s" % ( str(e) ) )
        except ValueError as e:
            sys.exit("program failed: input error in '%s': " \
                     "expecting numeric value, but found '%s'" % \
                     ( filename, b ))

    def generate_attribute_error():
        a = open("/etc/passwd","r")
        # Programming error: 'a' doesn't have function 'readdline'
        # (type with two 'd')
        # will raise AttributeError
        b = a.readdline().split(":")[0]
        c = int(b)


    def generate_type_error():
        # Invalid Python code, will raise TypeError exception
        a = "hello"
        b = "%s %s %s " % ( a )


    r = random.randint(1,4)
    if r==1:
        generate_runtime_error()
    elif r==2:
        generate_value_error()
    elif r==3:
        generate_attribute_error()
    else:
        generate_type_error()


## Using Specialized exception class

Terminating with `sys.exit` might be considered *bad form* in python:
exceptions are the proper way to generate/handle errors.
To differentiate **application-level** exceptions from other python
exceptions, we create a specialized class, which inherits from python's
`Exception` class. Throw it when there is an application-level error,
and catch it in the main code.
This will also be more modular, if we ever want to covnert this code into a
python module (a python module should never call `sys.exit`).

    #!/usr/bin/env python
    import sys, random

    class MyException(Exception):
        """ My Class for user-facing (non-programming) errors """
        pass

    def generate_runtime_error():
        # Raise I/O error
        try:
            a = open("/non/existing/file","r")
        except IOError as e:
            err = "Input/Output error: %s" % ( str(e) )
            raise MyException(err)

    def generate_value_error():
        filename = "/etc/passwd"
        try:
            a = open(filename,"r")
            # Get the username of the first user (usually 'root')
            b = a.readline().split(":")[0]
            # Convert to a number - this will fail with ValueError exception
            c = int(b)
        except IOError as e:
            err = "Input/Output error: %s" % ( str(e) )
            raise MyException(err)
        except ValueError as e:
            err = "input validation error in '%s': " \
                     "expecting numeric value, but found '%s'" % \
                     ( filename, b )
            raise MyException(err)

    def generate_attribute_error():
        a = open("/etc/passwd","r")
        # Programming error: 'a' doesn't have function 'readdline'
        # (type with two 'd')
        # will raise AttributeError
        b = a.readdline().split(":")[0]
        c = int(b)


    def generate_type_error():
        # Invalid Python code, will raise TypeError exception
        a = "hello"
        b = "%s %s %s " % ( a )


    try:
        r = random.randint(1,4)
        if r==1:
            generate_runtime_error()
        elif r==2:
            generate_value_error()
        elif r==3:
            generate_attribute_error()
        else:
            generate_type_error()
    except MyException as e:
        # Centralized place for termination-cleanup
        sys.exit("program failed: " + str(e))

## Custom Exceptions

More information: <https://docs.python.org/2/tutorial/errors.html>

The canonical syntax for [User-defined Exceptions](https://docs.python.org/2/tutorial/errors.html#user-defined-exceptions):

    class Error(Exception):
        """Base class for exceptions in this module."""
        pass

## Printing the type of a generic exception

At times you must catch all exceptions (or perhaps use someone else's code),
and can't pass them forward with `raise. To determine the type of the
exception (to improve the code with a specialized catch), use the following:

    try:
        # Code that might raise exception
        foo.bar()
    except Exception as e:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print message
     
