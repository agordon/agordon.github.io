#!/usr/bin/env python

# Command-line parsing Example
# Copyright (C) 2015 Assaf Gordon (assafgordon@gmail.com)
# License: MIT
# See: http://crashcourse.housegordon.org/command-line-parsing.html

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
