#!/usr/bin/env node

// Javascript Regex Tutorial:
//   https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
// Javascript Regex Reference:

var data = "chr1   65436543   rsID776";

// Test if 'data' matches the regex. returns NULL if no match found.
if (data.match(/^chr/)) {
    console.log("Found match! line starts with 'chr'");
}

// Regex to extract information (ie. 'grouping')
// Get the number following the 'chr', store it in array 'm'
// 'm' will be NULL if no match is found.
var m = data.match(/^chr([0-9]+)/);
if (m) {
   console.log("found chromosome: ", m[1]);
}
