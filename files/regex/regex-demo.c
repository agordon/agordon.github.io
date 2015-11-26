/*
 to compile:
     cc -Wall -g -o regex-demo regex-demo.c
 to run:
     ./regex-demo
*/
#include <string.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main()
{
    const char *data = "chr1   65436543   rsID776";
    regex_t re;
    #define MAX_MATCHES (10)
    regmatch_t matches[MAX_MATCHES];

    // Compile the regex
    int i = regcomp(&re,"^chr",REG_EXTENDED);
    assert (i==0);

    // Test it on the string
    i = regexec(&re, data, 0, NULL, 0);
    if (i != REG_NOMATCH) {
	printf("Found match! line starts with 'chr'\n");
    }
    regfree(&re);


    // Compile a regex with grouping
    i = regcomp(&re,"^chr([0-9]+)",REG_EXTENDED);
    assert (i==0);

    // Test it, results will be stored in 'matches'
    i = regexec(&re, data, MAX_MATCHES, (regmatch_t*)&matches, 0);
    if ( i != REG_NOMATCH ) {
        // matches[1].rm_so => start-offset of match
        // matches[1].rm_eo => end-offset of match
        const int len = matches[1].rm_eo - matches[1].rm_so;
        const char *ptr = data + matches[1].rm_so;
        // extract the matched value into a new string
        char *val = strndup(ptr, len);
        printf("found chromosome: %s\n", val);
	free(val);
    }
    regfree(&re);

    return 0;
}
