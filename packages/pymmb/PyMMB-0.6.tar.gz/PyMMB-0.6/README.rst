==============================================================
PyMMB - Python library to access BBC Microcomputer disc images
==============================================================

.. contents:: Table of Contents
   :depth: 2

Overview
--------

**PyMMB** is a python library to allow access to BBC Microcomputer DFS disc
images, and MMB disc image bundles.

History
-------

The BBC Microcomputer has been around for many years (over 30 years now),
and in all that time it has supported Tape, Floppy Disk, and occasionally
small Hard Disk Drive storage (If you have a 1770 and ADFS) but thanks to
the work of a number of enthusiasts there is now an inexpensive add-on to
allow any BBC Microcomputer (even those without Floppy Disk hardware) to
access mass storage on MMC Flash Cards.

This is wonderful but then poses a further problem, how to get the disk
images that the MMC/SuperMMC/TurboMMC hardware supports onto the flash card?

There are some tools which have been used for several years, they work ok,
as long as you are running a supported version of Windows (They don't work,
for example, under Wine or CrossoverOffice), but I've found them a little
confusing. The process to create an MMB, add a new disk and put files on it
is well documented but requires several steps and provides ample opportunity
for mistakes.

Details
-------

This is where PyMMB is intended to fit in. The aim of the project is to
provide a platform independant library, command-line toolset, GUI application
and FUSE binding for managing files stored on DFS disks, contained within
MMB files.

This package is the library providing all the functionality used by other
parts of the project. To make use of this library you should install one,
or more, of **PyMMBtools**, **PyMMBgui** or **PyMMBfuse**.

Requirements
------------

This package is written for Python 2.x (at least 2.5) and currently is not
supported under Python 3.x

Installation
------------

You can install PyMMB with your favourite egg installer. We recommend using
**pip** ::

  pip install PyMMB

Uninstall
---------

If you are using **pip** you can uninstall using ::

  pip uninstall PyMMB

Contributing
------------

Contributions of code, development time, testing, or money are welcome. If
you are kind enough to donate money, your name (and optionally company name,
and email or web address) will be listed as a sponsor.

You can join the project, see the current auto-build status, download the
code or browse the repository at http://projects.tlspu.com/PyMMB/

Please consider joining the PyMMB project before you fork. While you are
welcome to do either, joining us will help propell PyMMB forwards faster
the larger the contributor base becomes.

Sponsoring
----------

Development of this project is being sponsored by the following generous
individuals or organisations :

Credits
-------

    * Acorn Computers - For producing probably the most innovative computer
      for its time ever.

    * Martin Mather - For developing the original MMC Flash Card interface
      (and the MMB file format which bears his initials) for the BBC Micro.

    * Steve O'Leary - The code for FS Manager which helped me understand both
      MMB and DFS formats better.

