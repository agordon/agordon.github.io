---
title: "Command-line parsing in multiple programming languages"
date: 2015-06-15
layout: post
---

# {{ page.title }}

## Do's

1. Use the language's recommended mechanism:
    1. **C** - [getopt_long](http://linux.die.net/man/3/getopt_long)
       (fallback: [getopt(3)](http://pubs.opengroup.org/onlinepubs/9699919799/functions/getopt.html)
       supports only short options but more standardize on unix platforms).
       (see [example-age.c](./files/cmdline/example-age.c)).
    2. **perl** - [Getopt::Long](https://metacpan.org/pod/Getopt::Long)
       (see [example-age.pl](./files/cmdline/example-age.pl)).
    3. **python** - [argparse](https://docs.python.org/2/library/argparse.html)
       (see [example-age.py](./files/cmdline/example-age.py)).
    4. **R** - [optparse](http://cran.r-project.org/web/packages/optparse/index.html)
       (see [example-age.r](./files/cmdline/example-age.r)).
    5. **Shell** - [getopt](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/getopts.html),
       (or fallback to `$1` ONLY for simple scripts, with proper validation).
       (see [example-age.sh](./files/cmdline/example-age.sh)).
3. Support `-h` (and optionally `--help`) for usage information.
4. optionally support long options (e.g. `--parallel`) - **always** with two dashes.

## Dont's

1. **R** - Do not use `commandArgs` except in very simple scripts. Do not
   use `argparse` as it requires python.
2. **C** - Do not use `argv[]` directly except in very simple programs
   (unless combined with proper `getopt_long` usage).
3. **Python** - Do not use `sys.argv` except in very simple scripts.
4. **Perl** - Do not use `@argv` except in very simple scripts (or when
   combined with proper `Getopt::Long` usage).
5. **Shell** - Do not use `getopt` (i.e. `/usr/bin/getopt`).
   NOTE: this is different than `getopts` (with `s`) - which is OK to use.
6. **Java** - Do not use java.
7. DO NOT UNDER ANY CIRCUMSTANCES use single dash with long option
   (e.g. `foobar -version`).

## Proper etiquette - the Unix way

1.  If your program outputs one file (or one stream for multiple files),
    send it to STDOUT by default.  
    Optionally - allow setting output filename with `-o FILE` or `--output FILE`.  
    Example: `sort FILE > OUT` and `sort -o OUT FILE`.

2.  If your program accepts ONE file, it should be the LAST non-option
    (i.e. positional parameter).  
    If your program can work with pipes, allow the user to not specify any
    filename, and read from STDIN by default.  
    Example: `sort FILE` and `cat FILE | sort`.

3.  if your program accepts multiple files and produces one stream of output
    (e.g. STDOUT), accept all files as last non-option (positional) parameters.  
    Example: `sort FILE1 FILE2 FILE3 > out`

4.  If your program produces one output file for each input file, **do not**
    automatically calculate on the filename (and **never** calculate
    the filename based on removing some extension of the input file).  
    Bad example: `foobar a.sam` which automatically creates `a.bam` by
    changing the extension `.sam`.

5.  warnings and errors must be printed to STDERR (not STDOUT).

6.  If errors encountered, the program must exit with non-zero exit code.

7.  If no errors happpened, the program should exit with zero exit code.

8.  Progress messages should be printed only if the user asked for `--verbose`
    (alternatively: provide `--quiet` or `--silent` option to turn off
    all progress messages).

9.  If your program generates multiple files, consider one of two options:

    9.1. Allow the user to specify a prefix.
         Example: `myprogram --prefix /data/foo/bar input.txt` will read
        `input.txt` and produce `/data/foo/bar.log`, `/data/foo/bar.txt`,
        `/data/foo/bar.err`, etc.

    9.2. Allow the user to specify an output directory.
        Example: `myprogram --outdir /data/foo/bar input.txt` will read
        `input.txt`, and will create `/data/foo/bar/report.txt`,
        `/data/foo/bar/error.log`, `/data/foo/bar/chart.png`, etc.

    Bad behaviour to avoid:

    9.3. Do not create multiple files with fixed names in the current directory.
         (e.g. create `chart.png`, `results.txt` and `error.log` in the current
         directory).

    9.4. Do no create multiple files based on the input file name, with new extensions.
         (e.g. given `mydata.txt` create `mydata.results`,`mydata.log` and `mydata.png`).

10. If your program uses temporary files, create a temporary **directory**
    using `mktemp(1) -d` or `mkdtemp(3)`, while respecting the `TMPDIR`
    environment variable. Then create the temporary files inside the
    directory (they can have fixed names).

## basic usage of all code examples

These examples show the basic command-line parsing in Perl/Pytohn/R/C/Shell.

They do not demonstrate file handling (see next post for that).

The following programs implement the same interface:

    $ ./example-age.pl --help
    This is the frobnicator.
    It says hello and prints your year-of-birth and age.

    Usage: example-age.pl [OPTIONS] FILE

    FILE                  = File to process

    Options:
    -h, --help            = This help screen.
    -n NAME, --name NAME  = Your name
    -a AGE,  --age AGE    = Your age
    -y YEAR, --year YEAR  = Your birth year
    -v, --verbose         = Be verbose.

    FILE, NAME are required.
    Either AGE or YEAR are required.

And the usage is similar in all implementations:

    # Perl
    $ ./example-age.pl --name assaf --age 21 foo.txt
    Hello assaf
    You were born in 1994 and you are 21 years old.
    File to process: foo.txt

    # Python
    $ ./example-age.py --name assaf --age 21 foo.txt
    Hello assaf
    You were born in 1994 and you are 21 years old.
    File to process: foo.txt

    # R
    $ ./example-age.r --name assaf --age 21 foo.txt
    Hello assaf
    You were born in 1994 and you are 21 years old.
    File to process: foo.txt

    # C
    $ ./example-age-c --name assaf --age 21 foo.txt
    Hello assaf
    You were born in 1994 and you are 21 years old.
    File to process: foo.txt

    # Shell - only short options supported
    $ ./example-age-1.sh -n assaf -a 21 foo.txt
    Hello assaf
    You were born in 1994 and you are 21 years old.
    File to process: foo.txt

**NOTES**

1. These example accept only options (i.e. those starting with `-`).
2. Output is always to STDOUT.
3. error checking is omitted for brevity.
4. The one exception is the shell-script example: it only
   implements short options (i.e. `-n` but not `--name`).
5. Not shown but highly recommended: when exiting with an error, print
   the program's name (or script name).
6. Not shown but recommended: if the program can read input from
   STDIN (instead of a file), allow operating without specifying the
   `FILE` parameter to mean 'read input from STDIN'.

### Example 1: Python

Download [example-age.py](./files/cmdline/example-age.py).

    #!/usr/bin/env python
    import argparse
    import sys
    from warnings import warn
    from datetime import date
    
    def parse_command_line():
        # Define parameters
        parser = argparse.ArgumentParser(description="This the frobnicator. " \
                               "It says hello and prints your year-of-birth and age.",
                        epilog="FILE, NAME are required. " \
                               "Either AGE or YEAR are required.")
    
        # Option parameters
        parser.add_argument("-n", "--name",     help="your name")
        parser.add_argument("-y", "--year",     help="year of birth", type=int)
        parser.add_argument("-a", "--age",      help="your current age", type=int)
        parser.add_argument("-v", "--verbose",  help="be verbose", action="store_true")
        # Positional parameter
        parser.add_argument('filename', metavar='FILE', help='file to process');
        args = parser.parse_args()
    
        # Validate parameters
        if args.name is None:
            sys.exit("missing --name. See -h for help.")
        if args.year is None and args.age is None:
            sys.exit("Either --age or --year must be specified. See -h for help.")
        if args.year is not None and args.age is not None:
            sys.exit("--age and --year are mutually exclusive.")
        return args
    
    if __name__ == "__main__":
        args = parse_command_line()
    
        current_year = date.today().year
        if args.verbose:
            print >> sys.stderr, "current year = ", current_year
    
        if args.year:
            your_age  = current_year - args.year
            birth_year = current_year
        if args.age:
            your_age  = args.age
            birth_year = current_year - args.age
    
        print "Hello",args.name
        print "You were born in",birth_year,"and you are",your_age,"years old."
        print "File to process:", args.filename

### Example 1: Perl

Download [example-age.pl](./files/cmdline/example-age.pl).

    #!/usr/bin/env perl
    use strict;
    use warnings;
    use File::Basename;
    use Getopt::Long;
    
    my $verbose;
    my $age;
    my $year;
    my $name;
    my $filename;
    
    sub usage()
    {
        my $base = basename $0;
        print<<"EOF";
    This is the frobnicator.
    It says hello and prints your year-of-birth and age.
    
    Usage: $base [OPTIONS] FILE
    
    FILE                      = File to process
    
    Options:
        -h, --help            = This help screen.
        -n NAME, --name NAME  = Your name
        -a AGE,  --age AGE    = Your age
        -y YEAR, --year YEAR  = Your birth year
        -v, --verbose         = Be verbose.
    
    FILE, NAME are required.
    Either AGE or YEAR are required.
    EOF
        exit 0
    }
    
    sub parse_command_line()
    {
        GetOptions("v|verbose" => \$verbose,
                   "n|name=s"  => \$name,
                   "a|age=i"   => \$age,
                   "y|year=i"  => \$year,
                   "h|help"    => \&usage)
            or die "failed to parse command line options. See -h for help.\n";
        die "missing --name. See -h for help\n" unless $name;
        die "Either --age or --year must be specified. See -h for help.\n"
            unless $age || $year;
        die "--age and --year are mutually exclusive.\n"
            if $age && $year;
    
        # Now ensure there are positional parameters left
        die "missing file name. See -h for help\n"
            unless @ARGV;
        $filename = shift @ARGV;
        # DO NOT silently ignore extra parameters - that will only confuse users
        die "extra operands found. See -h for help\n" if @ARGV;
    }
    
    parse_command_line;
    my @t = localtime;
    my $current_year = $t[5] + 1900;
    warn "current year = $current_year\n" if $verbose;
    
    my ($birth_year, $your_age);
    if ($age) {
        $birth_year = $current_year - $age;
        $your_age = $age;
    }
    if ($year) {
        $birth_year = $year;
        $your_age = $current_year - $birth_year;
    }
    
    print "Hello $name\n";
    print "You were born in $birth_year and you are $your_age years old.\n";
    print "File to process: $filename\n";

### Example 1: R

Download [example-age.r](./files/cmdline/example-age.r).

    #!/usr/bin/env Rscript
    
    library(optparse,quietly=TRUE)
    
    option_list <- list(
      make_option(c("-n","--name"), help = "Your name", type="character", default=NA),
      make_option(c("-a","--age"), help = "Your age", type="integer",default=NA),
      make_option(c("-y","--year"),help = "Your birth year", type="integer",default=NA),
      make_option(c("-v","--verbose"),help = "Be verbose", action="store_true", default=FALSE)
    )
    parser <- OptionParser(
       usage = paste("%prog [OPTIONS] FILE",
                     "This is the frobnicator. It says hello and prints your year-of-birth and age.",
                     "",
                     "FILE = file to process", sep="\n"),
       epilogue = "FILE, NAME are required.\nEither AGE or YEAR are required.",
       option_list=option_list)
    
    ## Hack note: far from ideal, but the tryCatch+is.na()
    ## will print a friendlier error on parsing error
    ## instead of R's default cryptic message.
    arguments=NA
    tryCatch(
    { arguments = parse_args(parser, positional_arguments=1);},
       error = function(e) { })
    if (all(is.na(arguments))) {
         stop (paste("Failed to parse command-line parameters",
                     "(missing filename?).",
                     "Use --help for help"))
    }
    opts = arguments$options
    file = arguments$args
    
    ## Parameter Validation
    if ( is.na(opts$name) ) { stop ("Missing --name. Use --help for help.") }
    if ( is.na(opts$age) && is.na(opts$year) ) {
            stop ( "Either --age or --year must be specified. Use --help for help.")
    }
    if ( !is.na(opts$age) && !is.na(opts$year) ) {
            stop ("--age and --year are mutually exclusive. Use --help for help.")
    }
    if (is.na(file)) {
            stop ("missing file name. Use --help for help")
    }
    
    
    current_year = as.integer(format(Sys.time(), "%Y"))
    if (opts$verbose) {
    	cat(paste("current_year =",current_year,"\n") ,file=stderr())
    }
    
    if (!is.na(opts$age)) {
    	your_age = opts$age
    	birth_year = current_year - your_age
    }
    if (!is.na(opts$year)) {
    	birth_year = opts$year
    	your_age = current_year - birth_year
    }
    
    cat(
     paste("Hello",opts$name,"\nYou were born in",birth_year,
            "and you are",your_age,"years old.\nFile to process:",
            file,"\n"));
    
    quit();

### Example 1: Shell

Download [example-age.sh](./files/cmdline/example-age.sh).

    #!/bin/sh
    
    die()
    {
        BASE=$(basename "$0")
        echo "$BASE: error: $@" >&2
        exit 1
    }
    
    show_help_and_exit()
    {
        BASE=$(basename "$0")
        echo "This is the frobnicator.
    It says hello and prints your year-of-birth and age.
    
    Usage: $BASE [OPTIONS] FILE
    
    Options:
        -h        = This help screen.
        -n NAME   = Your name
        -a AGE    = Your age
        -y YEAR   = Your birth year
        -v        = Be verbose.
    
    FILE, NAME are required.
    Either AGE or YEAR are required.
    "
        exit
    }
    
    # Default values for parameters
    show_usage=
    age=
    year=
    name=
    verbose=
    filename=
    # Parse parameters
    while getopts vhn:a:y: param
    do
        case $param in
        h)   show_help=1;;
        v)   verbose=1;;
        a)   age="$OPTARG";;
        y)   year="$OPTARG";;
        n)   name="$OPTARG";;
        ?)   die "unknown command line option";;
        esac
    done
    shift $(($OPTIND - 1))
    
    # Validate parameters
    test -n "$show_help" && show_help_and_exit
    
    test -z "$1" && die "missing file name. See -h for help"
    test -n "$2" && die "extra operands found ($2). See -h for help"
    test -z "$name" && die "missing name (-n). See -h for help"
    test -z "$age" && test -z "$year" \
        && die "Either age (-a) or year (-y) must be specified. See -h for help."
    test -n "$age" && test -n "$year" \
        && die "age(-a)  and year(-y) are mutually exclusive."
    
    filename="$1"
    
    current_year=$(date +%Y)
    if [ -n "$verbose" ]; then
        echo "current year = $current_year" >&2
    fi
    
    if [ -n "$age" ] ; then
        your_age=$age
        birth_year=$((current_year-$age))
    fi
    if [ -n "$year" ] ; then
        birth_year=$current_year
        age=$((current_year-$birth_year))
    fi
    
    echo "Hello $name"
    echo "You were born in $birth_year and you are $your_age years old.";
    echo "File to process: $filename"

### Example 1: C

Download [example-age.c](./files/cmdline/example-age.c).

    /* To compile:
         cc -o example-age-c example-age.c
    */
    #include <getopt.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <err.h>
    #include <time.h>
    
    int verbose=0;
    int age=-1;
    int year=-1;
    char* name=NULL;
    char *filename=NULL;
    
    static char const short_options[] = "a:n:y:hv";
    
    static struct option const long_options[] =
    {
    	{"age",     required_argument, NULL, 'a'},
    	{"year",    required_argument, NULL, 'y'},
    	{"name",    required_argument, NULL, 'n'},
    	{"help",    no_argument,       NULL, 'h'},
    	{"verbose", no_argument,       NULL, 'v'},
    	{NULL,      0,                 NULL, 0}
    };
    
    void usage(const char* progname)
    {
    	printf("\
    This is the frobnicator.\n\
    It says hello and prints your year-of-birth and age.\n\
    \n\
    Usage: %s [OPTIONS] FILE\n\
    \n\
    FILE                      = File to process\n\
    \n\
    Options:\n\
        -h, --help            = This help screen.\n\
        -n NAME, --name NAME  = Your name\n\
        -a AGE,  --age AGE    = Your age\n\
        -y YEAR, --year YEAR  = Your birth year\n\
        -v, --verbose         = Be verbose.\n\
    \n\
    FILE,NAME are required.\n\
    Either AGE or YEAR are required.\n\
    ", progname);
    	exit(0);
    }
    
    void parse_command_line(int argc, char* argv[])
    {
    	int optc;
    
    	while ((optc = getopt_long (argc, argv,
                                  short_options, long_options, NULL)) != -1) {
    		switch (optc)
    		{
    		case 'a':
    			age = atoi(optarg);
    			if (age<=0)
    				errx(1,"invalid age '%s'", optarg);
    			break;
    
    		case 'y':
    			year = atoi(optarg);
    			if (year<=0)
    				errx(1,"invalid year '%s'", optarg);
    			break;
    
    		case 'n':
    			name = optarg;
    			break;
    
    		case 'h':
    			usage(argv[0]);
    			break;
    
    		case 'v':
    			verbose = 1;
    			break;
    
    		default:
    			errx(1,"invalid command-line option");
    		}
    	}
    
    	/* Validate parameters */
        if (optind >= argc)
            errx(1,"missing FILE name. See --help for help");
        filename = argv[optind++];
        if (optind < argc)
            errx(1,"extra operand found (%s). See --help for help",
                   argv[optind]);
    	if (name==NULL)
    		errx(1,"missing --name. See --help for help");
    	if (age==-1 && year==-1)
    		errx(1,"Either --age or --year must be specified. See -h for help.");
    	if (age!=-1 && year!=-1)
    		errx(1,"--age and --year are mutually exclusive.");
    }
    
    int main(int argc, char* argv[])
    {
    	time_t t;
    	struct tm *tm;
    	int current_year;
    	int birth_year;
    	int your_age;
    
    	parse_command_line (argc, argv);
    
    	time(&t);
    	tm = gmtime(&t);
    	if (tm==NULL)
    		err(1,"gmtime failed");
    	current_year = tm->tm_year + 1900;
    	if (verbose)
    		fprintf(stderr,"current year = %d\n", current_year);
    
    	if (age != -1) {
    		birth_year = current_year - age;
    		your_age = age;
    	}
    	if (year != -1) {
    		birth_year = year;
    		your_age = current_year - birth_year;
    	}
    
    	printf("Hello %s\n", name);
    	printf("You were born in %d and you are %d years old.\n",
    		birth_year, your_age);
        printf("File to process: %s\n", filename);
    	return 0;
    }
