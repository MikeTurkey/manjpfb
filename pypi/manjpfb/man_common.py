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
import time
import sys
import urllib.request
import tomllib


class Mainfunc(object):
    @staticmethod
    def geturlpath_man(rootdic: dict, vernamekey: str) -> tuple:
        if vernamekey == '@LATEST-RELEASE':
            timelist = list()
            for vername, d in rootdic.items():
                if d.get('status') != 'release':
                    continue
                url = d.get('url')
                osname = d.get('osname')
                s = d.get('thedate')
                t = time.strptime(s, '%Y%m%d-%H%M%S')
                epoch = int(time.mktime(t))
                timelist.append((epoch, url, osname))
            if len(timelist) == 0:
                errmes = 'Error: Unable to analyze root.toml.'
                print(errmes, file=sys.stderr)
                exit(1)
            timelist.append((10000, 'example.com', 'Example OS'))
            timelist.sort(key=lambda x: x[0], reverse=True)
            return (timelist[0][1], timelist[0][2])
        rootvaluedic: dict = dict()
        for vername, d in rootdic.items():
            if vername == vernamekey:
                rootvaluedic = d
                break
        if len(rootvaluedic) == 0:
            errmes = 'Error: Not match the OS Version name key. [{0}]'.format(
                vernamekey)
            print(errmes, file=sys.stderr)
            exit(1)
        url = rootvaluedic.get('url', '')
        osname = rootvaluedic.get('osname', '')
        if url == '':
            errmes = 'Error: Not found url key.  [VERNAME: {0}]'.format(
                vernamekey)
            print(errmes, file=sys.stderr)
            exit(1)
        if osname == '':
            errmes = 'Error: Not found osname key.  [VERNAME: {0}]'.format(
                vernamekey)
            print(errmes, file=sys.stderr)
            exit(1)
        return (url, osname)

    @staticmethod
    def loadstring_url(urlpath: str) -> str:
        try:
            with urllib.request.urlopen(urlpath)as response:
                html_content = response.read().decode("utf-8")
        except urllib.error.URLError as e:
            print(f"URLエラーが発生しました: {e}")
            errmes = '  URL: {0}'.format(urlpath)
            print(errmes, file=sys.stderr)
        except urllib.error.HTTPError as e:
            print(f"HTTPエラーが発生しました: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
        s = html_content
        return s

    @staticmethod
    def normurl(url: str) -> str:
        if '://' not in url:
            errmes = 'Error: Not url. [{0}]'.format(url)
            print(errmes, file=sys.stderr)
            exit(1)
        splitted = url.split('://', 1)
        tail = os.path.normpath(splitted[1])
        retstr = splitted[0]+'://'+tail
        return retstr


class _Main_man(object):
    @staticmethod
    def show_listman(roottomlurl: str, vernamekey: str):
        mainfunc = Mainfunc
        rootstr = mainfunc.loadstring_url(roottomlurl)
        rootdic = tomllib.loads(rootstr)
        t = mainfunc.geturlpath_man(rootdic, vernamekey)
        tgturl, root_osname = t
        s = mainfunc.loadstring_url(tgturl)
        tomldic = tomllib.loads(s)

        def inloop(name: str) -> str:
            ptns = ('.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9')
            for ptn in ptns:
                if name.endswith(ptn):
                    return name.removesuffix(ptn)
            return name
        mannames = [inloop(name)for name, d in tomldic.items()
                    if isinstance(d, dict) == True]
        mannames.sort()
        for name in mannames:
            print(name)
        exit(0)

    @staticmethod
    def show_listos(roottomlurl: str):
        mainfunc = Mainfunc
        rootstr = mainfunc.loadstring_url(roottomlurl)
        rootdic = tomllib.loads(rootstr)
        osnames = [vv for k, v in rootdic.items()
                   for kk, vv in v.items()if kk == 'osname']


[print(s)for s in osnames]
exit(0)
