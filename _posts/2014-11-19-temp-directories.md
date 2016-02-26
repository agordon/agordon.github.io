---
title: "Using Temporary Directories"
layout: post
date:   2014-11-19
---

# {{ page.title }}

This post (originally: a long email) was written in response to a friend's
email about running out of space on the shared server's `/tmp/` directory.

## TL;DR

1. Create a temporary directory with your prefix (e.g. `lobstr`), in the
   system's TMP directory:

        $ mktemp -d -t lobstr.XXXXXX
        /tmp/lobstr.je4Gax

2. Put all of your program's temporary files inside that directory.

3. Delete the directory when the program exits.

## Simple Usage (unix shell)

Create a temporary file, in the default TMP directory:

    $ mktemp
    /tmp/tmp.47i2SIE2lj

The created file is owned by the user, and is set to disallow access from
other users:

    $ ls -l /tmp/tmp.47i2SIE2lj
    -rw------- 1 gordon gordon     0 Nov 18 11:45 tmp.47i2SIE2lj

Create a temporary directory, in the default TMP directory:

    $ mktemp -d
    /tmp/tmp.6BvgfZqKrk
    $ ls -dl /tmp/tmp.6BvgfZqKrk
    drwx------ 2 gordon gordon 4096 Nov 18 11:51 /tmp/tmp.6BvgfZqKrk

Create a temporary file, with your program's prefix (e.g. `lobstr`):

    $ mktemp lobstr.XXXXXX
    lobstr.sdaTH9

At least six `X` must be specified, and they will be replaced by random letters.
Notice that the file was created in the *current* directory (not in `/tmp`).

You might be tempted to specify a full path with your prefix:

    $ mktemp /tmp/lobstr.XXXXXX   ### BAD EXAMPLE - DO NOT USE
    /tmp/lobstr.jLB4eX

But that is *wrong*. It assumes that `/tmp` is the always the TMP directory,
which is not the case. Instead, use the following:

    # Create a temporary file:
    $ mktemp -t lobstr.XXXXXX    #### Good Example
    /tmp/lobstr.k8h6g0p

The result looks the same, but using `-t` tells `mktemp` to use the system's
temporary directory (more examples, below).

To create a temporary directory, with a your prefix, in the system's TMP directory,
combine `-d` and `-t`. For portability on Mac OS X, the `-d` must be first:

    # Create a temporary directory:
    $ mktemp -d -t lobstr.XXXXXX
    /tmp/lobstr.eiDFtC

## Why not hard-code `/tmp/` for temporary files

On the most common unix systems, for your 'common' usage, there is a directory
named `/tmp`, which is supposed to contain temporary files.

BUT,  
There are many cases where you (or the system-administrator) wants to store
temporary files else where.

Examples:

1. On our server `club.wi.mit.edu`, `/tmp/` is on the root disk, which is
   very small (less than 1.1GB free space left).
2. On Cluster computer systems (e.g. TAK), and other systems using
   SGE/LFS/Torque/etc, when you submit a new job, and it starts running on a
   node, each user gets his/her own temporary directory - it is not `/tmp`.
3. On Windows (which we don't care about, but still...) - the temporary
   directory is obviously not `/tmp/` .
4. For faster performance, it is sometimes better to use a temporary directory
   on a specific disk, or even completely in memory.
5. On Amazon EC2, it is sometimes better to use the local-instance storage disk
   as temporary directory - which has lots of storage and relatively fast I/O.
6. On some systems, `/tmp` is using a in-memory-disk - which is very fast,
   but tends to be small. Using a different (disk-based) temporary directory
   can help store large temporary files.
7. Hard-coded paths are evil.


## Changing the temporary directory

When properly using `mktemp` (and the appropriate modules in Perl/Python/C,
see below), the location of the TMP directory can be set using the `TMPDIR`
environment variable:

    # Set the location of the TMP directory
    # (e.g. in "~/.bashrc")
    $ export TMPDIR=/data/gordon/tmp

    # Create a temporary file in the new temp directory
    $ mktemp -t lobstr.XXXXXX
    /data/gordon/tmp/lobstr.vzmfDd

By setting `TMPDIR` in your `.bashrc` file, or manually before running a command,
you can change the location of the temporary files - to a directory with more
storage space or faster disks.

## Shell examples

Create one temporary directory, then all file names can be fixed:
there would no collisions if the same script is run multiple times in parallel
as each temp directory is unique.

    #!/bin/sh

    DIR=$(mktemp -d -t myproject.XXXXXX) || exit 1
    echo "tmpdir = $DIR"
    echo "filename = $DIR/step1.txt"

    # Do one thing
    my-program > "$DIR/step1.txt" || exit 1

    # Do another thing
    sort "$DIR/step1.txt" > "$DIR/step2.txt" || exit 1

    # When the script is completed, delete the temp directory
    # (or keep it for debugging/troubleshooting)
    rm -r "$DIR"


Using the script:

    # default tmp directory
    $ sh example.sh
    tmpdir = /tmp/myproject.L3BxdI
    filename = /tmp/myproject.L3BxdI/step1.txt

    # Custom tmp directory
    $ export TMPDIR=/data/gordon/tmp/
    $ sh example.sh
    tmpdir = /data/gordon/myproject.K4Pijh
    filename = /data/gordon/myproject.K4Pijh/step1.txt

# Python

Use the `tempfile` module to create a temporary directory:


    import tempfile,os

    # Create a temporary directory
    tmpdir = tempfile.mkdtemp(prefix='lobstr.')

    # Write files in that directory
    filename = os.path.join(tmpdir,'step1.txt')

    print "tmpdir = ", tmpdir
    print "filename = ", filename

Using the script:

    ## default tmp directory
    $ python example.py
    tmpdir =  /tmp/lobstr.yuHqQV
    filename =  /tmp/lobstr.yuHqQV/step1.txt

    ## Custom tmp directory
    $ export TMPDIR=/data/gordon/tmp/
    $ python example.py
    tmpdir =  /data/gordon/tmp/lobstr.4MzWUG
    filename =  /data/gordon/tmp/lobstr.4MzWUG/step1.txt


## Perl

Use `File::Temp` module to create temporary directories:


    use File::Temp qw/tempdir/;
    use File::Spec::Functions;

    # Create a temporary directory
    $tmpdir = tempdir ( 'lobstr.XXXXXX', TMPDIR=> 1);

    # A file in the above temp directory
    $filename = catfile($tmpdir,'step1.txt');

    print "tmpdir = $tmpdir\n";
    print "filename = $filename\n";


Using the script:

    ## default tmp directory
    $ perl example.pl
    tmpdir = /tmp/lobstr.Ziqv9r/
    filename = /tmp/lobstr.Ziqv9r/step1.txt

    ## custom tmp directory
    $ export TMPDIR=/data/gordon/tmp/
    $ perl example.pl
    tmpdir =  /data/gordon/tmp/lobstr.teWY_P
    filename =  /data/gordon/tmp/lobstr.teWY_P/step1.txt


## NOTE about Pytohn/Perl with invalid TMPDIR

Python and Perl tries to 'help' developers by hiding technical details from them.
If the directory in TMPDIR is not accessible, they will try other directories
which out complaining or notifying the user (where as sane programs will fail
with an error message).

Examples:

`mktemp` - fails if directory doesn't exist (which is a Good Thing):

    $ TMPDIR=/foo/bar mktemp -t
    mktemp: failed to create file via template ‘/foo/bar/tmp.XXXXXXXXXX’: No such file or directory

Python will ignore the failure and try other directories:

    $ TMPDIR=/foo/bar python example.py
    tmpdir =  /tmp/lobstrzNlf6K
    filename =  /tmp/lobstrzNlf6K/step1.txt

Perl will ignore the failure too:

    $ TMPDIR=/foo/bar perl example.pl
    tmpdir = /tmp/lobstr.bwccSd

So always ensure your temp-directory is accessible.

# C

To the best of my knowledge, there's no standard (POSIX) way to automatically
use TMPDIR.  The following code should work on Unix systems:

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <err.h>

    int main(void)
    {
      const char *dirtemplate = "lobstr.XXXXXX";
      const char *tmpdir = NULL;
      /* Get TMPDIR env variable or fall back to /tmp/ */
      tmpdir = getenv("TMPDIR");
      if (tmpdir==NULL)
        tmpdir = "/tmp" ;

      /* Construct a template using 'tmpdir' */
      size_t len = strlen(tmpdir) + 1
                   + strlen(dirtemplate) + 1;
      char *template = calloc( len, 1 );
      if (template == NULL)
        err (1, "calloc(%zu,1) failed", len);
      strcpy(template, tmpdir);
      strcat(template, "/");
      strcat(template, dirtemplate);

      /* Create temporary directory */
      if (mkdtemp(template)==NULL)
        err (1, "mkdtemp(%s) failed",template);
      printf("tmpdir = %s\n", template);

     /* Construct a filename */
      const char* filetemplate="step1.txt";
      len = strlen(template)+1+strlen(filetemplate)+1;
      char *filename = calloc(len,1);
      if (filename==NULL)
        err (1, "calloc(%zu,1) failed", len);
      strcpy(filename,template);
      strcat(filename,"/");
      strcat(filename,filetemplate);
      printf("filename = %s\n", filename);

      return 0;
    }


Using the code:

    ## Compile the code
    $ gcc -Wall -Wextra -o ex1 example.c

    ## Use with default directory
    $ ./ex1
    tmpdir = /tmp/lobstr.kFLKey
    filename = /tmp/lobstr.kFLKey/step1.txt

    ## Use with custom directory
    $ TMPDIR=/data/gordon/tmp ./ex1
    tmpdir =  /data/gordon/tmp/lobstr.KBAewp
    filename =  /data/gordon/tmp/lobstr.KBAewp/step1.txt

    ## Use with invalid directory
    $ TMPDIR=/foo/bar/ ./ex1
    ex1: mkdtemp(/foo/bar//lobstr.Fhrenm) failed: No such file or directory

## Automatically deleting temporary direcotries

Using the shell's `trap` command you can automatically delete the temporary
directory, even in case the shell script terminated with an error, or by
CTRL+C:

    #!/bin/sh

    # Create tepmorary directory
    DIR=$(mktemp -d -t test.XXXXXX) || exit 1

    # When the script terminates, run the 'rm' command
    trap "rm -rf '$DIR'" EXIT

    # run your programs..
    my-program 1
    my-other-program --foo --bar

    # When the script ends (even with CTRL+C or an error),
    # the 'trap' command will be executed.

**NOTE**: When debugging, you'd probably want to comment-out this command,
to keep the temporary files available.

## BAD THINGS to avoid

* Do not create multiple temporary files directly in `/tmp/` (or which ever
  temporary directory. Instead - create on temporary directory, and create files
  inside it.
* Do not hard-code "/tmp/" in temporary file names you create.
* Do not assume "/tmp" is the temporary directory

## Security Considerations

There are several intricate security consideration when using temporary
files for critical processing (e.g. system files owned by root, or security
related operations).
Those are not covered here.

## Bonus round - sorting in memory

GNU Sort can sort very big files (much larger than available memory) by using
temporary files. But sorting completely in-memory without temporary files is
much faster (if you have enough RAM).

By pointing sort to an invalid temporary directory, you can ensure `sort` does
not use the disk (but you'll have to give it enough RAM to use).

Examples:

Default 'sort' - whether it uses temporary disk depends on the size of the
input file, and the amount of RAM in the system:

    $ sort INPUT > OUTPUT

When sorting from PIPE, sort can't tell how much RAM to use (because the size
of the input is unknown):

     $ program | sort > OUTPUT

Using `-s` you can tell SORT how much RAM to use:

    # Use upto 10GB of RAM:
    $ sort -S 10G INPUT > OUTPUT

By using an invalid temporary directory, you can force `sort` to use RAM (if the data fits) or simply fail:

    $ sort -S 10G -T /no/such/dir INPUT > OUTPUT

Example, try to sort 76MB of data using only 10MB of RAM:

    $ seq 10000000 | wc -c |numfmt --to=iec
    76M
    $ seq 10000000  | sort -S 10M -T /no/such/dir > /dev/null
    sort: cannot create temporary file in ‘/no/such/dir’: No such file or directory

Which indicates you'll need more RAM to sort the data in-memory without temporary files.
