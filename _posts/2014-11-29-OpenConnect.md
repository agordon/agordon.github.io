---
title: "Begone AnyConnect, Welcome OpenConnect"
layout: post
date:   2014-11-29
---

# {{ page.title }}

## Introduction

Cisco AnyConnect is a VPN client used by many institutions.
It is the bad successor to the equally terrible
[Cisco Systems VPN Client](http://en.wikipedia.org/wiki/Cisco_Systems_VPN_Client).

A typical installation procedure goes something like
[this](http://oit.ncsu.edu/data-network/vpn-installation-instructions-windows),
[this](http://oit.ncsu.edu/data-network/vpn-installation-instructions-mac-os),
or [this](http://vpnhelp.olemiss.edu/).

It's not clear which component is worse (requiring Java, installing Active-X on
windows, or giving administrator access to a Cisco program) - but anyone who
suffered through the old Cisco VPN will likely be willing to go to great
lengths to avoid it.

Luckily, there's an easy and Free-Software alternative:
[OpenConnect](http://www.infradead.org/openconnect/).

## Installing OpenConnect

### GNU/Linux Debian/Ubuntu Installation

Install the following packages:

    sudo apt-get -y install openconnect vpnc

### GNU/Linux CentOS/Fedora/RedHat Installation

Install the following packages:

    sudo yum -y install openconnect vpnc

> NOTE:  
> If the packages are not found, you might need to add additional repositories
> as explained [here (fedora)](http://fedoraproject.org/wiki/EPEL/FAQ#How_can_I_install_the_packages_from_the_EPEL_software_repository.3F)
> or [here (CentOS)](http://wiki.centos.org/AdditionalResources/Repositories/RPMForge)

### Mac OS X with HomeBrew

Using HomeBrew, install these pacakges:

    brew install vpnc
    brew install --HEAD --with-gnutls openconnect

> NOTE:  
> At the time of this writing (Nov-2014), the OpenConnect version in HomeBrew
> is 6.0.0, which requires additional drivers (Tun/Tap drivers for Mac OS X).
> Using `--HEAD` will install a newer version than 6.0.0, which does not
> require any special drivers.

### GUI Installation

Some GNU/Linux ditributions provide GUI for OpenConnect VPN.
On Debian/Ubuntu, try installing the `network-manager-openconnect` package.

For more information, see <http://www.infradead.org/openconnect/packages.html>.

### Building for source code

For building instructions, see the OpenConnect website:
<http://www.infradead.org/openconnect/building.html>.

## Using OpenConnect

Open a terminal window, and run the following:

    sudo openconnect https://vpn.YOUR-INSTITUTE-HOST/

For example, the NYGC's VPN host is `https://vpn.nygenome.org`.

Once connected, you'll be asked for:

1. The **group**. This will typically be provided in the VPN instructions of your institute. It will also be shown on the terminal.
2. The **username**. You should know what your username is.
3. The **password**.

Example:

    $ sudo openconnect https://vpn.nygenome.org
    POST https://vpn.nygenome.org/
    Attempting to connect to server 162.220.30.20:443
    SSL negotiation with vpn.nygenome.org
    Connected to HTTPS on vpn.nygenome.org
    XML POST enabled
    Please enter your username and password.
    GROUP: [XXX|YYY]:                           #### Enter Group Name, press Enter
    POST https://vpn.nygenome.org/
    XML POST enabled
    Please enter your username and password.
    Username:                                   #### Enter Username, press Enter
    Password:                                   #### Enter Password, press Enter
    POST https://vpn.nygenome.org/
    Got CONNECT response: HTTP/1.1 200 OK
    CSTP connected. DPD 30, Keepalive 20
    Connected tun0 as 192.168.252.236, using SSL
    Established DTLS connection (using OpenSSL). Ciphersuite AES256-SHA.

The last message might show different technical parameters (e.g. Ciphersuites),
but as long as it says "Established connection" - you're connected to the VPN.

Keep the terminal open and the program running as long as you want to be connected.

When the program terminates, the VPN is disconnected.

For many more options, see the OpenConnect website:
<http://www.infradead.org/openconnect/>

## VPN Network connection

This section is informative - there is no need to run these commands in order
to connect to the VPN.

The following are examples of the network interface and configuration while
the VPN connection is active. The `utun`/`tun0` network interface is the VPN
connection interface. It will disappear once the VPN is disconnected.
The exact numbers will be different from system to system, YMMV.

On a typical GNU/Linux, the connection will look like this:

    $ ifconfig
    <...>
    tun0      Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
              inet addr:192.168.252.236  P-t-P:192.168.252.236  Mask:255.255.255.255
              UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1406  Metric:1
              RX packets:1 errors:0 dropped:0 overruns:0 frame:0
              TX packets:1 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:500
              RX bytes:67 (67.0 b)  TX bytes:67 (67.0 b)

On some GNU/Linux systems which do not have ifconfig (e.g. CentOS-7, RedHat-7) the connection will be:

    $ ip addr
    <...>
    3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1406 qdisc pfifo_fast state UNKNOWN qlen 500
       link/none
       inet 192.168.252.236/32 scope global tun0
         valid_lft forever preferred_lft forever

On Mac OS X with the built-in utun driver, the connection will look like this:

    $ /sbin/ifconfig
    <...>
    utun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1406
        inet 192.168.252.196 --> 192.168.252.196 netmask 0xffffffff

Routing table will be (on GNU/Linux):

    $ route
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    162-220-30-20.s 10.0.2.2        255.255.255.255 UGH   0      0        0 eth0
    nygdc01.nygenom *               255.255.255.255 UH    0      0        0 tun0
    nygdc02.nygenom *               255.255.255.255 UH    0      0        0 tun0
    10.0.2.0        *               255.255.255.0   U     0      0        0 eth0
    192.168.252.0   *               255.255.255.0   U     0      0        0 tun0
    192.168.253.0   *               255.255.255.0   U     0      0        0 tun0
    10.2.0.0        *               255.255.0.0     U     0      0        0 tun0
    10.3.0.0        *               255.255.0.0     U     0      0        0 tun0
    10.1.0.0        *               255.255.0.0     U     0      0        0 tun0
    172.16.0.0      *               255.255.0.0     U     0      0        0 tun0
    link-local      *               255.255.0.0     U     1002   0        0 eth0
    default         10.0.2.2        0.0.0.0         UG    0      0        0 eth0

hostname resolution is configured as such (on GNU/Linux):

    $ cat /etc/resolv.conf 
    #@VPNC_GENERATED@ -- this file is generated by vpnc
    # and will be overwritten by vpnc
    # as long as the above mark is intact
    ; generated by /sbin/dhclient-script
    nameserver 10.1.1.51
    nameserver 10.1.1.50
    search nygenome.org
