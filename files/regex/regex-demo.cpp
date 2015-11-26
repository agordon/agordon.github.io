/*
 NOTE:
    Using std::regex requires g++>=4.9 or a recent enough clang.
 to compile:
     c++ -std=c++11 -Wall -g -o regex-demo-cpp regex-demo.cpp
 to run:
     ./regex-demo-cpp
*/
#include <iostream>
#include <string>
#include <regex>

using namespace std;

/*
  NOTES:
  std::regex_match => requires the ENTIRE string to match the regex
                      (as if with '^' and '$' anchors).
  std::regex_search => match any part of the string.

  The above funtions accepts a 'flags' parameter specifing the regex flavor,
  defaulting to EMCAScript if none is given.
  See: http://www.cplusplus.com/reference/regex/regex_constants/
       http://www.cplusplus.com/reference/regex/ECMAScript/
*/

int main()
{
    const string data("chr1   65436543   rsID776");

    const regex re("^chr");
    if (std::regex_search(data,re)) {
	cout << "Found match! line starts with 'chr'" << endl;
    }

    const regex re2("^chr(\\d+)");
    smatch matches;
    if (regex_search(data,matches,re2)) {
        cout << "found chromosome: " << matches[1] << endl;
    }

    return 0;
}
