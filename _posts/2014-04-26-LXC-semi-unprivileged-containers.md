---
title: "Semi-Unprivileged Linux Containers (LXC) on Debian 7 Stable."
layout: post
date:   2014-04-26 13:50:13
---

# {{ page.title }}

This short tutorial shows how to setup Linux Container with Semi-Unprivileged Containers on Debian 7.

This tutorial provides the following *Semi-Unprivileged* setup:

- Creating and Starting containers, still requires `sudo`.
- Inside a container:
    - The guest 'root' user mapped to a non-root host user.
    - Optional guest non-root user mapped to a different non-root host user.
- Not covered here:
    - Creating and Starting containers as non-root
    - Mapping range of users

This tutorial uses Debian 7.4 Stable, but any reasonable Linux distribution with Linux Kernel 3.12 or later should work.

## Background

Linux Containers are the new black in virtualization,
But security concerns still hinder adoption.

A recently added feature called 'Unprivileged Containers' enables running a container
with root-guest user mapped to non-root host user - resolving *some* of the security concerns.

The official support is currently for Ubuntu 14.04 LTS, and requires several patches. With this tutorial you'll be able to use unprivileged containers with stock Debian 7 (and other Linux distributions).

## Step 1 - Install Debian 7 Stable ("Wheezy")

Install Debian 7.4 "Wheezy". Instructions are beyond the scope of this document,
but are easy to find. Start here: <https://www.debian.org/distrib/> .

If you want to experiment with this tutorial on "the cloud", note the followings:

### Amazon Cloud

- Start with a Stock Debian 7.4 Image, listed here: <https://wiki.debian.org/Cloud/AmazonEC2Image/Wheezy> (e.g. for
US-East-1, 64bit, Para-Virtualized, use `ami-b7c8d5de`).
- When creating the new instance, choose a **custom kernel image** from the **advanced options** list,
and choose **PV-GRUB hd0-1.0.4 64bit** with ID **aki-919dcaf8**.
- The reason: Sometime between kernel 3.2 and kernel 3.9. the compression format of the `initrd` image file
was changed from gzip to xz. Debian 7.4 with Kernel 3.2 has the (old) gzip format, and boots just fine with
the old stock GRUB loader amazon provides by default.
- Once we upgrade to kernel 3.12 (see next section), the new `initrd` file will use xz compression,
and the Amazon instance WILL NOT REBOOT properly.
- Failing to use the new grub bootloader, the instance will not boot, and the system log will show something like:

        ERROR Invalid kernel: xc_dom_probe_bzimage_kernel: unknown compression format
        xc_dom_bzimageloader.c:394: panic: xc_dom_probe_bzimage_kernel: unknown compression format

- For the gory details, read this: <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/UserProvidedKernels.html>

### Digital Ocean

- DigitalOcean's stock Debian 7 image is perfect for this tutorial.
- The Droplet boots with Debian's linx kernel version 3.2.
- DigitalOcean Droplets' kernels are controlled by DigitalOcean - meaning just installing a
new kernel and rebooting will not suffice.
- After upgrading the kernel (as described below in step #2) - you **must** contact
DigitalOcean's support team (by opening a ticket), and ask them to use the newly installed kernel file.
- DigitalOcean's support team is very fast and efficient (my personal anecdotal experience) - it usually takes them less than 3 minutes to respond, and upgrading + rebooting took another minute.
- When opening a support request ticket, tell them the following:

        I would like to upgrade a kernel on my droplet [DROPLET NAME/IP].
        The new kernel is a standard image from Debian-Backports,
        named '3.12-0.bpo.1-amd64', and is installed in '/lib/modules'.

- They will powerdown the droplet, setup the new kernel, and reboot it for you.


## Step 2 - Upgrade to kernel 3.12 with Debian Backports

This is the only *not-so-stable* requirement: for [Linux Kernel User Namespace Support](http://lwn.net/Articles/532593/),
you'll need at least version 3.8. Version 3.12 is provided with [Debian Backports](http://backports.debian.org/), and avoids the need for a messy manual kernel compliation.

Once you booted and accessed the new Debian installation, run the following commands. These would add Debian Backports mirror as a source for packages, and install the new Kernel, including add the required setup (e.g. updating the Grub Menu):

```sh
echo "deb http://mirror.us.leaseweb.net/debian/ wheezy-backports main" | \
    sudo tee /etc/apt/sources.list.d/backports.list
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get -t wheezy-backports -y install linux-image-3.12-0.bpo.1-amd64
```

This is a good place to remind you - **never** perform these experiments on production systems, or even on partially important machine. If something went wrong and the machine doesn't reboot, it's easier to just kill it and start fresh - only if it's a test machine.

Before rebooting, ensure the machine is properly configured to use the new kernel. If using a local/physical machine, update the bootloader (e.g. 'grub'). If using a virtual machine on 'the cloud', see notes in step #1 above. When ready, reboot the machine.

## Step 3 - Verify User Namespace support

Once booted, verify the required support with the following commands. First, ensure the machine booted with the correct kernel version:

```sh
$ uname -r
3.12-0.bpo.1-amd64
```

Then, ensure the kernel supports user-namespace mapping. One indication is that each process will have two additional entries in its `/proc` directory:

```sh
$ cat /proc/1/{g,u}id_map
         0          0 4294967295
         0          0 4294967295
```

If either of these commands failed, go back and trouble-shoot the kernel upgrade.

## Step 4 - Prerequisites Setup

Few standard items must be configured on the host Debian machine.

Mount [cgroups](http://www.linux.com/news/featured-blogs/200-libby-clark/733595-all-about-the-linux-kernel-cgroups-redesign), by running the following commands:

```sh
$ echo "cgroup  /sys/fs/cgroup  cgroup  defaults  0   0" | sudo tee -a /etc/fstab
$ sudo mount /sys/fs/cgroup
```

Install few required programs:

```sh
$ sudo apt-get install -y libcap-dev build-essential wget
```

Install the latest [Linux Containers](https://linuxcontainers.org/downloads/) (version 1.0.3 at the time of this writing):

```sh
wget https://linuxcontainers.org/downloads/lxc-1.0.3.tar.gz
tar -xf lxc-1.0.3.tar.gz
cd lxc-1.0.3
./configure
make -j
sudo make install
cd
```

Install a *static* version of busybox, which we'll use for the container's demonstration:

```sh
wget http://busybox.net/downloads/busybox-1.22.1.tar.bz2
tar -xf busybox-1.22.1.tar.bz2
cd busybox-1.22.1
# Default Busybox configration is fine for this demo
make defconfig
# Exacpt one item: make it a static executable
sed -i '/CONFIG_STATIC/s/.*/CONFIG_STATIC=y/' .config
make -j
sudo cp busybox /usr/local/bin/busybox
```

**Note:** The above steps are suitable for this experimental setup. On a production machine you want proper installation paths, etc.

## Step 5 - Create and Test Privileged Containers

Before trying unprivileged containers, verify the default containers work as expected.

Create a new minimal conainer, using BusyBox template:

```sh
$ sudo lxc-create --template busybox --name test1
setting root password to "root"
Password for 'root' changed
```

Start the container, and run a simple command `sleep 60` (Ignore the `udhcpc` error - The BusyBox template starts dhcp by default, but does not have any network configured. To supress this warning, comment out the `/bin/udhcpc` line in the container's `./rootfs/etc/init.d/rcS` file):

```sh
$ sudo lxc-start --name test1
udhcpc: SIOCGIFINDEX: No such device

Please press Enter to activate this console.
/ # sleep 60
```

Back on the host machine (open a new console), see that the 'sleep' command inside the container
is run by the root user (which is the root on both the host and the container/guest):

```sh
# (Run On the host - numeric values will differ)
$ ps -H axo user,pid,comm | grep -B 6 sleep
root     20263   sudo lxc-start --name test1
root     20264     lxc-start --name test1
root     20266       init
root     20270         /bin/syslogd
root     20275         /bin/getty -L tty1 115200 vt100
root     20276         /bin/sh
root     20300           sleep 60
```

Notice how all the processes (`lxc-start` on the host, and `syslogd`, `getty`, `sh`, and `sleep` on the guest) are all
owned by user `root`.

On the host, stop the container:

```sh
$ sudo lxc-stop --name test1
```

On the guest console, you will see:

```
The system is going down NOW!
Sent SIGTERM to all processes
Terminated
Sent SIGKILL to all processes
Requesting system halt
```

Depending on your system's configuration, shutting down the container might take
few seconds, due to Busybox's handling of the shutdown procedure.

If all the above steps worked as expected, Linux Containers (with the default privileged containers) are properly installed.


## Step 6 - Prepare LXC for Semi-Privileged usage

On the host machine, create two non-root users. which will be mapped to the guest's root user and non-root users:

```sh
sudo adduser --quiet --uid 2001 --disabled-login --no-create-home lxc_root
sudo adduser --quiet --uid 2002 --disabled-login --no-create-home lxc_user
```

2. On the host machine, change ownership of few critical files.
For the purpose of this demonstation, the ownership modifications are sufficient.
For a production machine, further consideration must be made.

```sh
# The exact PATH depents on the name of the LXC (test1 in this tutorial)
$ cd /usr/local/var/lib/lxc/test1/
$ sudo mkdir ./rootfs/lxc_putold
$ sudo chown -R lxc_root:lxc_root ./rootfs/etc
```

On the host machine, add the following configuration items to the `config` file.

```
# The file is /usr/local/var/lib/lxc/test1/config

# In the BusyBox template, the following line is uncommented,
# COMMENT it (to disable it).
# lxc.pts = 1

lxc.kmsg = 0

# map Guest user 0 (root) to Host user 2001 (lxc_root)
lxc.id_map = u 0 2001 1
lxc.id_map = g 0 2001 1

# map guest user 1000 (see below) to host user 2002 (lxc_user)
lxc.id_map = u 1000 2002 1
lxc.id_map = g 1000 2002 1
```

Start the guest container, and run a test command (as the guest's root user):

```sh
$ sudo lxc-start --name test1
udhcpc: SIOCGIFINDEX: No such device

Please press Enter to activate this console.
# id
uid=0(root) gid=0(root)
# sleep 88
```

On the host, examine the user runnning the `sleep` command:

```sh
$ ps -H axo user,pid,comm | grep -B 7 sleep
admin    20281  bash
root     20374   sudo lxc-start --name test1
root     20375     lxc-start --name test1
lxc_root 20377       init
lxc_root 20384         /bin/getty -L tty1 115200 vt100
lxc_root 20385         /bin/sh
lxc_root 20391           sleep 88
```

The real user on the host is `lxc_root`, and it is a non-root user.

Inside the guest container, create a non-root user:

```sh
# adduser -u 1000 user
Changing password for user
New password:
Bad password: too short
Retype password:
Password for user changed by root

# su -l user
~ $ pwd
/home/user
~ $ id
uid=1000(user) gid=1000(user) groups=1000(user)
~ $ sleep 99
```

Back on the host, examine the user running the `sleep` command:

```sh
$ ps -H axo user,pid,comm | grep -B 7 sleep
admin    20281  bash
root     20374   sudo lxc-start --name test1
root     20375     lxc-start --name test1
lxc_root 20377       init
lxc_root 20384         /bin/getty -L tty1 115200 vt100
lxc_root 20385         /bin/sh
lxc_user 20422           -sh
lxc_user 20424             sleep 99
```

## Further Information

- Linux Containers Web Size: <https://linuxcontainers.org/news/>
- GitHub Repository: <https://github.com/lxc/lxc/>
- Linux Containers tutorials (10 parts series): <https://www.stgraber.org/2013/12/20/lxc-1-0-blog-post-series/>
    - Part #7: Unprivileged Containers: <https://www.stgraber.org/2014/01/17/lxc-1-0-unprivileged-containers/>
- Linux Containers Security (WARNING: some information might be outdated)
    - <http://www.slideshare.net/jpetazzo/linux-containers-lxc-docker-and-security>
    - <http://blog.docker.io/2013/08/containers-docker-how-secure-are-they/>

## Updates & Corrections

2014-04-29: Updated dhcp/shutdown information based on [Rami Rosen's comments](https://lists.linuxcontainers.org/pipermail/lxc-users/2014-April/006640.html)
