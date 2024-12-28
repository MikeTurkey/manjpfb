..
  Copyright 2024 Mike Turkey
  FreeBSD man documents were translated by MikeTurkey using Deep-Learning.
  contact: voice[ATmark]miketurkey.com
  license: GFDL1.3 License including a prohibition clause for AI training.
  
  Permission is granted to copy, distribute and/or modify this document
  under the terms of the GNU Free Documentation License, Version 1.3
  or any later version published by the Free Software Foundation;
  with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
  A copy of the license is included in the section entitled "GNU
  Free Documentation License".
  See also
    GFDL1.3: https://www.gnu.org/licenses/fdl-1.3.txt
    Mike Turkey: https://miketurkey.com/
..

=================================
manjpfb
=================================

  |  manjpfb created by MikeTurkey
  |  Version 0.0.7, 28 Dec 2024
  |  2024, COPYRIGHT MikeTurkey, All Right Reserved.
  |  ABSOLUTELY NO WARRANTY.
  |  GPLv3 License including a prohibition clause for AI training.

要約
---------------------------------

  FreeBSD 日本語マニュアルページャー


概要
---------------------------------

  manjpfbはpython3で動作するFreeBSD日本語マニュアルページャーです。
  このプログラムはデータを保存せず、その都度ごとにダウンロードをします。
  pythonスクリプトで動作していることから、将来的には多くのOSで動作すれば良いと考えています。
  多くのオペレーティングシステムでFreeBSD日本語マニュアルを読めるようになります。
  FreeBSD日本語マニュアルの中には完全に翻訳されていないものがありますが、現在のところ仕様です。
  ドキュメントの翻訳に全ての責任を負わないことに注意してください。

SUMMARY
---------------------------------

  FreeBSD Japanese-Man Pager.

SYNOPSIS
--------------------------------

  | manjpfb [ \--version | \--help ]
  | manjpfb [ \--listos | \--listman]
  | manjpfb [MANNUM] [MANNAME]

QUICK START
--------------------------------

Run on python pypi.

.. code-block:: console

  $ python3.xx -m pip install manjpfb
  $ python3.xx -m manjpfb man 


DESCRIPTION
--------------------------------

  manjpfb is pager of FreeBSD Japanese man using Python3.
  The program does not store man-data and download it with each request.
  Since it is a Python script, it is expected to run on many Operating Systems in the future.
  We can read the FreeBSD Japanese man on many Operating Systems.
  There is man-data that is not fully translated, but this is currently by design.
  Please note that I do not take full responsibility for the translation of the documents.

OPTIONS
-------------------------------

| \--version

  |   Show version.

| \--help

  |   Show help messages.
  
| \--showtmpdir

  |   Print temporary(cache) directory.

| \--listos

  |   Show the FreeBSD version name list of the manual.
  |   e.g. FreeBSD 13.2-Release

| \--listman

  |   Show the man list of the FreeBSD.
  |   e.g. ls, cp, rm, mv ... 

| \--listman1

  |   Show the man 1 list of the FreeBSD.
  |   man 1: General Commands Manual

| \--listman2

  |   Show the man 2 list of the FreeBSD.
  |   man 2: System Calls Manual

| \--listman3

  |   Show the man 3 list of the FreeBSD.
  |   man 3: Library Functions Manual

| \--listman4

  |   Show the man 4 list of the FreeBSD.
  |   man 4: Kernel Interfaces Manual

| \--listman5

  |   Show the man 5 list of the FreeBSD.
  |   man 5: File Formats Manual

| \--listman6

  |   Show the man 6 list of the FreeBSD.
  |   man 6: Games Manual

| \--listman7

  |   Show the man 7 list of the FreeBSD.
  |   man 7: Miscellaneous Information Manual

| \--listman8

  |   Show the man 8 list of the FreeBSD.
  |   man 8: System Manager's Manual

| \--listman9

  |   Show the man 9 list of the FreeBSD.
  |   man 9: Kernel Developer's Manual


EXAMPLE
--------------------------------

.. code-block:: console
		
  $ manjpfb ls
      print ls man.
  $ manjpfb 1 head
      print head 1 section man.
  $ manjpfb --version
      Show the message
  $ manjpfb --listman
      Show man page list.
  $ manjpfb --listos
      Show os name list of man.


BUGS
------

  | Please report bugs to the issue tracker: https://github.com/MikeTurkey/mman/issues
  | or by e-mail: <voice[ATmark]miketurkey.com>
   
AUTHOR
------

  MikeTurkey <voice[ATmark]miketurkey.com>

LICENSE
----------

  GPLv3 License including a prohibition clause for AI training.

