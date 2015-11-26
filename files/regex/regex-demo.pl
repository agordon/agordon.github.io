#!/usr/bin/env perl
use strict;
use warnings;

# Perl Quick Regex Tutorial:
#   http://perldoc.perl.org/perlrequick.html
# Perl Long Regex Tutorial:
#   http://perldoc.perl.org/perlretut.html
# Perl Full Regex Syntax:
#   http://perldoc.perl.org/perlrequick.html

my $data = "chr1   65436543   rsID776";

# Regex to test if string matches
if ($data =~ m/^chr/) {
	print "Found match! line starts with 'chr'\n";
}

# Regex to extract information (ie. 'grouping')
# Get the number following the 'chr', store it in '$1'
if ($data =~ m/^chr([0-9]+)/) {
	print "found chromosome: $1\n";
}
