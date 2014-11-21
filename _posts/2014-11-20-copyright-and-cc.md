---
title: "Copyright and Create-Common Licenses"
layout: post
date:   2014-11-20
---

# {{ page.title }}

**NOTE**: I am not a lawyer. This explanation is my personal understanding of
the copyright/licensing situtation.  
This is a layperson's explanation by a layperson.  
Corrections and suggestions are welcomed.

A friend asked: "Your blog states that all content is copy-righted and
CC-BY-NC-SA. isn't it an oxymoron?"

## TL;DR;

The short answer is "no" - these are not contradictory.

1. The statement "Copyright YEAR NAME" tells who owns the copyright
2. The statement "CC-BY-NC-SA" (or other like it) tells what is allowed
   to do with the creation.

## Copyright holder

The copyright statement is usually stated like this:

    Copyright [YEARS] [COPYRIGHT-HOLDER]

This asserts who owns the legal rights to the material.
It is commonly the author itself (as in: I wrote the blog post, I
own the copyright), but in more commercial environments, the copyright holder
and the author are different:

* With music, the record label can hold the copyright, not the singer/artists.
* With books, the publishing house holds the copyright, not the author.
* In commercial software, the company holds the copyright, not the programmer.
* In scientfic publications (depending on the journal), the journal might have
  the rights, not the scientists (which is changing with "open access" journals).

> NOTES:  
> 1. When writing code, it is common to add "(C)" after the word 'copyright'.  
> 2. When writing other documents which support the copyright symbol natively
>    (e.g. `&copy;` in HTML), the symbol can appear after the word 'copyright'.  
> 3. The word 'copyright' should appear in English.

After you've asserted the copyright holder, you can declare what is the allowed
usage of the created work (the license).

## Usage License

The usage license tells the consumers/users of the creation what they are
allowed to do with it.

Note that for technical legal reasons (the copyright laws are tricky), there
should be a known copyright holder in order to be able to apply a license to
any creation - which is why the copyright statement is needed.

The most common (and most restrictive) usage license is "All Rights Reserved"
- meaning you're practically not allowed to do anything with the creation,
except view it when legally allowed (e.g. renting a movie or listening to the music).

### Art ("Creative") licenses

For "art" (or more technically: created work which is not software code) there's
"Creative Commons" (CC). The are several CC licenses with varying degrees of
usage freedom:

* CC0 (<http://creativecommons.org/about/cc0>) - also known as "No Rights
  Reserved" - allows anything to be done with your creation, including modifying
  it, incorporating it in commercial work, including not giving you credit.

* CC-BY (<http://creativecommons.org/licenses/by/4.0/>) - ("Attribution") -
  anything is allowed, as long as proper credit is given to you.

* CC-BY-SA (<http://creativecommons.org/licenses/by-sa/4.0/>) - ("Attribution +
  Share Alike") - anything is allowed, as long as proper credit is given AND
  the shared/modified work is shared under the same license.

* CC-BY-ND (<http://creativecommons.org/licenses/by-nd/4.0/>) - ("Attribution +
  No Derivative") - sharing is OK as long as proper credit is given.
  Modifying or adapting the work is not allowed (i.e. it must be shared
  exactly as you've published it). Such license is usuful when publishing an
  opinion or a statement - you want it to be shared verbatim, never modified.

* *XX*-NC - ("Non Commercial") - to the three licenses, above, you can add
  a "Non-Commercial" limitation, which prohibits commercial use of your work
  (in addition to other limitation, such as "share alike" or "no derivatives").

The Creative Commons website (<http://creativecommons.org/>) has a page to
help you choose the license: <http://creativecommons.org/choose/>


### Software Licenses

Software licenses is a tricky subject, full of flamewars and ideaology
(and recently: multi-million-dollar lawsuits).

Part of the problem is that software is used in different way than "art":
A program can be compiled, distributed as binary, shared over a server, etc.
It can also be covered by patents (**which are not the same as copyright**).

I won't go into details, but will give few pointers.  
NOTE: All these websites are biased toward their own agenda, which is fine
as long as you're aware of it.

* Choose-A-License, from GitHub: <http://choosealicense.com/>

* A list of software licenses, with GNU/FSF's opinion about them:
  <http://www.gnu.org/licenses/license-list.html>

### Public domain

"Public Domain" is actually more complicated than it seems,
because it does have some legal complications, and is not always recognized
legally in all jurisdictions.

A short write-up is here: <http://creativecommons.org/about/pdm>

For "art", it's better to use "CC0" instead of public domain.

For code, use the GNU "All Permissive License"
(<http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html>)
Or something similar.

### If there's no copyright

Not sure about this one.

To the best of my understanding, if there is not explicit copyright because
the author was lazy, but it is implicitly understandable who is the author
- then if push comes to shove, the court would likely assert who is the author.

It is best to avoid questionable works which have no clear copyright holder.

### if there's no license

To the best of my understanding, if there is not explicit license,
courts would generally assume "All rights reserved" (if the matter
becomes a law-suit).

Critically, this means that a random piece of code you found on the internet
IS NOT FREE (as in freedom) to use if it doesn't have a clear license.

### License are tricky

To be legally binding, usage licenses must be carefully phrased.

You'll notice that the "Creative-Commons" licenses are already at version 4.  
The GNU GPL is at version 3, after years of deliberations and improvements.  
Even the simple BSD license has gone through several iterations.

It is really best to choose an existing, valid, well-established license than
to invent your own.

Some people are tired of the license mess, and think they can "stick it to
the man" by inventing their own funny license,  
e.g. The "Do what the F*
you want license" (<http://www.wtfpl.net/txt/copying/>).

In reality, it's not helping, because as it became abundantly clear in
recently lawsuits, copyright and licensing is an important business.
It's also a matter of principle: what do you want to allow users of your
creation to do: If you want to allow anything, use a well-worded license like "CC0".

### Interesting Trivia

* For some GNU programs, when someone contributes code to the projects,
  he/she is requested to assign copyright to Free Software foundation (FSF).  
  This helps in enforcing GPL compliance (against companies who violate GPL),
  because only the copyright holder is allowed to do so. More information at:
  <https://www.gnu.org/licenses/why-assign.html>.

* The practice of assigning copyright is very common, and is commonly called
  "Contributor License Agreement" (<http://en.wikipedia.org/wiki/Contributor_License_Agreement>).

* To make critical changes to a creation (e.g. changing the usage license),
  the agreement of ALL copyright holders is required.
  If a person contributed even a tiny fragment of code, he is also a copyright
  holder in the project.
  A nice example is the re-licensing of an old Text-mode computer game called
  Moria (<http://en.wikipedia.org/wiki/Moria_%28video_game%29>).
  First released in 1983, it was re-licensed as GPL in 2007, after a determined
  developer tracked each contributed to the source code and asked for their
  agreement to the re-licensing.  
  You can see the list here: <http://free-moria.sourceforge.net/>
  and read about his efforts here: <http://www.freesoftwaremagazine.com/articles/freeing_an_old_game_moria>

* To improve tracking of who did what, some projects (e.g. Linux Kernel) require
  specific lines to be added to every submitted change. Sometimes called
  "sign-off" line, explained here: <http://gerrit.googlecode.com/svn/documentation/2.0/user-signedoffby.html>

### Further Reading

* [How to Choose a license for your own work](http://www.gnu.org/licenses/license-recommendations.html)
* [What is CopyLeft](http://www.gnu.org/copyleft/copyleft.html)
* [Licenses in General](http://www.gnu.org/licenses/)
* [Copyright Wikipedia Article](http://en.wikipedia.org/wiki/Copyright)

