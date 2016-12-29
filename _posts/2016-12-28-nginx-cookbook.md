---
title: "NGINX Cookbook"
date: 2016-12-28
layout: post
---

# {{ page.title }}

Few examples of common nginx needs.

## HTTP to HTTPS redirection

    server {
        server_name foo.server.org ;
        location / {
           return 302 https://$host$request_uri;
        }
    }


## protect with either user/pw or IP

    # Limit access to the administration console
    location /admin/ {
        allow 1.2.3.4;
        allow 5.6.7.8;
        allow 127.0.0.1;
        deny  all;

        auth_basic           "Administration";
        auth_basic_user_file conf/htpasswd-file;

        # allow either IP or user/password
        satisfy any;
    }

## htpasswd files

Plain text (insecure but simple):

    $ cat htpasswd-file
    charlie:{PLAIN}mypassword12345

Salted SHA1 password:

A shell-based mentioned at <https://www.nginx.com/resources/wiki/community/faq/>:

    PASSWORD="SEcRe7PwD"
    SALT="$(openssl rand -base64 3)"
    SHA1=$(printf "$PASSWORD$SALT" \
          | openssl dgst -binary -sha1 \
          | xxd -ps \
          | sed 's#$#'"`echo -n $SALT | xxd -ps`"'#' | xxd -r -ps | base64);printf "Jim:{SSHA}$SHA1\n")

An easier script from <https://github.com/agordon/bin_scripts>:

    $ create-ssha-passwd -u charlie | sudo tee -a htpasswd-file
    Enter password:
    Repeat password:

The file will contain something like:

    charlie:{SSHA}7qbY4FyI8Dc9zsjC++w1QEYVQ5AuwpTr

For debugging purposes, add "-c" parameter to write the password in
plain text after the salted hash (which is insecure but handy):

    $ create-ssha-passwd -c -u charlie
    charlie:{SSHA}7qbY4FyI8Dc9zsjC++w1QEYVQ5AuwpTr:foobar

Recommended to limit access to the password file:

    sudo chown root:www-data htpasswd-file
    sudo chmod 0640 htpasswd-file



## Proxy error message fallback

Used when the back-end proxy server is down,
instead of showing ugly "HTTP 502 Bad Gateway" errors:

    server {
        ## Default location is the maintenance message.
        ## On HTTP Errors 502 (Bad Gateway) - show maintenance page.
        root /var/www/proxies/;

        # The content of this file will be displayed if the python proxy isn't working.
        error_page 502 /502.txt ;
        location /502.txt {
        }

       location / {
           proxy_pass http://127.0.0.1:10001;
       }
    }

Note:\
the display error is still an ugly text file (502.txt), but more
informative.  To display pretty HTML files, implicitly allow the HTML
file and other files (e.g css/png) BEFORE the catch-all "/" location.


## Catch-all locations

For any requested URL starting with "/foobar" - show one specific file.

    server {
        root /var/www/;
        location /foobar {
            # Doesn't matter which broken URL brought you here -
            # show the stub home page for this website
            rewrite ^.* /index.html break;
        }
    }


## directory path (root vs alias)

`alias` replaces the entire location URL.

`root` prepends a path to the requested URL.

    # http://server/r/foo/bar.txt becomes /srv/git/foo/bar.txt
    location /r {
        alias /srv/git;
        autoindex on;
    }


    # http://server/git/foo/bar.txt becomes /srv/git/foo/bar.txt
    location /git {
        root /srv;
        autoindex on;
    }


## CGI scripts

> **recommendation**
>
> disable the `SCRIPT_FILENAME` and `SCRIPT_NAME` settings in
> `/etc/nginx/fastcgi_params`.  Different settings are needed for
> different situations, > and having a common settings DOES NOT WORK.
>
> Set them independently in for each CGI script.

Install the standard `fcgiwrap` package, and ensure it runs as a service:

    apt-get install -yq fcgiwarp

On Debian/Ubuntu, `spawnfcgi` package will also be installed, and will
be used (automatically) to start the fcgiwrap program (this is the
prefered method).

On Debian/Ubuntu, the package is preconfigured to listen on a unix socket
at `/var/run/fcgiwrap.socket` (set in `/etc/init.d/fcgiwrap`).

If starting the deamon manually, run something like:

    fcgiwrap -c 5 -f -s /var/run/fcgiwrap.socket

### Handling fcgiwrap errors

In nginx configuration, the cgi script file can be specified
with `DOCUMENT_ROOT + SCRIPT_NAME` or with `SCRIPT_FILENAME`.

When the script is not found (or found but not executable),
fcgiwrap will report this error message:

    2016/12/12 17:28:45 [error] 27282#0: *35 FastCGI sent in stderr:
       "Cannot get script name, are DOCUMENT_ROOT and SCRIPT_NAME
        (or SCRIPT_FILENAME) set and is the script executable?"
       while reading response header from upstream, client: ::1,
       server: localhost, request: "GET /cgi1/ HTTP/1.1",
       upstream: "fastcgi://unix:/var/run/fcgiwrap.socket:",
       host: "localhost"

Sadly, it is not as helpful as it could be, and there's no easy way
to know which variable is set and used.

Be sure the define only one of them.

The following two settings are equivalent:

    location /cgi1/ {
        fastcgi_param SCRIPT_FILENAME  /path/to/script/cgi.sh;
        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }
    location /cgi2/ {
        fastcgi_param DOCUMENT_ROOT     /path/to/script;
        fastcgi_param SCRIPT_NAME       /cgi.sh;
        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }


### Simple CGI script (no parameters)

Visiting "http://server/servertime/" will run the CGI script and
return its output:

    location /servertime/ {
        fastcgi_param SCRIPT_FILENAME      /path/to/script.sh;
        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }

The script can be as simple as needed, e.g.:

    #!/bin/sh
    printf "content-type: text/plain\r\n\r\n"

    echo "Hello !"
    echo "Your remove address is ${REMOTE_ADDR}"
    echo "Server time is: $(date)"


### CGI script with HTTP GET parameters

Same nginx configuration as above.

HTTP/GET parameters will be sent to the script as the 'QUERY_STRING' environment variable.
If you change the script above to:

    #!/bin/sh
    printf "content-type: text/plain\r\n\r\n"

    echo "Hello !"
    echo "Your remove address is ${REMOTE_ADDR}"
    echo "Server time is: $(date)"
    echo "parameters = '$QUERY_STRING'

and use a URL such as `http://server/servertime/?timezone=JST`

Then 'QUERY_STRING' will contain 'timezone=JST'.

Perl's CGI is handy:

    #!/usr/bin/env perl
    use CGI qw/:standard/;

    @names = param;

    print header('text/plain');
    print "Hello! you've sent ", length(@names), " arameters:\n";
    for (@names) {
        print $_, " => ", param($_), "\n";
    }


with Python's CGI module:
(see https://docs.python.org/2/library/cgi.html)

    #!/usr/bin/env python

    import cgi
    form = cgi.FieldStorage()

    print "Content-Type: text/plain"
    print ""

    print "Hello!, you've sent these parameters:"
    for i in form.keys():
        print i, " => ", form[i].value


### PATH_INFO CGI parameter

In some setups is it preferable to pass the PATH of the URI
to the CGI script, e.g. given `http://server/downloads/foo/bar/file.txt` we
want to run `downloader.pl` and pass it `/foo/bar/file.txt` as a parameter.

The examples above would work as-is, except they would also pass the "/downloads/"
part of the PATH to the CGI script (in the  '$REQUEST_URI' variable).

Using nginx's `fastcgi_split_path_info` one can separate the base path (e.g. '/downloads/')
from the parameter part (e.g. '/foo/bar/file.txt').
This statement *must* have exactly two regex subexpressions. The first being the base path,
the second being the parameter to forward to the CGI script.

    location /downloads {
        # This command tells NGINX how to extract the path info part
        # from the requested URL: it trims the 'releases-redirect' part,
        # leaving only what follows it.
        fastcgi_split_path_info            ^(/downloads)(/?.+)$;

        # This command takes NGINX's path_info variable (extracted above),
        # and sends it to the FastCGI daemon as the PATH_INFO environment variable.
        fastcgi_param PATH_INFO            $fastcgi_path_info;

        fastcgi_param SCRIPT_FILENAME      /path/to/script/downloader.sh;

        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }

The `downloader.sh` script can be:

    #!/bin/sh
    printf "content-type: text/plain\r\n\r\n"

    echo "Hello !"
    echo "You've asked to download the following file: '$PATH_INFO'"
    echo "Extra parameters: '$QUERY_STRING'"

Given the URL
`http://localhost/downloads/foo/bar/file.txt?method=raw`, the output
of `downloader.sh` will be:

    Hello !
    You've asked to download the following file: '/foo/bar/file.txt'
    Extra parameters: 'method=raw'


## gitweb setup

gitweb is a perl-based web interface to git repositories.
It is part of the standard git source code.

Two Debian packages provide the 'gitweb' cgi:
`git` (in `/usr/share/gitweb/gitweb.cgi`)
and `gitweb` (in `/usr/lib/cgi-bin/gitweb.cgi`).

Install either of them with `apt-get install -yq gitweb git` .

#### Option 1: gitweb repositories as CGI paraemters

The following configuration is used on gnu savannah.

The URL for a specific repository includes the
repository name as a visible CGI parameter,
e.g. <http://server/gitweb/?p=sed.git>.

    location "/gitweb/static/" {
        # static files (png/css) served from /usr/share/gitweb/static
        root /usr/share/ ;
        expires 30d;
    }

    location /gitweb/ {
        fastcgi_param GITWEB_CONFIG    /etc/gitweb.conf;
        fastcgi_param SCRIPT_FILENAME  /usr/share/gitweb/gitweb.cgi;
        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }


#### option 2: gitweb repositories as path components

The following configuration allows repositories to
appear as part of the URL's path, e.g. <http://server/gitweb/sed.git>.

    location /gitweb/ {
        index gitweb.cgi
        fastcgi_param GITWEB_CONFIG  /etc/gitweb.conf;
        fastcgi_param DOCUMENT_ROOT  /usr/share/gitweb/;
        fastcgi_param SCRIPT_NAME    /gitweb.cgi$fastcgi_path_info;
        fastcgi_split_path_info      ^(/gitweb)(/?.+)$;

        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }

For this to work, add the following line to `/etc/gitweb.conf`:

    $feature{'pathinfo'}{'default'} = [1];


## cgit setup

[cgit](https://git.zx2c4.com/cgit/about/) is a fast web interface to
GIT repositories written in C.

See the <https://git.zx2c4.com/cgit/tree/README> file for installation
instructions (there is currently no debian package for it).

The build files are minimal. Assuming they were installed to `/opt/cgit`:

    $ cd /opt/cgit
    $ ls -lhog
    total 5.8M
    -rwxrwxr-x 1 5.7M Oct 29 19:51 cgit
    -rw-rw-r-- 1  13K Oct 29 19:51 cgit.css
    -rw-rw-r-- 1 1.4K Oct 29 19:51 cgit.png
    -rw-rw-r-- 1 1.1K Oct 29 19:51 favicon.ico
    -rw-rw-r-- 1   47 Oct 29 19:51 robots.txt

The following nginx configuration will work:

    location ~ "/cgit/cgit\.(png|css)$" {
            # Serve static files directly
            root /opt/ ;
            expires 30d;
    }

    location /cgit/ {
        fastcgi_param CGIT_CONFIG      /etc/cgitrc;
        fastcgi_param DOCUMENT_ROOT    /opt/cgit/;
        fastcgi_param SCRIPT_NAME      /cgit$fastcgi_path_info;
        fastcgi_split_path_info        ^(/cgit)(/?.+)$;
        include fastcgi_params;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
    }
