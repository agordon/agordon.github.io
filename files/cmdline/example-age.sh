#!/bin/sh

# Command-line parsing Example
# Copyright (C) 2015 Assaf Gordon (assafgordon@gmail.com)
# License: MIT
# See: http://crashcourse.housegordon.org/command-line-parsing.html

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
