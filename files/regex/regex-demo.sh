#!/bin/sh

# NOTE:
# 'grep -E' to use Extended Regular expression in grep (the default is 'basic').
#
# 'sed -r' to use Extended regular expressions in sed
#          (sadly does not work on Mac).

data="chr1   65436543   rsID776"

# option 1: print lines that match the regex
echo "Matching lines:"
echo "$data" | grep -E '^chr'
echo
echo

# option 2: just check if there is a match and print nothing
# 'grep -q' means 'quiet' (don't print anything)
if echo "$data" | grep -q -E '^chr' ; then
	echo 'Found match! line starts with 'chr'\n'
fi

# sed trick:
# The regex will find:
#   1. lines starting with 'chr'
#   2. followed by digits
#   3. then anything (.*)
# And will be replaced by whatever was found in the parenthesis group
echo "found chromosome: "
echo "$data" | sed -r 's/^chr([0-9]*).*/\1/'

