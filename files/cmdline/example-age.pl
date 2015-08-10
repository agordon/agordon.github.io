#!/usr/bin/env perl

# Command-line parsing Example
# Copyright (C) 2015 Assaf Gordon (assafgordon@gmail.com)
# License: MIT
# See: http://crashcourse.housegordon.org/command-line-parsing.html

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
