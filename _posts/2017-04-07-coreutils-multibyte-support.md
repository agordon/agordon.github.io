---
title: "GNU Coreutils - Multibyte/unicode support"
date: 2017-04-07
layout: post
---

# {{ page.title }}

Random notes and pointers regarding the on-going effort to add
multibyte and unicode support in [GNU Coreutils](https://gnu.org/s/coreutils).

If you're considering working on multibyte/unicode/utf8 support in GNU coreutils
(or other packages) - reading these should bring you up to speed (and hopefully
save some time, too).

NOTE: *multibyte*, *multibyte-sequences*, *unicode*, *utf-8* are sometimes used
interchangeably throughout the document, but the intent is to support
all multibyte locales, not just UTF8 encodings.

Content
-------

1.  [**Relevant Discussions on coreutils' mailing lists**](#relevant_discussion) -
    long and technical discussions with lots of relevant information.
1.  [**Related Bug Reports**](#related_bugs) - various bugs reports
    from past years. Linked here if they contain useful points and/or
    detailed replies.
1.  [**Useful websites**](#useful_websites) - good readings
1.  [**Online tools**](#online_tools) - websites providing useful
    conversions and information.
1.  [**Low-level command-line conversion**](#lowlevel_tools) - using
    printf,od,uconv,perl.
1.  [**invalid sequences**](#invalid_sequences) - invalid sequences.
1.  [**Unicode glyph rendering**](#glyph_rendering) - interplay between
    libc and xterm.
1.  [**cygwin and 16-bit wchar_t**](#cygwin) - special handling for systems where
    wchar_t is 16-bit, and UTF-16 surrogates (cygwin/OpenSolaris/AIX).
1.  [**glyph width and wcwidth issues**](#wcwidth) - issues relating to
    incorrect wcwidth(3) results and different glyph rendering.
1.  [**expand**](#expand) - expand topics.
1.  [**wc**](#wc) - wc topics.
1.  [**cut**](#cut) - cut topics.
1.  [**head/tail**](#head_tail) - head/tail topics.
1.  [**tr**](#tr) - tr topics.
1.  [**fold/fmt**](#fold_fmt) - fold and fmt topics.
1.  [**od**](#od) - od topics.
1.  [**unorm**](#unorm) - unorm topics.
1.  [**Unicode Explained: The Book**](#unicode_book) - pointers to relevant pages.


<a name="relevant_discussion"></a>

Relevant Discussions on Coreutils' mailing lists
------------------------------------------------

* [Pádraig Brady](https://www.pixelbeat.org) maintains a repository
  containing RedHat's incomplete implementation at
  <https://github.com/pixelb/coreutils/tree/i18n>, with more details
  at <http://www.pixelbeat.org/docs/coreutils_i18n/>.

* 2017-Apr-4:
  [multibyte support (round 3)](http://lists.gnu.org/archive/html/coreutils/2017-04/msg00009.html) -
  Patch with added `fold(1)` support.

* 2016-Sep-19:
  [multibyte support (round 3)](http://lists.gnu.org/archive/html/coreutils/2016-09/msg00026.html) -
  Patch with added `cut(1)` support.

* 2016-Sep-4:
  [Multibyte support (round 2)](http://lists.gnu.org/archive/html/coreutils/2016-09/msg00011.html) -
  Patch with `unorm` and `expand` working with UTF-16.  Expanded
  description of `unorm`, and issues with `expand` and width of Emoji
  unicode characters

* 2016-Jul-20:
  [multibyte processing - handling invalid sequences (long)](http://lists.gnu.org/archive/html/coreutils/2016-07/msg00013.html) -
  Thread about handling invalid sequences. Also contains a list
  of coreutils programs and their multibyte-related needs.

  * [2016-Jul-21](http://lists.gnu.org/archive/html/coreutils/2016-07/msg00016.html) -
    discussion and introduction of `mbfix` (a precursor of `unorm`).

    Following messages in the thread discuss unicode normalization
    (NFKD,NFKD,NFC,NFD).

* 2015-Sep-25:
  [PATCH: Multibyte support for expand and unexpand v2](https://lists.gnu.org/archive/html/coreutils/2015-10/msg00000.html) - patch by Ondrej Oprala.

* 2011-Feb-2:
  [bug#7971: Bug in libiconv](https://lists.gnu.org/archive/html/bug-coreutils/2011-02/msg00018.html) -
  Lots of details about Cygwin and wchar_t/utf-16.

* 2011-Feb-2:
  [bug#7948: 16-bit wchar_t on Windows and Cygwin](https://debbugs.gnu.org/7948)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2011-02/msg00001.html) -
  Lots of technical details about cygwin (and similar) systems where wchar_t is 16-bits
  by Bruno Haible, Eric Blake and others.
  Also discussed: naming a new typedef `wwchar_t` , `xchar_t` etc.

* 2010-Sep-13:
  [PATCH: join: support multi-byte character encodings](https://lists.gnu.org/archive/html/coreutils/2010-09/msg00029.html) -
  patch by Pádraig Brady followed by detailed discussions. Pádraig
  emphasized (off-list): "Note in that patch the avoidance of startup
  overhead for printf due to avoiding dynamically linking with
  libunistring."

* 2009-Feb-21:
  [Re: new modules for Unicode normalization](https://lists.gnu.org/archive/html/bug-coreutils/2009-02/msg00224.html) by Bruno Haible - this is gnulib's `uninorm` module.

* 2009-Mar-11:
  [bug in join: case comparisons don't work in multibyte locales](https://lists.gnu.org/archive/html/bug-coreutils/2009-03/msg00102.html) - detailed and technical discussion started by Bruno Haible,
  lead to the creation of [GNU libunistring](https://lists.gnu.org/archive/html/bug-coreutils/2009-03/msg00156.html).

* 2008-May-8:
  [Re: horrible utf-8 performace in wc](http://lists.gnu.org/archive/html/bug-coreutils/2008-05/msg00063.html) -
  coreutils' `wc` supported multibyte characters for a long while. This discussion
  resulted in [processing speed-ups](http://lists.gnu.org/archive/html/bug-coreutils/2008-05/msg00065.html).

* 2006-Jul-31:
  [uniq i18n implementation](https://lists.gnu.org/archive/html/bug-coreutils/2006-07/msg00153.html)
  by Pádraig Brady.





<a name="related_bugs"></a>

Related Bug Reports
-------------------

#### tr

* [bug#20114: tr does not support multibyte characters in the first	argument](https://debbugs.gnu.org/20114)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2015-03/msg00044.html))

* [bug#26362: tr -cd -- Problem with UTF-8?](https://debbugs.gnu.org/26263)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2017-04/msg00008.html))

* [tr is handling bytes not characters](https://lists.gnu.org/archive/html/bug-coreutils/2009-02/msg00028.html)
  from 5 Feb 2009.

* [Multibyte Awareness](https://lists.gnu.org/archive/html/coreutils/2017-02/msg00039.html) -
  Pádraig mentions `sed` as temporary work-around for missing `tr`
  case-conversion code.

#### printf

* [Incomplete support of unicode characters in printf \u](https://lists.gnu.org/archive/html/coreutils/2016-03/msg00026.html).
  [thread continues here](https://lists.gnu.org/archive/html/coreutils/2016-04/msg00006.html).
  Conclusion seem to be that this should be fixed/improved.

* [bug#17196: UTF-8 printf string formating problem](https://debbugs.gnu.org/17196)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2014-04/msg00049.html)) -
  long discussion with many details and examples about `printf '%s'` and multiybyte
  characters.

* [/usr/bin/printf: invalid universal character name](https://lists.gnu.org/archive/html/bug-coreutils/2008-05/msg00068.html) - Jim Meyering explains why `printf` refuses to print certain escape
  sequences (a requirement of 'C99, ISO/IEC 10646').


#### wc

* [WC counts UTF-16 codepoints](https://lists.gnu.org/archive/html/coreutils/2015-05/msg00017.html)

* [WC does not count invalid multibyte sequences](https://lists.gnu.org/archive/html/coreutils/2015-11/msg00132.html) - this thread started the [Coreutils' Gotcha](http://www.pixelbeat.org/docs/coreutils-gotchas.html) page.

* [bug#20751: wc -m doesn't count UTF-8 characters properly](https://debbugs.gnu.org/20751)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2015-06/msg00054.html))


#### Sort

* [bug#17189: Sort bug #2](https://debbugs.gnu.org/17189)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2014-04/msg00040.html)) -
  sort ignores punctuation in non-C locales.
  Lots of detailed emails form Eric Blake.

* [bugs#24601: UTF-8 locale makes lexicographic sort weird](https://debbugs.gnu.org/24601)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2016-10/msg00003.html))
  [This message](https://lists.gnu.org/archive/html/bug-coreutils/2016-10/msg00017.html)
  in the thread provides a simple C program to test `strcoll` behaviour.

* [bugs#23677: sort --debug not ignoring punctuation when sort does](https://debbugs.gnu.org/23677)
  Karl Berry raises the issue that sorting in anything except `LC_ALL=C` locale
  is highly problematic - due to 'secodary' role of punctuations.

* [bug#21844: sort behavior unstable based on neighboring elements ?](https://debbugs.gnu.org/21844)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2015-11/msg00006.html))

* [bug#8871: Bug with "sort -i" ?](https://debbugs.gnu.org/8871)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2011-06/msg00090.html)) -
  Details from Eric, also mentioning RedHat's i18n patches vs upstream's lack of multibyte support.

* [bug#9418: Fwd: bug#9418: case sensitivity buggy in sort](https://debbugs.gnu.org/9418)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2011-09/msg00018.html)) -
  locale related confusion. Quote:

        > > Yes, that is exactly the case - why on earth would someone want that?
        > > This results in just some sorting madness!
        >
        > Complaints have been made about glibc's absurd and insane preference for
        > case insensitive collation (at least in en and the euro locales) for
        > nearly 20 years now.  All w/o resolution.

* [Re: sort seems deficient](https://lists.gnu.org/archive/html/bug-coreutils/2008-09/msg00072.html) -
  locale/punctuation related confusion. This message from Jim Meyering contains
  simple example of the problem.


#### Other programs

* [bugs#24924: pr has no concept of wide characters](https://debbugs.gnu.org/24924)
  (same on [mailing list](TODO)).

  [Last message on thread](https://debbugs.gnu.org/cgi/bugreport.cgi?bug=24924#26)
  from Stephane Chazelas mentions `pr` bug in BIG5-HKSCS locale.

* [pr considers bytes not presentation width](https://lists.gnu.org/archive/html/bug-coreutils/2006-12/msg00251.html)
  report by Dan Jacobson with examples in both UTF-8 and big5 encoding.

* [bug#25630: df Unicode is not supported on mounted](https://debbugs.gnu.org/25630)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2017-02/msg00008.html))

* [bug#25550: Apparent unicode bug in uniq 8.26](https://debbugs.gnu.org/25550)
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2017-01/msg00097.html))

* [od and unicode](https://lists.gnu.org/archive/html/coreutils/2014-12/msg00004.html) -
  detailed message but discussion did not ensue.

* [Unicode characters in tail and head](https://lists.gnu.org/archive/html/bug-coreutils/2010-02/msg00078.html) -
  discussion about `head --chars`. Eric Blake's reply still reasonates:

  > "Eventually, when someone contributes a maintainable patch that does not
  > bloat the code size and that is still efficient for unibyte locales, then
  > yes, we would like to support multibyte character processing in the
  > various text-based utilities."

* [bug#22001: Is it possible to tab separate concatenated files?](https://debbugs.gnu.org/cgi/bugreport.cgi?bug=22001#26) - not directly unicode related, but thread turned into a discussion
  about what constitutes a *text* file (according to POSIX and whatsnot).
  (same on [mailing list](https://lists.gnu.org/archive/html/bug-coreutils/2015-11/msg00055.html))


* [terrible Unicode shattering fold(1) command](https://lists.gnu.org/archive/html/bug-coreutils/2008-08/msg00194.html) - with examples in Thai language. Quote from James Youngman:

  > FWIW, that is hard in languages like Thai, where it's hard to
  > distinguish which bits are the words and where the reasonable breaks
  > are.
  >
  > See for example
  > http://cpan.uwinnipeg.ca/htdocs/String-Thai-Segmentation/String/Thai/Segmentation.pm.html


* TODO: `bug#7960: fmt: fix formatting multibyte text (bug #7372)`





<a name="useful_websites"></a>

Useful websites
---------------

* List of unicode letters in different languages:
  <http://www.ltg.ed.ac.uk/~richard/unicode-sample.html>

* UTF-8 Samples: <http://www.columbia.edu/~fdc/utf8/> -
  Paragraphs and sentenses in multiple scripts.

* The case for UTF8 everywhere: <http://utf8everywhere.org/> -
  Long and interesting read.

* Examples Of Unicode Usage For Business Applications:
  <http://www.i18nguy.com/unicode/unicode-example-intro.html> -
  files in various formats containing utf-8 data.

* UTF-8 and Unicode FAQ for Unix/Linux by **Markus Kuhn**:
  <https://www.cl.cam.ac.uk/~mgk25/unicode.html> - a must read.

* **Markus Kuhn**'s UTF-8 decoder capability and stress test
  <https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt> -
  The gold standard in UTF-8 testing.

  The unorm/mbbuffer tests in [this patch](http://lists.gnu.org/archive/html/coreutils/2017-04/msg00009.html)
  are closely modelled after this stress tests
  (see [test-mbbuffer.c](/files/coreutils-unicode/test-mbbuffer.c) - comments
   such as `/* 4.1.2 */` refer to test 4.1.2 in the UTF-8 stress test).

* Dark corners of unicode: <https://eev.ee/blog/2015/09/12/dark-corners-of-unicode/> -
  Abandon hope all ye who enter here.


* [GNU UniFont](http://unifoundry.com) aims to create a
  universal bitmap font which contains *ALL* unicode glyphs.
  Perhaps it's not as pretty as vector fonts, but it's very useful
  and important. They provide a unicode tutorial at
  <http://unifoundry.com/unicode-tutorial.html>.

* What Every Programmer Absolutely, Positively Needs To Know About
  Encodings And Character Sets To Work With
  Text <http://kunststube.net/encoding/> - basic but very good.

* The Absolute Minimum Every Software Developer Absolutely, Positively
  Must Know About Unicode and Character Sets (No
  Excuses!)<https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/> -
  Similar to the above, by Joel Spolsky.

<a name="online_tools"></a>

Online tools
------------

* Unicode Toys (online conversion): <http://qaz.wtf/u/>

* Examine unicode characters:

  * [fileformat.info](http://www.fileformat.info) - e.g.
    <http://www.fileformat.info/info/unicode/char/FB01/index.htm>

  * [codepoints.net](http://codepoints.net) - e.g.
    <https://codepoints.net/U+FB01>

  * [unicode.org's CLDR](http://unicode.org/cldr/) - e.g.
    <http://unicode.org/cldr/utility/character.jsp?a=FB01>


<a name="lowlevel_tools"></a>

Low-level command-line conversion
---------------------------------

Print unicode with perl:

    perl -e 'print "\x{3A3}\n"'
    perl -e 'print "\N{U+03A3}\n"'
    perl -e 'print "\N{GREEK CAPITAL LETTER SIGMA}\n"'

Using coreutils' printf (note that other printfs such as FreeBSD do not support `\u`):

    printf '\u03A3\n'
    printf '\U000003A3\n'

print octets with `od` (i.e. the binary encoding in the corrent locale, '\316\250'
is the octal representation of UTF-8 encoding for []()):

    $ printf 'Ψ\n' |  LC_ALL=C od -c -An
       316 250  \n

For maximum portability, always use `LC_ALL=C` (because FreeBSD's od
*does* support multibyte input and will not display the octet's octal
value). Print in octal, as every POSIX-compliant `printf` can handle
octal values:

    $ printf '\316\250\n'
    Ψ

Displaying hex unicode codepoints:

    $ printf "Σημ" | iconv -t UTF-16LE | od -tx2 -An
     03a3 03b7 03bc

The above assumes little-endian (e.g. intel) CPU. Change to UTF-16BE for
big-endian machines. It also assumes all code-points in the input fit
into 16-bits (which is not a safe assumption). If some characters
require more than 16-bit, a safer option is to use 32-bits for every
code point:

    $ printf "Σημ" | iconv -t UTF-32LE | od -tx4 -An
     000003a3 000003b7 000003bc

Checking for invalid multibyte-sequences with GNU sed:

The following example works in UTF-8 locale, and relies on the fact
the GNU sed's regular expression will *not* match invalid sequences
(i.e.  anything that was *not* replaces by the regex is invalid
octet).  If the output isn't empty, the input had invalid multibyte
sequenes:

    $ printf 'a\xCEc\n' | sed 's/.*//g' | od -tx1c -An
      ce 0a
      c  \n

    # Same detection for an input file:
    $ printf 'ab\nc\n\xCE\xCEde\n\xCE\xA3f\n' > invalid.txt

    $ sed -n 's/.//g ; H ; $@{x;s/\n//g;l@}' invalid.txt
    \316\316$

    # With few more commands, the offending line can be printed as well:
    $ sed -n 's/.//g;=;l' invalid.txt | paste - -  | awk '$2!="$"'
    3       \316\316$

    # GNU sed in C locale can edit octets directly:
    $ LC_ALL=C sed '3s/\o316\o316//' invalid.txt > fixed.txt


Converting UTF to \u sequences (using 'uconv' from [ICU package](http://site.icu-project.org)):

    $ printf "Σημεῖόν" | uconv -x 'hex-any ; any-hex'
    \u03A3\u03B7\u03BC\u03B5\u1FD6\u03CC\u03BD

Converting UTF-8 to named unicode charactes:

    $ printf "Σημεῖόν" | uconv -x 'hex-any ; any-name'
    \N{GREEK CAPITAL LETTER SIGMA}\N{GREEK SMALL LETTER ETA}
    \N{GREEK SMALL LETTER MU}\N{GREEK SMALL LETTER EPSILON}
    \N{GREEK SMALL LETTER IOTA WITH PERISPOMENI}
    \N{GREEK SMALL LETTER OMICRON WITH TONOS}\N{GREEK SMALL LETTER NU}


List of possible transliterations in 'uconv'/ICU:

    uconv -L | tr ' ' '\n' | grep -i any | sort -f |  less

    # such as:
    uconv -x 'hex-any ; any-hex/perl'
    uconv -x 'hex-any ; any-hex/java'
    uconv -x 'hex-any ; any-hex/c'

ICU's `uconv` supports several methods to handle invalid data
(called 'callbacks' in their man page). This is part of the inspiration
for `unorm` (the proposed coreutils program). Examples:

    $ printf 'ab\342cdef' | uconv
    Conversion to Unicode from codepage failed at input byte position 2. Bytes: e2 Error: Illegal character found
    $ printf 'ab\342cdef' | uconv --callback substitute
    ab�cdef
    $ printf 'ab\342cdef' | uconv --callback escape-c
    ab\xE2cdef



<a name="invalid_sequences"></a>

Invalid Sequences
-----------------

Modified-UTF-8 allows encoding NULL as 0xC0 0x80.  This allows the
byte with the value of zero, which is now not used for any character,
to be used as a string
terminator. <https://en.wikipedia.org/wiki/Null_character#Encoding>.

Invalid Sequences:
<https://en.wikipedia.org/wiki/UTF-8#Invalid_byte_sequences>
<https://en.wikipedia.org/wiki/UTF-8#Invalid_code_points>




<a name="glyph_rendering"></a>

Unicode glyph rendering
-----------------------

Show different unicode font implementation/support in terminals:

1.  Easy case: 'e' + combining mark (where a pre-combined 'e' exists):

        $ printf 'e\u0301\n'
        é

    Works on gnome-terminal, mac-os-x-terminal, xterm.
    doesn't work on 'st' (simple-terminal from st.suckless.org),
    prints 'e' followed by empty 'grave'.

2.  Advanced support: any letter (regardless of pre-combined letter
    support:

        $ printf 'x\u0301e\n'

    On gnome-terminal,mac-os-terminal, prints 'x' with grave
    (nonsensical, but graphically correct) followed by 'b'.

    On xterm, simple-term: prints 'xe'



<a name="cygwin"></a>


Cygwin (and other systems with 16-bit wchar_t)
----------------------------------------------

Cygwin UTF-16 problems: <https://cygwin.com/ml/cygwin/2011-02/msg00037.html> - long and
interesting discussion. First mention of possibility of `wwchar_t` and abstratction layer.

Cygwin Internationalization: <https://cygwin.com/cygwin-ug-net/setup-locale.html> - 
keeps recommending UTF8 everywhere.

How cygwin deals internally with windows filenames (which are UTF16):
<https://cygwin.com/cygwin-ug-net/using-specialnames.html#pathnames-unusual>


But iswalpha takes `wint_t` which IS int32_t - perhaps do conversion manually?
see <https://cygwin.com/ml/cygwin/2011-02/msg00039.html> and
<https://cygwin.com/ml/cygwin/2011-02/msg00044.html>.

1.  printf can generate them, but on wchar_t/64-bit systems,
    mbrtowc(3) can't decode them:

        $ printf '\ud800\n' | iconv -f utf-8 iconv:
        illegal input sequence at position 0

2.  A file containing:

        printf '\ud800\udc000\n' > 1.txt

    will be interpreted as 6 invalid octets on 64bit systems,
    and as either 'U+100000' or 'U+D800 U+DC00' on cygwin.
    which is correct ?

3.  On Cygwin, this input can be detected (and rejected to maintain
    consistency) by checking `mbstate_t.__count==4` .
    What about other systems ?


whcar_t is NOT always UCS4:
<https://www.gnu.org/software/libunistring/manual/html_node/The-wchar_005ft-mess.html>


#### OpenSolaris

In OpenSolaris, only under unicode locales, "wchar_t" is UTF-32 (good enough?).
from  <https://docs.oracle.com/cd/E36784_01/html/E39536/gmwkm.html>:

    The ISO/IEC 9899 standard does not specify the form or the
    encoding of the contents for the wchar_t data type. Because it is
    an implementation-specific data type, it is not portable.

    Although many implementations use some Unicode encoding forms for
    the contents of the wchar_t data type, do not assume that the
    contents ofwchar_t are Unicode. Some platforms use UCS-4 or UCS-2
    for their wide-character encoding.

    In Oracle Solaris, the internal form of wchar_t is specific to a
    locale.

    In the Oracle Solaris Unicode locales, wchar_t has the UTF-32
    Unicode encoding form, and other locales have different
    representations.



#### AIX

From <https://www.ibm.com/support/knowledgecenter/en/ssw_aix_53/com.ibm.aix.nls/doc/nlsgdrf/codeset_over.htm>:

    On AIX 5.1 and later, the wchar_t datatype is 32–bit in the 64–bit
    environment and 16–bit in the 32–bit environment.

    The locale methods have been standardized such that in most
    locales, the value stored in the wchar_t for a particular
    character will always be its Unicode data value. [...]  All
    locales use Unicode for their wide character code values (process
    code), except the IBM-eucTW codeset.




<a name="wcwidth"></a>

glyph width and wcwidth issues
------------------------------

`Expand`, `pr`, `fold`, `fmt` will have glyph-width related issues.
Some glyphs' widths can not be determined by libc -
but only by the graphical program that will render them on screen.

In other cases, the glyphs are *optionally* zero-width combining
characters, or stand-alone visible characters. Example: Skin-tone
modifiers (not zero width, but optionally is if it follows an face/hand emoji).
See <http://unicode.org/reports/tr51/#Diversity>.

This is EMOJI MODIFIER FITZPATRICK TYPE-1-2' ([U+1F3FB](https://codepoints.net/U+1F3FB?lang=en)):

    # With space (non-emoji) before the modifier, it is rendered as a normal character:
    $ printf '\U0001F466 \U0001F3FB\n'
    👦 🏻

    # with an emoji preceeding it, it is combined:
    $ printf '\U0001F466\U0001F3FB\n'
    👦🏻

    # NOTE for readers: whether the above is rendered as a single
    # face depends on your web-browser or text editor.

The `mbbuffer-debug` (from [this patch](http://lists.gnu.org/archive/html/coreutils/2017-04/msg00009.html))
is used below to examine multibyte input. The `W` column shows the result of
wcwidth() of the character.

When checking with `wcwidth`, it gives width of 1 on MAC OS X
('1' is not always accurate, depending on later combining rendering):

    $ printf '\U0001F3FB' | ./src/mbbuffer-debug -r
    ofs  line colB colC V wc(dec) wc(hex) Ch  W n octets
    0    1    1    1    y  127995 0x1f3fb =   1 4 0xf0 0x9f 0x8f 0xbb

Yet on glibc, wcwidth returns -1 for all SMP codepoints (as wcwidth
returns -1 for all non-printables):

    $ printf '\U0001F3FB' | ./src/mbbuffer-debug -r
    ofs  line colB colC V wc(dec) wc(hex) Ch  W n octets
    0    1    1    1    y  127995 0x1f3fb =  -1 4 0xf0 0x9f 0x8f 0xbb

It is not at all clear if there's a "correct" width,
as the visualization results differ based on the rendering environment
(the following looks different between Mac OSX terminal and gnome-terminal 3.6.2
and safari and chrome):

    $ printf 'a\U0001F466\U0001F3FBaa\tb\naaaa\tb\n'
    a👦🏻aa   b
    aaaa    b

Should we use 'wcswidth', or alternatively, process "EmojiModifiers"
propery? (see <http://unicode.org/reports/tr51/#Data_Files> but then,
the list of possible specific properies is endless).

Other "Modifier Symbols" (Category Sk): <https://codepoints.net/search?gc=Sk>

See also: Multi-Person Grouping:
<http://unicode.org/reports/tr51/#Multi_Person_Groupings>
Can be rendered as multiple icons or one combined icon (taking one or more characters).


More examples

joiner such as: [U+20E0 COMBINING ENCLOSING CIRCLE BACKSLASH](https://codepoints.net/U+20E0?lang=en)
which as an overlaid glyph, to indicate a prohibition or “NO”

    $ printf '\U0001F52b\u20E0\n'  # no guns
    🔫⃠

    $ printf '\U0001F399\u20E0\n'  # no microphones
    🎙⃠


Some characters are 'combining', and wcwidth *does* indicate
they have zero width (which is good for expand/pr/fold/fmt),
but when rendered they actually consume visual space
on the screen, messing up alignment.
This is [COMBINING ENCLOSING KEYCAP (U+20E3)](http://www.fileformat.info/info/unicode/char/20e3/index.htm):

    $ printf 'a\u20E3aa\tb\naaaa\tb\n'
    a⃣aa     b
    aaaa    b

    # this is multibyte-aware expand, still incorrect output:
    $  printf 'a\u20E3aa\tb\naaaa\tb\n'  | ./src/expand
    a⃣aa     b
    aaaa    b

    # Despite wcwidth giving W=2, the character is rendered
    # wider than a single column on the screen:
    $ printf 'X\u20E3\n' | ./src/mbbuffer-debug -r
    ofs  line colB colC V wc(dec) wc(hex) Ch  W n octets
    0    1    1    1    y      88 0x00058 X   1 1 X
    1    1    2    2    y    8419 0x020e3  ⃣   0 3 0xe2 0x83 0xa3
    4    1    5    3    y      10 0x0000a =  -1 1 0x0a

    # NOTE to readers:
    # On Mac OS X terminal, Safari and Firefox,
    # the above is rendered as 'a' surrounded by a square. YMMV.


TODO:

1. How many characters are NON-PRINTABLE (i.e. wcwidth()==-1), but in
   expand we do not treat them properly?  when adding columns in
   'expand', ensure wcwidth>0 ??  Do all "word_break" or
   "line_break" characters have wcwidth()==-1 ?
2. check wcwidth() on CJK idograms (does it return 2?)


#### Not bugs, but worth knowing

**Combined letters**

In [Laten Extended-B](https://en.wikipedia.org/wiki/Latin_Extended-B):
Some glyphs are 2-letters squeezed into a width of 1.
wcwidth on glibc and macos seems to handle it correctly (return width==1),
and on Xterm,Mac Terminal they are indeed rendered in width of 1
(there seems to be a problem on gnome-terminal/ubuntu-14.04, but that's
a font issue).

Example: [Dž](https://en.wikipedia.org/wiki/Dž):

    $ printf '\u01c4a\nbc\n'
    Ǆa
    bc

**Full Width glyphs**

Some glyphs are designated as full-width, meaning the consume
a width of 2 characters, and can be used for easy alignment with CJK
characters.
See <https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms#In_Unicode>

This is [Full-width capital B U+FF22](https://codepoints.net/U+FF22?lang=en):

    $ printf 'a\uFF22c\nabc\n'
    aＢc
    abc

Both glibc and MacOS-X wcwidth gives width==2 for these (which is good for
expand/pr/fmt/fold):

    $ printf '\uFF22' | ./src/mbbuffer-debug -r
    ofs  line colB colC V wc(dec) wc(hex) Ch  W n octets
    0    1    1    1    y   65314 0x0ff22 Ｂ  2 3 0xef 0xbc 0xa2


From [Cygwin's internationalization page](https://cygwin.com/cygwin-ug-net/setup-locale.html):

    There's a class of characters in the Unicode character set, called
    the "CJK Ambiguous Width" characters. For these characters, the
    width returned by the wcwidth/wcswidth functions is
    usually 1. This can be a problem with East-Asian languages, which
    historically use character sets where these characters have a
    width of 2. Therefore, wcwidth/wcswidth return 2 as the width of
    these characters when an East-Asian charset such as GBK or SJIS is
    selected, or when UTF-8 is selected and the language is specified
    as "zh" (Chinese), "ja" (Japanese), or "ko" (Korean). This is not
    correct in all circumstances, hence the locale modifier
    "@cjknarrow" can be used to force wcwidth/wcswidth to return 1 for
    the ambiguous width characters.



<a name="expand"></a>

expand
------

See [width/wcwidth](#wcwidth) issues above.



<a name="wc"></a>

wc
--

1. Add a special option in 'wc' to count non-zero width characters??
   (But then, what about optional modifiers, e.g. skin-color and
   family-joiner?)
2. What about counting SMP characters (which gives wcwidth()==-1).



<a name="cut"></a>

cut
---

option to never cut in a combining-mark?
(or technically, only cut in clear graphmeme? e.g. never before ZWJ, BIDI mark, etc.)?




<a name="head_tail"></a>

head/tail
---------

how to treat zero-width-joiners, how to treat combined characters ?  based on width ?





<a name="tr"></a>

tr
--

Multibyte sequence case conversion (the following works on Mac/FreeBSD,
not yet in coreutils):

    $ printf '\u0103\n'
    ă

    $ printf '\u0103\n' | /usr/bin/tr '[:lower:]' '[:upper:]'
    Ă

Pádraig Brady wrote (privately):
> I've also noticed interesting chars like the titlecase letter 'ǈ' (U+01C8)
> which is neither upper or lower but does have an upper case (U+01C7),
> or the fact the there are only 2 code points Ⱥ (U+023A) and Ⱦ (U+023E)
> that increase in length (2 to 3 bytes) when lower-cased.


Deleting multibyte-sequences:

    $ printf '\u0103b\u0106d\n'
    ăbĆd

    $ printf '\u0103b\u0106d\n' | LC_ALL=C od -tc -An
     304 203   b 304 206   d  \n

    # On Mac/FreeBSD, it works as expected:
    $ printf '\u0103b\u0106d\n' | tr -d 'ă' | LC_ALL=C od -tc -An
       b 304 206   d  \n

    # Coreutils 'tr' treats input as two independant octets, delete
    # both instances of \304 resulting in invalid output:
    $ printf '\u0103b\u0106d\n' | tr -d 'ă' | LC_ALL=C od -tc -An
       b 206   d  \n



[POSIX tr(1)](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/tr.html)
says (in "Extended Description"):

> "\octal - [...] Multi-byte characters require multiple, concatenated escape
> sequences of this type, including the leading <backslash> for each
> byte."

Based on my understanding of the above, the following 'should work':

    # It doesn't work at all on Mac/FreeBSD:
    $ printf '\u0103b\u0106d\n' | tr -d '\304\203' | LC_ALL=C od -tc -An
     304 203   b 304 206   d  \n

    # It doesn't work on GNU tr (since as above, it treats the octets indepedently):
    $ printf '\u0103b\u0106d\n' | tr -d '\304\203' | LC_ALL=C od -tc -An
       b 206   d  \n




1. Should uppercase mapping of ligatures turns into two letters?

        ## U+FB01 LATIN SMALL LIGATURE FI (ﬁ)

2. German [Capital Sharp S](https://en.wikipedia.org/wiki/Capital_ẞ) is a similar issue.

        $ printf '\uFB01' | tr '[:lower:]' '[:upper:]'

3.  POSIX says Chracter Ranges are UNDEFINED in non-posix locale:

        > "c-c"
        > "In locales other than the POSIX locale, this construct has unspecified behavior."

    How to handle these when we do implement multibyte support?


4. What does the `-C` (upper-case C) exactly do according to POSIX ?

        > "The ISO POSIX-2:1993 standard had a -c option that behaved
        > similarly to the -C option, but did not supply functionality
        > equivalent to the -c option specified in POSIX.1-2008."  The
        > earlier version also said that octal sequences referred to
        > collating elements and could be placed adjacent to each
        > other to specify multi-byte characters. However, it was
        > noted that this caused ambiguities because tr would not be
        > able to tell whether adjacent octal sequences were intending
        > to specify multi-byte characters or multiple single byte
        > characters. POSIX.1-2008 specifies that octal sequences
        > always refer to single byte binary values when used to
        > specify an endpoint of a range of collating elements.  "

5. Equivalence classes: The following is supposed to work
   (i.e. replace also the umlaut-a into X), but does not work
   on FreeBSD-10.3/OpenBSD-6 which supposed to support it (TODO: check on musl-libc):

        $ printf 'abc \303\244\303\202 def\n' | LC_ALL=en_US.UTF-8 tr '[=a=]' X
        Xbc äÂ def

   There is no portable for an application to determine 'equivalence class'
   without knowledge of libc internals. FreeBSD's tr is supposed
   to be able to do it by assuming it knows the internals of its libc:
   <https://github.com/freebsd/freebsd/blob/master/usr.bin/tr/str.c#L212>.

   A lot depends on the system's libc. For example, the following works
   on glibc but not on Mac (in both cases using GNU sed):

        # works on glibc with gnu sed:
        $ printf 'abc \303\244\303\202 def\n' | LC_ALL=en_US.UTF-8 sed 's/[[=a=]]/X/g' 
        Xbc XX def



Implementation issues:
The critical strucutres in the [tr code](https://git.savannah.gnu.org/cgit/coreutils.git/tree/src/tr.c#n107).

Other places also assume only 256 different values (e.g.
`enum { N_CHARS = UCHAR_MAX + 1 };`).




<a name="fold_fmt"></a>

fold/fmt
--------

character 'WJ' (word-joiner) - special treatment in 'fold / fmt'?

Does any 'space' character is space, or 'iswspace',
or only ASCII 0x20,0x09,0x0d ?





<a name="join"></a>

join
----

FreeBSD's join bails out on invalid sequences:
see function 'mbssep()' in <https://github.com/freebsd/freebsd/blob/master/usr.bin/join/join.c#L362>.

Currently join DOES support some locale-comparison,
as fields are compared with gnulib's `memcoll` (which uses `strcoll(3)` internally).

Two things that are not supported (and are partially implemented in redhat's i18n patch):

1. multibyte field delimiters - but the patch turns the global delimiter variable into a string,
   making processing slower in all cases.

2. Case-insensitive comparison - the patch allocates new buffers for every key (in every line)
   and iterates with mbrtowc+towupper.


Also, risk of collating into same order (cf. Karl Berry surprised results from sort
in [bug#23677](https://debbugs.gnu.org/23677).




<a name="od"></a>

od
--

In GNU:

    $ printf "\u03a8\n" | od -tx1c -An
       ce  a8  0a
      316 250  \n


In Mac/FreeBSD:

    $ printf  "\u03A8\n" | od -t x1c -An
      ce  a8  0a
      Ψ   **  \n

in Mac/FreeBSD: invalid mb-seqeuences:

    $ printf  "\xce\xce\n" | od -t x1c
      ce  ce  0a
     316 316  \n


Implementation problem: POSIX says the FIRST character of a valid
multibyte sequence should display the character, and the following
octets should show '**'. But the first octet might appear on the LAST
character of the line, and the '**' should be displayed on the
following line.

In FreeBSD, it 'just works':

    $ printf "aaaaaaaaaaaaaaa\316\250bb\n" | od -An -tc
           a   a   a   a   a   a   a   a   a   a   a   a   a   a   a   Ψ
          **   b   b  \n

They (FreeBSD) have implemented a 'peek' option following
a multibyte octet: <https://github.com/freebsd/freebsd/blob/master/usr.bin/hexdump/conv.c#L98>.

On GNU coreutils' od, it seems (IIUC) that the implementation
reads exactly the (known) amounts of octets needed to display
each line, and adding 'peeking' feature will be tricky:
<http://git.savannah.gnu.org/cgit/coreutils.git/tree/src/od.c#n1360>







<a name="unorm"></a>

unorm
-----

TODO: organize this mess...

Check normalization according to NormalizationTest.txt

Check compatiblity of:

    U+00B5 MICRO SIGN
    U+03BC GREEK SMALL LETTER MU

    U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE
    U+212B ANGSTROM SIGN

    U+03B2 GREEK CAPITAL LETTER BETA
    U+00DF LATIN SMALL LETTER SHARP S

    U+03A9 GREEK CAPITAL LETTER OMEGA
    U+2126 OHM SIGN

    U+03B5 GREEK SMALL LETTER EPSILON
    U+2208 ELEMENT OF0xEA

    U+005C REVERSE SOLIDUS
    U+FF3C FULLWIDTH REVERSE SOLIDUS

Unexpected?? U+00E6 LATIN SMALL LETTER AE (æ) is NOT decomposed:

> "Originally a ligature representing a Latin diphthong, it has been
> promoted to the full status of a letter in the alphabets of some
> languages, including Danish, Norwegian, Icelandic and Faroese."
>  - https://codepoints.net/U+00E6

However this is decomposable:

    U+FB01 LATIN SMALL LIGATURE FI (ﬁ)
    <https://codepoints.net/U+FB01>


Check decomposition of:
   wcwidth() on LATIN-EXtended-B  characters:
      \u01c4 Latin Capital Letter DZ with caron
      \u01c5 Latin Capital Letter D with Small Letter Z with caron
      \u01c6 Latin Small Letter DZ with caron
      \u01c7 Latin Capital Letter LJ
      \u01c8 Latin Capital Letter L with Small Letter J
      \u01c9 Latin Small Letter LJ
      \u01ca Latin Capital Letter NJ
      \u01cb Latin Capital Letter N with Small Letter J
      \u01cc Latin Small Letter NJ

      \u01f1 Latin Capital Letter DZ
      \u01f2 Latin Capital Letter D with Small Letter
      \u01f3 Latin Small Letter DZ

      \u1f6 Latin Capital Letter Hwair (seems to work through with wcwidth==1)

      \u01fC Latin Capital Letter AE with acute Ǽ (seems to woth with wcwidth==1)

      \u0238 Latin Small Letter DB Digraph ȸ (seems ok) - despite being called digraphs
      \u0239 Latin Small Letter QP Digraph ȹ (seems ok)


  ESPECIALLY the "DZ with Caron" - is it decomposed to D,Z,Caron or D,z-with-caron ?

and these two: does decompistion results in O,dot,macron ?

    \u0230 Latin Capital Letter O with dot above and macron Ȱ -
    \u0231 Latin Small Letter O with dot above and macron ȱ


Check decomposition/compatiblity of IPA block, e.g.

    \u2A3 Latin Small Letter DZ Digraph ʣ - does this translates to DZ, or
          to the Latin-Extended-B 'DZ' latter?
    up to and including:
    \u2AB Latin Small Letter LZ Digraph

Check compatability and decomposition of 'fullwidth' characters,
   see https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms#In_Unicode
   e.g. does '\uFF21' (full-width A) decomposes to ascii 'A' ?

Check compatibility/decomposition of entire block:
    https://en.wikipedia.org/wiki/Alphabetic_Presentation_Forms


mbbuffer
========

TODO: organize this mess...

Modified NULL (\xC0\x80)

(Unicode book page 282): Unicode conformance

     UNAssigned Code Points (C4)
     Test unassigned codes (don't generate, don't change) in all programs.
     Test non-characters (U+FFFE, U+FFFF)
     Test surrogate codes

Surrogate codepoints treated as invalid on "normal" unixes:

    $ printf '\uD800\n' | ./src/mbbuffer-test -r
    ofs  line colB colC V wc(dec) wc(hex) Ch w n octets
    0    1    1    1    n       *       * *  * 1 0xed
    1    1    2    2    n       *       * *  * 1 0xa0
    2    1    3    3    n       *       * *  * 1 0x80
    3    1    4    4    y      10 0x0000a =  -1 1 0x0a

but on Cygwin:

    Administrator@WIN-9FFSHRJAFVN ~/coreutils-8.25.71-1437c
    $  printf '\uD800\n' | ./src/mbbuffer-test -r
    ofs  line colB colC V wc(dec) wc(hex) Ch  W n octets
    0    1    1    1    y   55296 0x0d800 =  -1 3 0xed 0xa0 0x80
    3    1    4    2    y      10 0x0000a =  -1 1 0x0a


page 437: Check all special characters
     and their effects in various programs.


TODO for Book:
     Show examples of conversion cases in page 501/502.

     sed (and grep/gawk) NEVER match regular expressions to invalid
       multibyte sequences. To Force matching, use LC_ALL=C.

     $ printf '\xe1\xbc\x11' | LC_ALL=C ./sed/sed 's/./X/g' | od -tx1
     0000000 58 58 58
     0000003


TODO: Special handling for "modified UTF-8" with NULL as

      UTF-8 "\xC0\x80" ?
      system's native mbrtowc does not handle it,
      and will return -1 .

TODO: prepare for all types of invalid sequences:

      https://en.wikipedia.org/wiki/UTF-8#Invalid_byte_sequences :
      ----
      Not all sequences of bytes are valid UTF-8. A UTF-8 decoder should be prepared for:
      * the red invalid bytes in the above table
      * an unexpected continuation byte
      * a leading byte not followed by enough continuation bytes (can happen in
        simple string truncation, when a string is too long to fit when copying it)
      * an overlong encoding as described above
      * a sequence that decodes to an invalid code point as described below

      https://en.wikipedia.org/wiki/UTF-8#Invalid_code_points :
      ------
      Since RFC 3629 (November 2003), the high and low
      surrogate halves used by UTF-16 (U+D800 through U+DFFF) and code
      points not encodable by UTF-16 (those after U+10FFFF) are not
      legal Unicode values, and their UTF-8 encoding must be treated
      as an invalid byte sequence.

      Not decoding surrogate halves makes it impossible to store
      invalid UTF-16, such as Windows filenames, as UTF-8. Therefore,
      detecting these as errors is often not implemented and there are
      attempts to define this behavior formally (see WTF-8 and CESU
      below).


from https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt:

Section3.3  Sequences with last continuation byte missing:

    All bytes of an incomplete sequence should be signalled as a single
    malformed sequence, i.e., you should see only a single replacement
    character in each of the next 10 tests. (Characters as in section 2).

Mbbuffer currently reports EACH invalid octet instead
of just one per incomplete sequence.

TODO: Does incomplete sequence in the middle of the file
reported as incomplete (mbrtowc==-2) or invalid (mbrtowc==-1) ?

If we report on the FIRST octet (including line,byte/char offset),
the user (needing low-level processing) won't be able to tell
the differences without further processing. By reporting
all octets, we provide easier work-arounds
(but we also 'pollute' stdout with more "invalid char" markers
than needed). Perhaps add this as an option?

On Ubuntu 14.04 with xterm 322, terminal prints only one "invalid char":

    $ printf '\ud800\n'
    �

On Ubuntu 14.04 with gnome-terminal 3.6.2, nothing is printf.

Mac OS X terminal prints 3 question marks:

    $ printf '\ud800\n'
    ???

Web browsers print 3 characters:
  visit https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
  and view section 5.1.1.

On Linux: Google Chrom 51.0, Firefox 48.0
On Mac: Safari 8.0.7, Chrome 47.0, IceCat 37.0

    $ printf '\367\277\277\n' | ./src/mbbuffer-test.exe -r
    ofs  line colB colC V wc(dec) wc(hex) Ch  W n octets
    0    1    1    1    n       *       * *   * 1 0xf7
    1    1    2    2    n       *       * *   * 1 0xbf
    2    1    3    3    n       *       * *   * 1 0xbf
    3    1    4    4    y      10 0x0000a =  -1 1 0x0a


Also see seciont 5.1 (Single UTF-16 surrogates)
where he claims each invalid sequence should result in ONE
"invalid character" output:
e.g.

    5.1.1  U+D800 = ed a0 80 = "���"

In such cases 'mbrtowc' return -1 THREE times (or is it because
we reset mbstate_t after each failure?)



TODO:

    "[...] U+FFFE and U+FFFF must not occur in normalUTF-8 or UCS-4
    data. UTF-8 decoders should treat them like malformedor overlong
    sequences for safety reasons."
    (http://m.blog.csdn.net/article/details?id=50910387)





<a name="unicode_book"></a>

Unicode Book
------------

**HIGHLY RECOMMENDED**

---

![unicode-explained-cover](http://akamaicovers.oreilly.com/images/9780596101213/cat.gif)

**Unicode Explained**

Internationalize Documents, Programs, and Web Sites

By Jukka K. Korpela

<http://shop.oreilly.com/product/9780596101213.do>

---

The following are pointers and notes from the above book which
seemd (IMHO) relevant for coreutils' multibyte implementation
(or for testing).

page 11: Finish har har har - change with char-classes, regex, normalization, upper/lower cases

page 12: ligature "fi": change for normalization, char classes

page 23: German lower-case "strasse" (sharp-S?) becomes "SS" in upper-case (two characters).
         Also differ from greek "beta" glyph.
         '\u00DF'

page23: 0-with-cross is diameter in mechanical writing, or a letter in Nordic
        languages?

Length of BIDI markers (zero width?)

page 29 (2nd paragraph from bottom): Greek Sigma in middle vs final form.
        If there's no equivalence between them, how about sort order ?

page 29 (top): initial/middle/final/separate contextual forms (e.g hebrew/arabic)
        Sort order ?

Page 143: Transcoding tools
     http://www.unicode.org/Public/MAPPINGS
     TODO: Download these for offline processing.

Page 145: Repertiore requirements
      Characters in each language:
      http://www.eki.ee/letter

Page 169: Named Sequences
     http://www.unicode.org/Public/UNIDATA/NamedSequences.txt

Page 178: Table 4.3: Code-point Classification
     TODO: Test unassigned, Surrogate, Private-Use input.
           Ensure no bugs, should be passed as it.
           What about "wc" and "cut" ?

Page 182: DiGraph
     e.g "ll" in Spanish, "Ch" in some others - two distinct characters
         logically treated as one by native language speakers.
     VS
     æ (\u00E6) which is one character for "ae".
     ĳ (\u0133) which is small latin ligature "ij".
     TODO: Check unicode-normalization-decomposition.

Page 185: unicode standard - chapters
     Chapter 5: Implementation Guidelines

Page 194: Varient Selectors
     Unicode markers affecting the precending code-point,
     ∩︀ (\u2229 - "intersection" symbol) followed by \uFE00
     ("variant selector" VS1). Affect font in applicaiton ?
     IS this Zero width character ?
     TODO: check with 'expand', 'cut', 'wc'.

Page 195: Ligatures.
     in Danish/Norwegian, æ (\u00E6) is an independent letter,
     vs just a ligature of two letters "ae" in other languages.
     TODO: Test sort order with such input in Danish-vs-other locales.
     TODO: in Danish locale, should unicode normaliztion NOT decompose it??
     Unicode "Alphabetic PResentation Form" block (U+FB00..U+FB4F).

     TODO: Test decomposition of ligatures in that block (e.g. hebrew ligatures?)
     $ printf '\ufb00\n'
     ﬀ
     $ printf '\ufb03\n'
     ﬃ
     $ printf '\ufb4a\n'
תּ

     ZWJ (\u200d) should instruct the application to join the
     characters before/afer into legature.
     Doesn't seem to work (on Mac OS):
        $ printf 'f\u200Di\n'
        f i

     Similarly, ZWNJ (\u200C) should prevent joining.
     TODO: test ZWJ,ZWNJ (zero width or "invisible control" chars?)
     in cut/expand/wc.


Page 196: Vowels vs Marks
     Hebrew+Arabic: Nikud.

     Hindi (Devanagaris script):
     \u092A (pa) followed by \u0942 (uu) appears as one glyph (puu).

Page 211, Table 5-1: General Category VAlues.

Page 216: Character Property 'ea' = Asian Width Full,Half,narrow.
     Affects 'expand' ?

Page 216: Grapheme Clusters? for 'fold/fmt/cut' ?

Page 219,220: Use 'WB' (WordBreak)' or 'WS' (Whitespace) 'SB' (Sentense-break)
     properties for counding-words in 'wc' ?

     gfdafda d dfsa fdsa fdsa
     fdafda fdsafdsa

Page 220: Property 'SFC' (Simple-Case-Folding): Upper/Lower case are simple.

Page 227: Canonical vs Compatability mapping
       Canonical: different encoding for SAME symbol.
       Compatibility: fundamentally similar characters, differ in rendering/
                      usage (and sometimes in meaning)

     Examples in Book
     \u2126 = \u03a9

Page 231:
     Iterative decompisition:

     ANGSTRAM (U+212b):
       $ printf '\u212b\n'
       Å
     Is canonical-mapped to 'A-with-Ring U+00C5':
       $ printf '\u00c5\n'
       Å
     Which is canonical mapped to 'A + combining mark ring (U+030a)':
       $ printf 'A\u30a\n'
       Å

Page 233:

     Decomposition of 'VULGAR HALF', 'MICRO SIGN', 'E WITH GRAVE':

       $ printf '\u00BD\u00b5\u00e8\n'
       ½µè

     Becomes:
        VULGAR HALF => 1 'FRACTION SLASH' 2
        MICRO SIGN  => greek mu
        'E WITH GRAVE' => 'E' 'COMBING MARK GRAVE'

    With decomposition (E + combing grave mark):
      $ printf '\u00BD\u00b5\u00e8\n'| ./src/unorm -n nfkd  | iconv -t ucs-2le | od -tx2 -An
      0031 2044 0032 03bc 0065 0300 000a

    Without decomposition ('E WITH GRAVE' stays as-is):
      $ printf '\u00BD\u00b5\u00e8\n'| ./src/unorm -n nfkc  | iconv -t ucs-2le | od -tx2
      0031 2044 0032 03bc 00e8 000a

    TODO: for 'sort', 'uniq', 'join':
       Test the above strings as 'equivalent' (strxfrm/strcoll) ?

Page 249: Collation order
     no official collation order.
     Unicode Technical STandard #10
     http://www.unicode.org/reports/tr30/tr30-4.html

Page 256: Text Boundaries
     See the files in /Users/gordon/projects/unicode-mapping/www.unicode.org/Public/9.0.0/ucd/auxiliary
     like WordBreakProprty.txt
     includes test files
     TODO: for wc,fold,fmt,cut ?
     TODO: instead of 'iswspace' is unicode ''Alphabetic' Property?

     For Book: document exceptions for Thai/Lao/Hiragana ?

Page 276: Line-BReaking rules
     for fold/fmt ?

Page 282: Unicode Conformance requirements
     TODO: Test unassigned codes (don't generate, don't change) in all programs.

Page 285:
     Conformance: C12a: unorm is conformant.

Page 286:
     Conformance: C14,15,16 (normalization): unorm is conformant.

page 287:
     Conformance: When mentioning normalization, use proper terms
                  (for unorm)

Page 299: UTF-8 vs ISO-8859-1
     For Book

Page 300: Duplicate Octet Range rable, add octal

Page 392: Duplicate table of control characters, add octal
     mention sed, printf, od
     for book/ /website

Page 414: Fixed with charachers
     (e.g. em/en dashes)
     TODO: How to treat in 'expand' ?

page 426: Line-break chracters in unicode
     for fold/fmt , what about 'wc' ?
     LS (U+2028) Line Separator
     PS (U+2029) Paragraph separator
     For Book/website

Page 426: mathenatical and technical symbols
     For Book/website: canocnical compatiblity with other chars.

Page 438:
     'other' non alphabetical markers, should they be counted as words?

     $ env printf '\ufff9assaf\ufffagordon\ufffb\n' |  wc
     1       1      21

     in HTML this would be rendered as two words, assaf/gordon.


Page 468: Invisible characters ?

Page 469:
     MArkup vs plaintext:
     Table 9-2: should these characters be counted in 'wc',
     skipped in 'expand', non-break with 'cut' ?

     Are these considerd "word break" properties?
     should SED's "\b \B \< \>" regex operators support them?

Page 592: Patterns, regex patterns.
     TODO: ensure tests cases according to page 594.

page 597: "Basic Unicode Support"
     TODO: Check which coreutils fall under the requirements,
           and whether they comply.





Last but not least
==================


Support the cause: Adopt a Unicode Character!
<http://www.unicode.org/consortium/adopted-characters.html>




Unorganized (yet)
-----------------


OpenBSD removes non-utf8 locales: <http://marc.info/?l=openbsd-cvs&m=143956261214725&w=2>

<http://unix.stackexchange.com/questions/90100/convert-between-unicode-normalization-forms-on-the-unix-command-line>


TODO: learn from grep's multibyte-white-space test
