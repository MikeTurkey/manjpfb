
snakeland
********************************

 | snakeland created by MikeTurkey
 | Version 0.0.7, 14 Jan 2025
 | 2023-2025, COPYRIGHT MikeTurkey, All Right Reserved.
 | ABSOLUTELY NO WARRANTY. The Licence is based on GPLv3.
 | URL: https://miketurkey.com

Summary
=======

 Instant Python3 script installer.

Synopsis
========

 | snakeland \--version | \--help | \--license'
 | snakeland install-byconf [CONFIG]
 | snakeland uninstall [PKGNAME]
 | snakeland findpy3 [\--later 3.xx] | [\--older 3.xx] | \--latest | [\--range 3.xx-3.yy] | [\--order 3.x,..,3.yy]

QUICK START
--------------

 Install by config

 .. code-block:: console

   $ snakeland install-byconf snakeland-APP.conf
   $ APP --help 
     -- help message --

 Uninstall

 .. code-block:: console
		
   $ snakeland uninstall APP
   
 Find python3 command.

 .. code-block:: console

   $ snakeland findpy3 --later 3.8
     /usr/bin/python3.12
   $ snakeland findpy3 --older 3.11
     /usr/bin/python3.9
   $ snakeland findpy3 --latest
     /usr/bin/python3.12
   $ snakeland range 3.5-3.10
     /usr/bin/python3.9
   $ snakeland range --order 3.13,3.12,3.11,3.10,3.9
     /usr/bin/python3.12   
     
DESCRIPTION
------------

 | snakeland is instant python3 script installer.
 | The script wrapper is make on /usr/local/bin as cui command.

ARGUMENT
------------

  \--version, \--help, \--license

      | Print version, help message, license.

  \--latest

      | findpy3 sub command only
      | Print latest python3 command path.
	    
  \--later [PYTHONVERSION]

      | findpy3 sub command only
      | Print PYTHONVERSION later command path.

  \--older [PYTHONVERSION]

      | findpy3 sub command only
      | Print PYTHONVERSION older command path.

  \--range 3.xx-3.yy

      | findpy3 sub command only
      | Print latest python command path in 3.xx - 3.yy.

  \--order 3.x,...,3.yy

      | findpy3 sub command only
      | Print first matched python command path.

CONFIG
------------

  The Config is in restricted toml format.

  OSCHECK:  

      | Describe OS names. The string is similar to 'uname -s' cmd.
      | default section, optional key.
      | Darwin: Mac OS
      | Linux: Linux based OS
      | FreeBSD: FreeBSD OS
      | OpenBSD: OpenBSD
      | e.g.
      |   OSCHECK = ['Darwin', 'Linux', 'FreeBSD']

     
  DSTBASEDIR:

      | Destination Base Directory.
      | Recommend path is '/usr/local/libexec/CMDNAME'.
      | default section, essential key.

  INSTALLCMD:

      | Install command path. default path is '/usr/local/bin'.
      | default section, optional key.

  CMDNAME001-CMDNAME999:

      | The command name. The command file is made on INSTALLCMD directory.
      | default section, essential key.

  PY3TARGET001-PY3TARGET999:

      | The python3 script path. The script is executed by python3.xx cmd.
      | default section, optional key.
      | (Either of TARGETPY3, TARGETCMD is always required.)
      
  SRCMANFILES: Source Man files.

      | default section, optional key.
      | The pair of SRCMANFILES and DSTMANDIR work together to install the run directory.
      | Enable to set plain type and gz compress type.
      | snakeland install one of plain and gz compress file by the platform.
      | e.g.
      |   SRCMANFILES = ['man/snakeland.1.gz', 'man/snakeland.1']
 
  DSTMANDIR: Destination Man directory.

      | default section, optional key.
      | The pair of SRCMANFILES and DSTMANDIR work together to install the run directory.
      | e.g.
      |   DSTMANDIR = '/usr/local/share/man/man1'
      
  SHEBANG:

      | The shebang of CMDNAME file. default path is '/bin/sh'.
      | default section, optional key.

  PY3VERSION:

      | Execute python3 of the version.
      | The string is similar to 'findpy3' options.
      | default section, optional key.
      
        | '3.x later'  : python 3.x later.
        | '3.x older'  : python 3.x older.
        | 'latest'     : Latest python3 
        | '3.xx - 3.yy': Latest python3 in 3.xx - 3.yy.
        | '3.6 3.7 3.8': First found python3 in 3.6, 3.7, 3.8.
   
  DSTDIR:

      | Relative path of DSTBASEDIR.
      | You cannot set it to a directory above the DSTBASEDIR.
      | source file section, essential key.
	 
  FMODE:

      | File mode of the section file. default mode is 644.
      | source file section, optional key.

  Example of config

      .. code-block:: text

	 DSTBASEDIR = '/usr/local/libexec/CMDNAMEAPP/'
	 PKGNAME    = 'CMDNAMEAPP'
	 CMDNAME001   = 'CMDNAMEAPP'
	 PY3TARGET001 = '/usr/local/libexec/CMDNAMEAPP/CMDNAMEAPP.py'

	 [script/CMDNAMEAPP.py]
             DSTDIR = '.'

BUGS
------

  | Please report bugs to the issue tracker:
  | https://github.com/MikeTurkey/snakeland/issues
  | or by e-mail: <voice[ATmark]miketurkey.com>

Author
--------

  MikeTurkey <voice[ATmark]miketurkey.com>

LICENSE
----------

  GPLv3 License including a prohibition clause for AI training.


COPYRIGHT
-------------
  
  | 2023-2025, COPYRIGHT MikeTurkey, All Right Reserved.
  | ABSOLUTELY NO WARRANTY.
  | Document: GFDL1.3 License including a prohibition clause for AI training.
  | URL: https://miketurkey.com

