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
import re
import sys
import urllib.request
import tomllib
import socket
import multiprocessing
import typing


class Mainfunc(object):
    @staticmethod
    def getid_linux() -> str:
        if sys.platform != 'linux':
            return ''
        linuxid: str = ''
        fpath: str = '/etc/os-release'
        idrow: str = ''
        try:
            with open(fpath, 'rt') as fp:
                for row in fp:
                    if row.startswith('ID='):
                        idrow = row.rstrip()
                        break
        except:
            return ''
        if idrow == '':
            return ''
        s = idrow.removeprefix('ID')
        s = s.removeprefix('=')
        retid: str = s.strip()
        return retid

    @staticmethod
    def geturlpath_man(rootdic: dict, vernamekey: str) -> tuple[list, str, str, str, str]:
        mainfunc = Mainfunc
        errmes: str
        rettpl: tuple[list, str, str, str, str]
        reterr: tuple[list, str, str, str, str] = ([], '', '', '', '')
        if vernamekey == '@LATEST-RELEASE':
            timelist: list = list()
            for tpl in mainfunc.iter_rootdic(rootdic):
                vername, osname, status, thedate, urls = tpl
                t = time.strptime(thedate, '%Y%m%d-%H%M%S')
                epoch = int(time.mktime(t))
                timelist.append(
                    (epoch, urls, osname, status, thedate, vername))
            if len(timelist) == 0:
                errmes = 'Error: Unable to analyze root.toml.'
                print(errmes, file=sys.stderr)
                exit(1)
            timelist.append((10000, ['example.com'], 'Example OS', '', '', ''))
            timelist.sort(key=lambda x: x[0], reverse=True)
            rettpl = timelist[0][1:]
            return rettpl
        matched: bool = False
        for tpl in mainfunc.iter_rootdic(rootdic):
            vername, osname, status, thedate, urls = tpl
            if vername == vernamekey:
                matched = True
                break
        if matched == False:
            return reterr
        rettpl = (urls, osname, status, thedate, vernamekey)
        return rettpl

    @staticmethod
    def iter_rootdic(rootdic: dict):
        vername: str
        s: str
        osname: str
        status: str
        thedate: str
        urls: list = list()
        errmes: str
        chklist: list
        vname: str
        for vername, d in rootdic.items():
            if vername in ('baseurls', 'message'):
                continue
            if d.get('status') != 'release':
                continue  # Not 'release' status.
            if d.get('url') != None:
                s = d.get('url')
                if isinstance(s, str) != True:
                    errmes = 'Error: url value on root.toml is NOT string.'
                    print(errmes, file=sys.stderr)
                    exit(1)
                urls.append(s)
            osname = d.get('osname')
            status = d.get('status')
            thedate = d.get('thedate')
            if isinstance(d.get('urls'), list):
                urls.extend(d.get('urls'))
            chklist = [('osname', osname), ('status', status),
                       ('thedate', thedate)]
            for vname, v in chklist:
                if isinstance(v, str) != True:
                    errmes = 'Error: {0} on root.toml is NOT string.'.format(
                        vname)
                    print(errmes, file=sys.stderr)
                    exit(1)
            if isinstance(urls, list) != True:
                errmes = 'Error: urls on root.toml is NOT list type.'
                print(errmes, file=sys.stderr)
                exit(1)
            yield (vername, osname, status, thedate, urls)
        return

    @staticmethod
    def loadbytes_url(urlpath: str, exception: bool = True) -> bytes:
        html_content: bytes = b''
        if exception:
            try:
                with urllib.request.urlopen(urlpath) as response:
                    html_content = response.read()
            except urllib.error.URLError as e:
                errmes = 'Error: URL Error. {0}, URL: {1}'.format(e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            except urllib.error.HTTPError as e:
                errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            except Exception as e:
                errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(
                    e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            b: bytes = html_content
            return b
        else:
            try:
                with urllib.request.urlopen(urlpath) as response:
                    html_content = response.read()
            except:
                pass
            return html_content

    @staticmethod
    def loadstring_url(urlpath: str, exception: bool = True) -> str:
        html_content: str = ''
        if exception:
            try:
                with urllib.request.urlopen(urlpath) as response:
                    html_content = response.read().decode("utf-8")
            except urllib.error.URLError as e:
                errmes = 'Error: URL Error. {0}, URL: {1}'.format(e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            except urllib.error.HTTPError as e:
                errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
            except Exception as e:
                errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(
                    e, urlpath)
                print(errmes, file=sys.stderr)
                exit(1)
        else:
            try:
                with urllib.request.urlopen(urlpath) as response:
                    html_content = response.read().decode("utf-8")
            except:
                pass
        s = html_content
        return s

    @staticmethod
    def normurl(url: str) -> str:
        if '://' not in url:
            errmes = 'Error: Not url. [{0}]'.format(url)
            print(errmes, file=sys.stderr)
            exit(1)
        splitted = url.split('://', 1)
        ptn = r'/+'
        tail = re.sub(ptn, '/', splitted[1])
        retstr = splitted[0] + '://' + tail
        return retstr


class Cargo(object):
    @staticmethod
    def _is_resolvable_hostname_resolver(hostname: str, retqueue):
        ret: bool = False
        try:
            socket.getaddrinfo(hostname, None)
            ret = True
        except:
            pass
        retqueue.put(ret, timeout=1)
        return

    @staticmethod
    def is_resolvable_hostname(url: str, timeout=1) -> bool:
        subr = Cargo
        errmes: str = ''
        s: str = ''
        ptn: str = r'https\:\/\/[0-9a-zA-Z\.\_\-]+'
        reobj = re.match(ptn, url)
        if reobj == None:
            errmes = 'Error: url is https:// only. [{0}]'.format(url)
            raise ValueError(errmes)
        s = reobj.group() if reobj != None else ''  # type: ignore
        hostname: str = s.removeprefix('https://')
        retqueue: multiprocessing.queues.Queue = multiprocessing.Queue()
        func: typing.Callable = subr._is_resolvable_hostname_resolver
        pobj = multiprocessing.Process(target=func, args=(hostname, retqueue))
        pobj.start()
        resolvable: bool = False
        time_end: int = int(time.time()) + timeout
        while time_end >= int(time.time()):
            try:
                resolvable = retqueue.get_nowait()
            except:
                time.sleep(0.1)
                continue
            break
        if pobj.is_alive():
            pobj.terminate()
            time.sleep(0.1)
        pobj.close()
        return resolvable
