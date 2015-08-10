#!/usr/bin/env Rscript

# Command-line parsing Example
# Copyright (C) 2015 Assaf Gordon (assafgordon@gmail.com)
# License: MIT
# See: http://crashcourse.housegordon.org/command-line-parsing.html

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
