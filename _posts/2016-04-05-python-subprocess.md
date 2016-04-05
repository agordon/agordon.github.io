---
title: "Python Subprocess Module - Running external programs"
date: 2016-04-05
layout: post
---

# {{ page.title }}

Python's [subprocess](https://docs.python.org/2/library/subprocess.html) module
provides several methods of running external programs. It's easy to use,
but robust usage with proper error checking requires few more details.

## Content

* [method summary](#methods-summary)
* [shell parameter summary](#shell-parameter-summary)
* [Basic Usage](#basic-usage) - primary function calls
  * [check_call](#checkcall)
  * [check_output](#checkoutput)
  * [call](#call)
  * [Popen](#popen)
* [Error Checking](#error-checking)
  * [check_output error checking (without shell expansion)](#check_output_w_err)
  * [check_output error checking (with shell expansion)](#check_output_shell_w_err)
  * [Popen error checking (without shell)](#popen_w_err)
  * [Popen error checking (with shell)](#popen_shell_w_err)
* [Advanced Usage](#advanced-usage)
  * [Merging STDERR into STDOUT](#merging-stderr-into-stdout)
  * [Redirecting output to a file](#redirecting-output-to-a-file)
  * [Redirecting STDIN from a file](#redirecting-stdin-from-a-file)
  * [Redirecting BOTH STDIN and STDOUT](#redirecting-both-stdin-and-stdout)
  * [STDIN,STDOUT from/to a python variable](#stdinstdout-fromto-a-python-variable)
  * [Detecting error by STDERR](#detecting-error-by-stderr)
  * [Re-enabling SIGPIPE](#re-enabling-sigpipe)
* [things NOT to do](#things-not-to-do)
  * [using stdin.write / stdout.read](#using-stdinwrite--stdoutread)
  * [using PIPE with check_call/check_output/call](#using-pipe-with-checkcallcheckoutputcall)
  * [using Popen.wait() with PIPEs](#using-popenwait-with-pipes)
  * [Pass unvalidated input as a string with ‘shell=True’](#pass-unvalidated-input-as-a-string-with-shelltrue)


### methods summary

<div id="summary1" markdown="1">

|---
| Method | Returns | On errors | Recommended Use
|:-|:-|:-|:-
| `call` | exit code | returns non-zero exit code | programs which are expected to fail (or return non-zero code)
| `check_call` | exit code (always zero) | raises [CalledProcessError](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError) | programs which should not fail (failure is the exception, if you'll excuse the pun)
| `check_output` | program\'s output (stdout) | raises [CalledProcessError](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError) | programs which should not fail
| `Popen` | [Popen Object](https://docs.python.org/2/library/subprocess.html#popen-objects) | requires additional error handilng code | Fine-control of program's execution

</div>

###  shell parameter summary

<div id="summary1" markdown="1">

|---
|  | `shell=True` | `shell=False` (the default)
|:-|:-|:-
| cmd type | string:<br/>`"ls -l /etc/passwd"` | list:<br/>`["ls","-l","/etc/passwd"]`
| When program not found | returns non-zero exit code (usually 127). <br/> With `check_call`/`check_output` will raise [CalledProcessError](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError) | raise [OSError](https://docs.python.org/2/library/exceptions.html#exceptions.OSError)
| Advantages | Simple to use;<br/>Allows shell expansion (e.g. `ls /tmp/*.txt`, `$HOME`) <br/> and complex pipe commands (`seq 10 | rev | tac 2>/dev/null`)  | Safer,easier to use with problematic file names (e.g. with spaces or non-English characters);<br/>Avoids potential shell-related security issues;
| Disadvantages | potential security issues, see [here](https://docs.python.org/2/library/subprocess.html#frequently-used-arguments) | shell-functionality (redirection, pipes, globbing, env-vars) requires extra python code ;

</div>


## Basic Usage

*  The examples below show typical usage, with contrieved examples
   (there is rarely a real need to run `ls -l` from within python - better
   use [os.path](https://docs.python.org/2/library/os.path.html) module
   for such things)
*  The examples start with minimal error checking, then progress to complete
   code with proper error checking.

### check_call

Run the program (`ls`), STDOUT/STDERR shared with the script's
(e.g. will be printed to the terminal):


```python
from subprocess import check_call
check_call("ls -l /etc/passwd /dev/null",shell=True)
```

Similarly, without shell interpolation:

```python
from subprocess import check_call
check_call(["ls","-l","/etc/passwd","/dev/null"])
```

### check_output

Run the program (`seq`), STDOUT is returned as a variable:

```python
from subprocess import check_output
numbers = check_output("seq 10",shell=True)
```

### call

Run the program, get its exit code.
`grep` returns 0 if the regular-expression matched any lines,
1 if no lines matched, or other if an error occured.
Because a regular expression can contain characters with special shell-meaning,
it is better to run it with `shell=False` and avoid variable-expansion:

```python
from subprocess import call
rc = call(["grep","-Eq","(z|k|tc)sh","/etc/passwd"])
if rc == 0:
    print ("someone is using zsh/ksh/tcsh")
elif rc == 1:
    print ("zsh/ksh/tcsh not used")
else:
    print ("an error occured, grep returned %d" % rc)
```

If any error occurs, `grep` will print a message to STDERR, which will
be sent to the same STDERR of the script's (e.g. the screen) - the user
will see it.


### Popen

[Popen](https://docs.python.org/2/library/subprocess.html#subprocess.Popen) enables
fine-control over the external process - getting its STDOUT,STDERR and returned code.
In the example below `out` will contain the content of `/etc/passwd`,
and `err` will contain an error message about `/foo/bar` not being found.
The returned code will be 1:


```python
from subprocess import Popen,PIPE
p = Popen(["cat","/etc/passwd","/foo/bar"], stdout=PIPE,stderr=PIPE)
(out,err) = p.communicate();
print ("cat returned code = %d" % p.returncode)
print ("cat output:\n\n%s\n\n" % out)
print ("cat errors:\n\n%s\n\n" % err)
```



## Error Checking

### check_output error checking (without shell expansion)         {#check_output_w_err}

The `check_*` functions will raise [CalledProcessError](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError) if a program fails (runs, but returns non-zero exit code), or [OSError](https://docs.python.org/2/library/exceptions.html#exceptions.OSError) if the program was not found.
The following contrived example will randomly run `seq 10`, `seqXX 10`, `seq foo`, `seqXX foo` - thus generating different types of errors:

```python
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
```

( download [check-output.py](./files/py-subprocess/check-output.py) )

### check_output error checking (with shell expansion)         {#check_output_shell_w_err}

The `check_*` functions will raise [CalledProcessError](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError) if a program fails (it runs, but returns non-zero exit code), or if the program is not found (and the return-code will be 127). [OSError](https://docs.python.org/2/library/exceptions.html#exceptions.OSError) is unlikely but can still happen and should be accounted for.
The following contrived example will randomly run `seq 10`, `seqXX 10`, `seq foo`, `seqXX foo` - thus generating different types of errors:

```python
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
```

( download [check-output-shell.py](./files/py-subprocess/check-output-shell.py) )


### Popen  error checking (without shell)                        {#popen_w_err}

`Popen` (without shell) will run the program and return its STDOUT,STDERR and return code.
[OSError](https://docs.python.org/2/library/exceptions.html#exceptions.OSError) will be raised
if the program is not found.
The following contrived example will randomly run `seq 10`, `seqXX 10`, `seq foo`, `seqXX foo` - thus generating different types of errors:

```python
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
```

( download [popen.py](./files/py-subprocess/popen.py) )



### Popen error checking (with shell)                        {#popen_shell_w_err}

`Popen` (with shell) will run the program and return its STDOUT,STDERR and return code.
return code of 127 indicates the program was not found by the shell.
[OSError](https://docs.python.org/2/library/exceptions.html#exceptions.OSError) will be raised
on extreme cases where the system failed to run a new shell.
The following contrived example will randomly run `seq 10`, `seqXX 10`, `seq foo`, `seqXX foo` - thus generating different types of errors:

```python
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
```


( download [popen-shell.py](./files/py-subprocess/popen-shell.py) )

## Advanced Usage


### Merging STDERR into STDOUT

When using `check_output`, output is returned as a python variable
while STDERR is shared with the script's STDERR (e.g. printed to the
terminal).  By merging STDERR into STDOUT, the external program's
errors can be hidden from the user (while stil using the simple
`check_output` method).

This method is also useful if a program writes information other than
error messages to STDERR (e.g. progress information).

```python
from subprocess import check_output, CalledProcessError, STDOUT
try:
    numbers = check_output(["seq","foo", stderr=STDOUT)
except CalledProcessError as e:
    sys.exit("'seq foo'' failed, returned code %d" % e.returncode )
except OSError as e:
    sys.exit("failed to execute seq: %s" % (str(e)))
```

In the above example, the error message (content of STDERR) is lost.
The program's failure is detected by its non-zero exit-code (leading to
a 'CalledProcessError' exception.

There is little reason to use this method with `call`/`check_call`, since
these functions do not return the output in any form.
There is little reason to use this method with `Popen`, since it returns
the content of STDERR in a separate variable.

### Redirecting output to a file

Using a file object with `stdout` parameter will redirect the program's STDOUT
to a file:

```sh
# shell equivalent:
#   ls -l /etc > files.txt
```

```python
from subprocess import check_call
fout = open('files.txt','w');
check_call ("ls -l /etc/", shell=True, stdout=fout)
```

STDERR can be similarly redirected:

```sh
# shell equivalent:
#   ls -l /etc /foo/bar >files.txt 2>errors.txt
```

```python
from subprocess import check_call
fout = open('files.txt','w')
ferr = open('errors.txt','w')
check_call ("ls -l /etc/ /foo/bar", shell=True, stdout=fout, stderr=ferr)
```

For properly robust code, I/O errors must be checked as well:

```python
from subprocess import check_call
try:
    fout = open('files.txt','w')
    ferr = open('errors.txt','w')
    check_call ("ls -l /etc/", shell=True, stdout=fout, stderr=ferr)
    fout.close()
    ferr.close()
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except CalledProcessError as e:
    sys.exit("'ls' failed, returned code %d (check 'errors.txt')" \
             % (e.returncode))
except OSError as e:
    sys.exit("failed to run shell: %s" % (str(e)))
```

( download [redirect-to-a-file.py](./files/py-subprocess/redirect-to-a-file.py) )

### Redirecting STDIN from a file

The following contrived example runs `base64` with STDIN redirected from a file
(in real-world applications it is recommended to use python's built-in base64 module):

```sh
# shell equivalent:
#  b=$(base64 < /etc/passwd) || echo base64 failed
```

```python
from subprocess import check_output
import sys
try:
    fin=open('/etc/passwd','r')
    b=check_output(["base64"], stdin=fin)
    fin.close()
    print ("encoded passwd: %s" % str(b))
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except CalledProcessError as e:
    sys.exit("base64 failed: %s" % (str(e)))
except OSError as e:
    sys.exit("failed to run 'base64': %s" % (str(e)))
```


( download [redirect-stdin-from-file.py](./files/py-subprocess/redirect-stdin-from-file.py) )

### Redirecting BOTH STDIN and STDOUT

```sh
# Shell Equivalent:
#    base64 < /etc/passwd > encoded-passwd.txt \
#         || echo base64 failed
```

```python
from subprocess import check_call, CalledProcessError
try:
    fin=open('/etc/passwd','r')
    fout=open('encoded-passwd.txt','w')
    check_call(["base64"], stdin=fin, stdout=fout)
    fout.close()
    fin.close()
except IOError as e:
    sys.exit("I/O error on '%s': %s" % (e.filename, e.strerror))
except CalledProcessError as e:
    sys.exit("base64 failed: %s" % (str(e)))
except OSError as e:
    sys.exit("failed to run 'base64': %s" % (str(e)))
```

( download [redirect-stdin-stdout-to-files.py](./files/py-subprocess/redirect-stdin-stdout-to-files.py) )

### STDIN,STDOUT from/to a python variable

**NOTE**: when using this method, ensure the input is **small**. Sadly there
are not strict guidelines as to 'how small', the Python documentation says:
"Note The data read is buffered in memory, so do not use this method if the data
size is large or unlimited.". Few lines of text should be fine. To send large
amount of data, use file redirection or other methods. This issue is not
python-specific. For detailed discussion of pipes and subprocesses, see
[Advanced Programming in the Unix Environment, 3rd Ed.](http://www.apuebook.com/apue3e.html),
Chapter 15 ("Interprocess Communication") section 15.2 ("Pipes").

```sh
# shell (almost) equivalent:
#  out=$(printf "Hello World" | base64 2>err) || echo base64 failed
```

```python
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
```

( download [redirect-stdin-stdout-to-vars.py](./files/py-subprocess/redirect-stdin-stdout-to-vars.py) )

### Detecting error by STDERR

Most 'well-behaved' unix programs will terminte with exit code 0 upon success
and non-zero exit-code upon error. Shell syntax and python's
`check_call`/`check_output` operate under this assumption.

Some programs, however, exit with exit-code zero EVEN if there was an error,
and write error information to STDERR. Detecting errors for such programs
requires a bit more code.

The example below runs `openssl` with an *incorrect* option (`sha1X`).
openssl exits with code 0 even if wrong parameters are
given. Detection of errors is done by examining the content of the
returned STDERR string.

Shell Equivalent:

```sh
A=$(openssl sha1X < /etc/passwd 2>tmp.err) \
     || echo "openssl failed (should not happen)"
if test -s tmp.err ; then
     echo "Openssl failed, error = "
     cat tmp.err
     exit 1
fi
echo "OpenSSL succeeded, output = $A"
```

Python code:

```python
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
```


( download [detect-errors-by-stderr.py](./files/py-subprocess/detect-errors-by-stderr.py) )


### Re-enabling SIGPIPE

Python's subprocess module disables SIGPIPE by default (SIGPIPE is
sets to ignore). Most unix programs expect to run with SIGPIPE enabled.
When running a single external program (e.g. with `shell=False`) this is
usually not a problem. It does become a problem when running shell-pipes,
or when the executed program runs sub-programs on its own.

Example: the following shell command will print one line and terminate
immediately. This happens because when 'head' terminates, 'seq' will
receive a SIGPIPE signal, causing it to terminate without counting all
the way to 99999999:

```sh
seq 1 0.00001 99999999 | head -n1
```

Yet the following python code will run for a long time, because SIGPIPEs
are silenced by default:


    #!/usr/bin/env python
    from subprocess import check_output
    x = check_output("seq 1 0.0001 99999999 | head -n1",shell=True)


( download [sigpipe-issue.py](./files/py-subprocess/sigpipe-issue.py) )


> NOTE: future versions of GNU coreutils 'seq' will detect and address
> this issue regardless of python's SIGPIPE settings, but the problem
> will still exist for other programs.

The solution is to re-enable the default SIGPIPE behaviour.

Use the following method for Python2:

```python
#!/usr/bin/env python
import signal
from subprocess import check_output

def sigpipe_fix():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

x = check_output("seq 1 0.0001 99999999 | head -n1",
                 preexec_fn=sigpipe_fix,shell=True)
print "x = ", x
```

( download [sigpipe-fix2.py](./files/py-subprocess/sigpipe-fix2.py) )


Use the following method for Python3:

```python
#!/usr/bin/env python3
import signal
from subprocess import check_output
x = check_output("seq 1 0.0001 99999999 | head -n1",
                 restore_signals=True,shell=True)
print ("x = ", x)
```

( download [sigpipe-fix3.py](./files/py-subprocess/sigpipe-fix3.py) )


See further details and discussion:

<http://www.chiark.greenend.org.uk/~cjwatson/blog/python-sigpipe.html>,

<http://bugs.python.org/issue1652>,

<http://www.pixelbeat.org/programming/sigpipe_handling.html>.


## things NOT to do

Some techniques and methods should be avoided (despite being demonstrated
in various locations).

### using stdin.write / stdout.read

The [Popen object](https://docs.python.org/2/library/subprocess.html#popen-objects)
has `stdin`,`stdout`,`stderr` attributes. **DO NOT** use them. Quoting
from the manual:

> Warning Use communicate() rather than .stdin.write, .stdout.read or
> .stderr.read to avoid deadlocks due to any of the other OS pipe
> buffers filling up and blocking the child process.

Examples might look like so:

```python
## !! BAD EXAMPLE - DO NOT USE stdin.write/stdout.read !!
p = Popen([...], stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=False)
p.stdin.write("input to program")
result = p.stdout.readline()
p.wait()
p.kill()
```


### using PIPE with check_call/check_output/call

**DO NOT** set `stdout=PIPE` or `stderr=PIPE` in `check_call`/
`check_output`/`call` methods.

Only use `Popen` and `comminucate()` with the PIPE options.


### using Popen.wait() with PIPEs


**DO NOT** use the [Popen.wait()](https://docs.python.org/2/library/subprocess.html#subprocess.Popen.wait)
when using PIPEs for stdout/stderr - this might lead to a deadlock.
Use `Popen` and `comminucate()` instead.


### Pass unvalidated input as a string with 'shell=True'.

Do not pass unvalidated input (e.g. entered by the user or read from a
file) directly to a command-line string with `shell=True`.
This could lead to a security problem.
See [Subprocess FAQ](https://docs.python.org/2/library/subprocess.html#frequently-used-arguments)
for a detailed example.
