---
title: "Finding and Deleting files with find"
layout: post
date:   2014-11-19
---

# {{ page.title }}

This post (originally: a long email) was written in response to a friend's
question of how to find and delete certain files to free up a space on a
lab's shared server.

## Part 1 - Using "find" without any criteria - list all files

The command "find" can be used to list files that match a certain criteria.
"criteria" can be: file name, file size, file owner, etc.

The first parameter should be the name of the directory to search in.

Example: Find all files under `/home/alon`:

    find /home/alon

Example: Find all files under `/seq/epiprod/`:

    find /seq/epiprod/

You can use "." to search the current directory.
You can omit the directory name if you want to search in the current directory,
but I'd recommend against it.

Examples: find all files under `/home/alon`:

    cd /home/alon
    find .

    cd /home/alon
    find


## Part 2 - Using "find" with criteria

After the directory name, you can add one or more criteria (technically,
called "predicates"). The list of available criteria are found in `man find`.
predicates begin with one dash (minus character), and usually require an additional parameter.

Example: find all files under `/home/alon` whose name ends in "bam"
(note: don't forget the quotes):

    find /home/alon -name "*.bam"

Example: find all files under `/seq/epiprod/` whose owner is "goren":

    find /seq/epiprod/ -user goren

Example: find all files under `/seq/epiprod/` whose group-onwer is "icmgrp":

    find /seq/epiprod/  -group icmpgrp

Example: find all empty files under `/seq/epiprod`:

    find /seq/epiprod/ -empty

Example: find all directories (exclude files) under `/seq/epiprod`:

    find /seq/epiprod/ -type d


## Part 3 - Using "find" with size criteria

The `-size` predicate allows you find files of certain size.

> NOTE  
> The number after "size" MUST have a suffix, otherwise you'll get unexpected results.  
> Meaning: `find /home/alon -size 4000` WILL NOT DO WHAT YOU WANT.

The suffixes are:

* `-size 500c`   =  500 bytes (think: characters)
* `-size 3k`     =  3*1024 bytes (think: kilobytes)
* `-size 7M`     =  7*1048576 bytes (think: megabytes)
* `-size 2G`     =  2*1073741824 bytes (think: gigabytes)

Additionally, adding `-` to the size means "less than",
and adding `+` to the size means "greater than".

Examples:

* `-size -1000c`   = less than 1000 bytes
* `-size -40k`     = less than 40KB
* `-size +1G`      = greater than 1GB

NOTE: due to technical issues, the size comparison with k/M/G suffixes should be considered approximation.
Specifically, using `-size -1M` or `-size -1K` or `-size -1G` will not give you the expected results.

Example: find files in `/home/alon` which are smaller than 10MB:

    find /home/alon -size -10M

Example: find files in `/home/alon` which are bigger than 1G:

    find /home/alon -size +1G


## Part 4 - combining "find" creterias

find criteria can be combined in one command.
There are some tricky subtleties about this, which I will ignore for now.
The simple predicates (e.g `-name`, `-user`, `-group`, `-size`) should
"just work" (but better to always verify).

Example: find all files with have "BAM" in the name AND bigger than 1G:

    find /home/alon -name "*.bam" -size +1G

## Part 5 - Listing the files

find's output is the list of file names which match the criteria.
To list them with full details (such as with `ls -l`),
I'd recommend using `xargs`.

Example: find files bigger than 1G, list them with `ls -l`:

    find /home/alon -size +1G | xargs ls -l

Example: find files bigger than 2M, list with with `ls -lh`
(showing sizes with "human sizes", e.g. 40K instead of 40394):

    find /home/alon -size +2M | xargs ls -lh

**NOTE:**  
The above commands (and in fact, anything with `xargs`) will only work as
long as your file names DO NOT HAVE SPACES.  
If you're one of the crazy people who user spaces in their unix file names,
or if you've transferred files from Mac/Windows, the above will not work.
Use this instead:

    find /home/alon -size +2M -print0 | xargs -0 ls -lh

Adding `-print0` as the last part to "find" and adding `-0` as the first
parameter to `xargs` will work-around filenames with spaces.
In fact, it's always recommended to use this method.


## Part 6 - Deleting files with "find"

**DO NOT JUST DELETE THE FILES WITHOUT LOOKING AT THE FILE LIST.**

You are very likely to specify the wrong "find" criteria in the first couple
of attempt - which will delete the wrong files.

To automatically delete all the files matching the criteria, add the `-delete`
predicate. With `-delete`, find will DELETE the matching files instead of
printing them.

I would *highly* recommend first running `find` without delete,
and examining the listed files.
If you are happy with the list, then use `-delete`.

**NOTE**:
`-delete` must be the LAST predicate. Otherwise you'll delete all files.

**NOTE**:
When deleting files, I recommend adding `-type f` criteria (meaning
find only files, not directories)

Example: delete files under `/home/alon` which are bigger than 4GB and
have "*.bam" file name:

    find /home/alon -type f -size +4G -name "*.bam" -delete


## Part 7 - Move files before deleting

A Safer way to clean-up space is the MOVE all the files you've find to a
different directory, then examine them, and only then delete them.

Step 1: Create a directory to put the files.

    mkdir /seq/epiprod/test_before_delete

The directory MUST be on the same disk as the existing files,
otherwise it will be very slow and also unsafe.
That is, If you're cleaning files from `/home/alon/project/foo`,
move them to somewhere under `/home/alon`.
If you're cleaning files from `/seq/epiprod/goren`, move to to somehwere
under `/seq/epiprod/`.
(This was not an technically accurate description, but it should do for now).

Step 2: determine the correct "find" crtierias.
Example, all "BAM" files bigger than 2G:

    find /seq/epiprod/alon -type f -name "*.bam" -size +2G

Step 3: Use `xargs`+`ls` to examine the list

    find /seq/epiprod/alon -type f -name "*.bam" -size +2G  -print0 \
        | xargs -0 ls -lh

Step 4: move all the found files to the directory we created in step 1:

    find /seq/epiprod/alon -type f -name "*.bam" -size +2G -print0 \
        | xargs -0 mv --backup=numbered -t /seq/epiprod/test_before_delete

You can then check the size of files you're about to delete:

    du -sh /seq/epiprod/test_before_delete

It's even better to leave the files in this directory untouch (don't delete
them) for a short while, to ensure you didn't delete anything critical.

If three files had the same name but in different directories (e.g. `README.TXT`),
they will be named:

    README.TXT
    README.TXT.~1~
    README.TXT.~2~
    etc.

