#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# manjpfb, FreeBSD Japanese-Man Pager.
# Copyright (C) 2024 MikeTurkey All rights reserved.
# contact: voice[ATmark]miketurkey.com
# license: GPLv3 License
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE
#
# In addition to the rights granted under the applicable license(GPL-3),
# you are expressly prohibited from using any form of machine learning,
# artificial intelligence, or similar technologies to analyze, process,
# or extract information from this software, or to create derivative
# works based on this software.
#
# This prohibition includes, but is not limited to, training machine
# learning models, neural networks, or any other automated systems using
# the code or output of this software.
#
# The purpose of this prohibition is to protect the integrity and
# intended use of this software. If you wish to use this software for
# machine learning or similar purposes, you must seek explicit written
# permission from the copyright holder.
#
# see also 
#     GPL-3 Licence: https://www.gnu.org/licenses/gpl-3.0.html.en
#     Mike Turkey.com: https://miketurkey.com/

import os
import sys
import tomllib
import types
import pydoc
if __name__ == '__main__':
    from man_common import Mainfunc, _Main_man
else:
    from .man_common import Mainfunc, _Main_man


class Main_manjpfb(object):
    version:     str = '0.0.2'
    versiondate: str = '30 Nov 2024'

    @staticmethod
    def show_version():
        version = Main_manjpfb.version
        versiondate = Main_manjpfb.versiondate
        meses = ['manjpfb written by MikeTurkey',
                 'ver {0}, {1}'.format(version, versiondate),
                 '2024 Copyright MikeTurkey ALL RIGHT RESEVED.',
                 'ABSOLUTELY NO WARRANTY.',
                 'Software: GPLv3 License including a prohibition clause for AI training.',
                 'Document: GFDL1.3 License including a prohibition clause for AI training.',
                 'FreeBSD man documents were translated by MikeTurkey using Deep-Learning.',
                 '',
                 'SYNOPSIS',
                 '  manjpfb [OPT] [mannum] [name]',
                 '',
                 'Summary',
                 '  FreeBSD Japanese-man Pager.',
                 '',
                 'Description',
                 '  jpmanf is pager of FreeBSD japanese man using python3.',
                 '  The program does not store man-data and download it with each request.',
                 '  Since it is a Python script, it is expected to run on many operating systems in the future.',
                 '  We can read the FreeBSD japanese man on many Operating Systems.',
                 '  There is man-data that is not fully translated, but this is currently by design.',
                 '  Please note that I do not take full responsibility for the translation of the documents.',
                 '',
                 'Example',
                 '  $ manjpfb ls',
                 '      print ls man.',
                 '  $ manjpfb 1 head',
                 '      print head 1 section man.',
                 '  $ manjpfb --version',
                 '      Show the message',
                 '  $ manjpfb --listman',
                 '      Show man page list.',
                 '  $ manjpfb --listos',
                 '      Show os name list of man.',
                 '']
        for s in meses:
            print(s)
        exit(0)

    def main(self):
        mainfunc = Mainfunc
        _main_man = _Main_man
        t = (104, 116, 116, 112, 115, 58, 47, 47, 109, 105, 107, 101,
             116, 117, 114, 107, 101, 121, 46, 99, 111, 109, 47, 106,
             112, 109, 97, 110, 102, 47, 100, 98, 47, 104, 97, 115,
             104, 47)
        baseurl = ''.join([chr(i) for i in t])
        t = (104, 116, 116, 112, 115, 58, 47, 47, 109, 105, 107, 101,
             116, 117, 114, 107, 101, 121, 46, 99, 111, 109, 47, 106,
             112, 109, 97, 110, 102, 47, 114, 111, 111, 116, 46, 116,
             111, 109, 108)
        roottomlurl = ''.join([chr(i) for i in t])
        opt = types.SimpleNamespace(manhashfpath='', mannum='', manname='',
                                    listos=False, listman=False, release='')
        arg1 = ''
        arg2 = ''
        on_manhash = False
        on_release = False
        for arg in sys.argv[1:]:
            if on_manhash:
                opt.manhashfpath = os.path.abspath(arg)
                on_manhash = False
                continue
            if on_release:
                opt.release = arg
                on_release = False
                continue
            if arg == '--manhash':
                on_manhash = True
                continue
            if arg == '--release':
                on_release = True
                continue
            if arg == '--version':
                self.show_version()
                exit(0)
            if arg == '--listos':
                opt.listos = True
                break
            if arg == '--listman':
                opt.listman = True
                break
            if arg1 == '':
                arg1 = arg
                continue
            if arg2 == '':
                arg2 = arg
                continue
            errmes = 'Error: Invalid args option. [{0}]'.format(arg)
            print(errmes, file=sys.stderr)
            exit(1)
        vernamekey = opt.release if opt.release != '' else '@LATEST-RELEASE'
        if opt.listos:
            _main_man.show_listos(roottomlurl)
            exit(0)
        if opt.listman:
            _main_man.show_listman(roottomlurl, vernamekey)
        if arg2 == '':
            opt.manname = arg1  # e.g. args: ls
        else:
            opt.mannum = arg1  # e.g. args: 1 ls
            opt.manname = arg2
        if opt.manhashfpath == '':
            rootstr = mainfunc.loadstring_url(roottomlurl)
            rootdic = tomllib.loads(rootstr)
            t = mainfunc.geturlpath_man(rootdic, vernamekey)
            tgturl, root_osname = t
            s = mainfunc.loadstring_url(tgturl)
            tomldic = tomllib.loads(s)
        else:
            with open(opt.manhashfpath, 'rb') as fp:
                tomldic = tomllib.load(fp)
        fnameurldic = dict()  # key: fname, value: urlpath
        tomldic_osname = 'None'
        for k, v in tomldic.items():
            if k == 'OSNAME':
                tomldic_osname = v
                continue
            fname = k
            hashdg = v['hash']
            s = baseurl + '/' + hashdg[0:2] + '/' + hashdg + '/' + fname
            tgturl = mainfunc.normurl(s)
            fnameurldic[fname] = tgturl
        if root_osname != tomldic_osname:
            errmes = 'Error: Mismatch OSNAME. [{0}, {1}]'.format(
                root_osname, tomldic_osname)
            print(errmes)
            exit(1)
        if opt.mannum != '':
            if opt.mannum not in '123456789':
                errmes = 'Error: Invalid man section number(1-9). [{0}]'.format(
                    opt.mannum)
                print(errmes, file=sys.stderr)
                exit(1)
            fnameurldictkeys = [opt.manname + '.' + opt.mannum]
        else:
            fnameurldictkeys = ['{0}.{1}'.format(
                opt.manname, i) for i in range(1, 10)]
        for fname in fnameurldictkeys:
            tgturl = fnameurldic.get(fname, '')
            if tgturl != '':
                break
        if tgturl == '':
            errmes = 'Error: Not found the manual name. [{0}]'.format(
                opt.manname)
            print(errmes, file=sys.stderr)
            exit(1)
        s = mainfunc.loadstring_url(tgturl)
        pydoc.pager(s)
        print('OSNAME(man):', root_osname)
        exit(0)


def main():
    cls = Main_manjpfb()
    cls.main()
    return


if __name__ == '__main__':
    main()
    exit(0)
