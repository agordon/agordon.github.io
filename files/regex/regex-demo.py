#!/usr/bin/env python
import re

# Python Regex Howto + Syntax
# https://docs.python.org/2/howto/regex.html
data = "chr1   65436543   rsID776"


# Build a Regex Object based on desired pattern
regex = re.compile('^chr')
if regex.search(data):
    print "Found match! line starts with 'chr'"

# Regex to extract information (ie. 'grouping')
# Get the number following the 'chr', store in object 'm'
regex = re.compile('^chr([0-9]+)')
m = regex.search(data)
if m:
    print "found chromosome: ", m.group(1)
