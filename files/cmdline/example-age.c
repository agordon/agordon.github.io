/*
  Command-line parsing Example
  Copyright (C) 2015 Assaf Gordon (assafgordon@gmail.com)
  License: MIT
  See: http://crashcourse.housegordon.org/command-line-parsing.html
*/

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
