2.0.1 2019-08-25
---------------

- Python 3 tolerance
- move to github

2.0.0 2018-02-5
---------------

- Update to libcdio 2.0.0 API
- remove old compability code before 2.0.0
  We no longer support obsolte CD-Text interface
- Update Python packaging info

0.20 2013-09-6
--------------

- Bug fixes and update README.txt

0.19 2013-02-16
---------------

- Bug fixes for libcdio =< 0.82 versus libcdio >= 0.90
- Make this work on Python3

0.18 2013-01-07
----------------

- Adjust for libcdio 0.90

0.17 2010-10-27
---------------

- Minor instruction and bug fixes

0.16 2009-10-27 Halala ngosuku lokuzalwa
----------------------------------------

- Remove shbang from cdio.py and ios9660.py which helps Fedora packaging
- Off-by-one compensation in get_devices_* not needed anymore

0.15 2009-05-18
---------------

- Add Access to CDText thanks to Thomas Vander Stichele

0.14 2008-12-10
---------------

- Make more setuptools and distutils friendly. Small cleanups.

0.13 2007-10-27
---------------

- Small bugfix

0.12 2006-12-10
---------------

- Add get_msg()
- Add pathname_isofy() in iso9660.py
- Correct bugs in SWIG pathname_isofy() and close_tray()
- Correct bug in get_devices when there was only one device.

0.11 2006-03-27
---------------

- Add ISO 9660 library:
  * add example programs to extract a file from an ISO fileystem
  * add regression tsets
- Changes to make building outside of source tree (e.g. "make
  distcheck") work
- Include SWIG-derived files. In theory you don't need SWIG installed
  any more (although you do need a C compiler and libcdio installed).
- Remove bug in is_device()
- Fixes for Solaris and cygwin builds (compilation/linking flags)
- Minor SWIG changes to be more precise.

0.10 2006-01-30
---------------

Initial Python wrapper
