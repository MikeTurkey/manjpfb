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
import pathlib
import tempfile
import shutil
import hashlib
import gzip


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


class Man_cache(object):
    _suffix_cmdnames: typing.Final[dict] = \
        {('fb', 'eng', 'arm64'): 'enfb', ('fb', 'jpn', 'arm64'): 'jpfb',
         ('ob', 'eng', 'arm64'): 'enob'}

    def __init__(self):
        self._og_os2: str = ''
        self._og_lang: str = ''
        self._og_arch: str = ''
        self._hashdg_roottoml: str = ''
        self._hashdg_mantoml: str = ''
        self._platform: str = sys.platform
        self._suffix_cmdname: str = ''
        self._tmpdir: pathlib.Path = pathlib.Path('')
        return

    @property
    def og_os2(self):
        return self._og_os2

    @property
    def og_lang(self):
        return self._og_lang

    @property
    def og_arch(self):
        return self._og_arch

    @property
    def hashdg_roottoml(self):
        return self._hashdg_roottoml

    @property
    def hashdg_mantoml(self):
        return self._hashdg_mantoml

    @property
    def platform(self):
        return self._platform

    @property
    def suffix_cmdname(self):
        return self._suffix_cmdname

    @property
    def tmpdir(self):
        return self._tmpdir

    def _makefpath_tmpdir(self) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path | None]:
        systemtmpdir: typing.Final[str] = tempfile.gettempdir()
        date: typing.Final[str] = time.strftime('%Y%m%d', time.localtime())
        tuplekey: typing.Final[tuple] = (
            self.og_os2, self.og_lang, self.og_arch)
        suffix_cmdname: typing.Final[str] = self._suffix_cmdnames.get(
            tuplekey, '')
        tmpdir: pathlib.Path
        tmpdir1st: pathlib.Path
        tmpdir2nd: pathlib.Path | None
        s: str = ''
        if self.platform != 'win32':
            uid: typing.Final[str] = str(os.getuid())
            if suffix_cmdname == '':
                errmes = 'Error: Unknown _suffix_cmdnames key. [{0}]'.format(
                    tuplekey)
                print(errmes, file=sys.stderr)
                exit(1)
            s = '/mman_{0}/{1}/man{2}'.format(date, uid, suffix_cmdname)
            tmpdir = pathlib.Path(os.path.abspath(systemtmpdir + s))
            s = '/mman_{0}'.format(date)
            tmpdir1st = pathlib.Path(os.path.abspath(systemtmpdir + s))
            s = '/mman_{0}/{1}/'.format(date, uid)
            tmpdir2nd = pathlib.Path(os.path.abspath(systemtmpdir + s))
        elif self.platform == 'win32':
            if suffix_cmdname == '':
                errmes = 'Error: Unknown _suffix_cmdnames key. [{0}]'.format(
                    tuplekey)
                print(errmes, file=sys.stderr)
                exit(1)
            s = '\\mman_{0}\\man{1}'.format(date, suffix_cmdname)
            tmpdir = pathlib.Path(os.path.abspath(systemtmpdir + s))
            s = '\\mman_{0}'.format(date)
            tmpdir1st = pathlib.Path(os.path.abspath(systemtmpdir + s))
            tmpdir2nd = None
        return (tmpdir, tmpdir1st, tmpdir2nd)

    def init(self, os2: str, lang: str, arch: str):
        errmes: str = ''
        t: tuple = (os2, lang, arch)
        s: str = self._suffix_cmdnames.get(t, '')
        if s == '':
            errmes = 'Error: Not _suffix_cmdnames dict key. [{0}]'.format(t)
            print(errmes, file=sys.stderr)
            exit(1)
        self._suffix_cmdname = s
        self._og_os2 = os2
        self._og_lang = lang
        self._og_arch = arch
        t = self._makefpath_tmpdir()
        self._tmpdir = t[0]
        return

    def mktempdir_ifnot(self):
        errmes: str = ''
        t: tuple = self._makefpath_tmpdir()
        tmpdir: typing.Final[pathlib.Path] = t[0]
        tmpdir1st: typing.Final[pathlib.Path] = t[1]
        tmpdir2nd: typing.Final = t[2]
        pathlib.Path(tmpdir1st).mkdir(exist_ok=True)
        if tmpdir2nd != None:
            pathlib.Path(tmpdir2nd).mkdir(exist_ok=True)
        pathlib.Path(tmpdir).mkdir(exist_ok=True)
        if self.platform != 'win32':
            newstmode: int = 0
            dpath: str = ''
            dpath = str(tmpdir1st)
            newstmode = os.stat(dpath).st_mode | 0o1000
            os.chmod(dpath, newstmode)
            dpath = str(tmpdir2nd)
            newstmode = os.stat(dpath).st_mode | 0o1000
            os.chmod(dpath, newstmode)
            dpath = str(tmpdir)
            newstmode = os.stat(dpath).st_mode | 0o1000
            os.chmod(dpath, newstmode)
        self._tmpdir = tmpdir
        self._tmpdir1st = tmpdir1st
        self._tmpdir2nd = pathlib.Path(
            '') if self.platform == 'win32' else tmpdir2nd
        return

    def remove_oldcache(self):
        s: str = ''
        errmes: str = ''
        systemtmpdir: typing.Final[pathlib.Path] = pathlib.Path(
            tempfile.gettempdir())
        date: typing.Final[str] = time.strftime('%Y%m%d', time.localtime())
        s = 'mman_{0}'.format(date)
        nowtmpdir: typing.Final[pathlib.Path] = systemtmpdir / s
        ptn: str = r'mman\_2[0-9]{3}[01][0-9][0-3][0-9]'
        recpl = re.compile(ptn)
        for f in pathlib.Path(systemtmpdir).glob('*'):
            if f.is_dir() != True:
                continue
            if f == nowtmpdir:
                continue
            s = str(f.relative_to(systemtmpdir))
            if recpl.match(s) == None:
                continue
            shutil.rmtree(f)
        return

    def store_roottoml(self, hit: bool, gzbys: bytes):
        if hit:
            return
        errmes: str = ''
        chklist: list = [(hit, 'hit', bool), (gzbys, 'gzbys', bytes)]
        for v, vname, vtype in chklist:
            if isinstance(v, vtype) != True:
                errmes = 'Error: {0} is NOT {1} type'.format(
                    vname, repr(vtype))
                raise TypeError(errmes)
        fpath: pathlib.PosixPath | pathlib.WindowsPath
        fpath = self.tmpdir / 'root.toml.gz'
        with open(str(fpath), 'wb') as fp:
            fp.write(gzbys)
        return

    def get_roottoml(self, hashdg: str) -> tuple[bool, str]:
        ptn: str = r'[0-9a-f]{64}'
        errmes: str = ''
        if re.fullmatch(ptn, hashdg) == None:
            errmes = 'Error: Not hashdg string. [{0}]'.format(hashdg)
            print(errmes, file=sys.stderr)
            exit(1)
        if self.tmpdir.is_dir() != True:
            errmes = 'Error: Not found cache directory. [{0}]'.format(
                self.tmpdir)
            print(errmes, file=sys.stderr)
            exit(1)
        fpath: pathlib.PosixPath | pathlib.WindowsPath
        fpath = self.tmpdir / 'root.toml.gz'
        if fpath.is_file() != True:
            return False, ''
        hobj: typing.Final = hashlib.new('SHA3-256')
        try:
            with open(fpath, 'rb') as fp:
                gzbys: typing.Final[bytes] = fp.read()
        except:
            errmes = 'Error: root.toml.gz cache file open error. [{0}]'.format(
                fpath)
            print(errmes, file=sys.stderr)
            exit(1)
        hobj.update(gzbys)
        hashdg_body: str = hobj.hexdigest()
        if hashdg_body != hashdg:
            return False, ''
        rootbys: bytes = gzip.decompress(gzbys)
        rootstr: str = rootbys.decode('UTF-8')
        return True, rootstr

    def store_mantoml(self, hit: bool, url: str, gzbys: bytes):
        if hit:
            return
        errmes: str = ''
        chklist: list = [(hit, 'hit', bool), (url, 'url',
                                              str), (gzbys, 'gzbys', bytes)]
        for v, vname, vtype in chklist:
            if isinstance(v, vtype) != True:
                errmes = 'Error: {0} is NOT {1} type'.format(
                    vname, repr(vtype))
                raise TypeError(errmes)
        splitted: list = url.rsplit('/', 1)
        if len(splitted) != 2:
            errmes = 'Error: Not url format. [{0}]'.format(url)
            print(errmes, file=sys.stderr)
            exit(1)
        fname: str = splitted[1]
        ptn: str = r'man.+(?:amd64|arm64)_hash_2[0-9]{3}[0-1][0-9][0-3][0-9]\.toml\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not man.toml.gz format. [{0}]'.format(fname)
            print(errmes, file=sys.stderr)
            exit(1)
        fpath: pathlib.PosixPath | pathlib.WindowsPath
        fpath = self.tmpdir / fname
        with open(str(fpath), 'wb') as fp:
            fp.write(gzbys)
        return

    def get_mantoml(self, url: str, hashdg: str) -> tuple[bool, str]:
        ptn: str = r'[0-9a-f]{64}'
        errmes: str = ''
        if re.fullmatch(ptn, hashdg) == None:
            errmes = 'Error: Not hashdg string. [{0}]'.format(hashdg)
            print(errmes, file=sys.stderr)
            exit(1)
        if self.tmpdir.is_dir() != True:
            errmes = 'Error: Not found cache directory. [{0}]'.format(
                self.tmpdir)
            print(errmes, file=sys.stderr)
            exit(1)
        splitted: list = url.rsplit('/', 1)
        if len(splitted) != 2:
            errmes = 'Error: Not url format. [{0}]'.format(url)
            print(errmes, file=sys.stderr)
            exit(1)
        fname: str = splitted[1]
        ptn = r'man.+(?:amd64|arm64)_hash_2[0-9]{3}[0-1][0-9][0-3][0-9]\.toml\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not man.toml.gz format. [{0}]'.format(fname)
            print(errmes, file=sys.stderr)
            exit(1)
        fpath: pathlib.PosixPath | pathlib.WindowsPath
        fpath = self.tmpdir / fname
        if fpath.is_file() != True:
            return False, ''
        hobj: typing.Final = hashlib.new('SHA3-256')
        try:
            with open(fpath, 'rb') as fp:
                gzbys: typing.Final[bytes] = fp.read()
        except:
            errmes = 'Error: man.toml.gz cache file open error. [{0}]'.format(
                fpath)
            print(errmes, file=sys.stderr)
            exit(1)
        hobj.update(gzbys)
        hashdg_body: str = hobj.hexdigest()
        if hashdg_body != hashdg:
            return False, ''
        mantomlbys: bytes = gzip.decompress(gzbys)
        mantomlstr: str = mantomlbys.decode('UTF-8')
        return True, mantomlstr


class Man_pagercache(object):
    def __init__(self):
        self._tmpdir: pathlib.Path = pathlib.Path('.')
        return

    @property
    def tmpdir(self):
        return self._tmpdir

    def init(self, tmpdir: pathlib.Path):
        errmes = ''
        if isinstance(tmpdir, pathlib.PosixPath) != True and isinstance(tmpdir, pathlib.WindowsPath) != True:
            errmes = 'Error: tmpdir is NOT PosixPath or WindowsPath object.'
            raise TypeError(errmes)
        self._tmpdir = tmpdir
        return

    def get_pager(self, url: str) -> tuple[bool, str]:
        errmes: str = ''
        if isinstance(url, str) != True:
            errmes = 'Error: url is not string type.'
            print(errmes, file=sys.stderr)
            exit(1)
        if self.tmpdir.is_dir() != True:
            errmes = 'Error: Not found cache directory. [{0}]'.format(
                self.tmpdir)
            print(errmes, file=sys.stderr)
            exit(1)
        splitted: list = url.rsplit('/', 2)
        if len(splitted) != 3:
            errmes = 'Error: Not url format. [{0}]'.format(url)
            print(errmes, file=sys.stderr)
            exit(1)
        fname: str = splitted[2]
        hashdg: str = splitted[1]
        ptn: str = r'[0-9a-f]{64}$'
        if re.match(ptn, hashdg) == None:
            errmes = 'Error: Not hash digest format. [{0}]'.format(hashdg)
            print(errmes, file=sys.stderr)
            exit(1)
        ptn = r'[0-9a-f]{6}\.[1-9a-z]\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not pager file format. [{0}]'.format(fname)
            print(errmes, file=sys.stderr)
            exit(1)
        fpath: pathlib.PosixPath | pathlib.WindowsPath
        fpath = self.tmpdir / fname
        if fpath.is_file() != True:
            return False, ''
        hobj: typing.Final = hashlib.new('SHA3-256')
        try:
            with open(fpath, 'rb') as fp:
                gzbys: typing.Final[bytes] = fp.read()
        except:
            errmes = 'Error: man.toml.gz cache file open error. [{0}]'.format(
                fpath)
            print(errmes, file=sys.stderr)
            exit(1)
        hobj.update(gzbys)
        hashdg_body: str = hobj.hexdigest()
        if hashdg_body != hashdg:
            return False, ''
        mantomlbys: bytes = gzip.decompress(gzbys)
        mantomlstr: str = mantomlbys.decode('UTF-8')
        return True, mantomlstr

    def store_pager(self, hit: bool, pagerurl: str, gzbys: bytes):
        if hit:
            return
        errmes: str = ''
        chklist: list = [(hit, 'hit', bool), (pagerurl,
                                              'pagerurl', str), (gzbys, 'gzbys', bytes)]
        for v, vname, vtype in chklist:
            if isinstance(v, vtype) != True:
                errmes = 'Error: {0} is NOT {1} type'.format(
                    vname, repr(vtype))
                raise TypeError(errmes)
        splitted: list = pagerurl.rsplit('/', 1)
        if len(splitted) != 2:
            errmes = 'Error: Not pagerurl format. [{0}]'.format(pagerurl)
            print(errmes, file=sys.stderr)
            exit(1)
        fname: str = splitted[1]
        ptn: str = r'[0-9a-f]{6}\.[1-9a-z]\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not pager format. [{0}]'.format(fname)
            print(errmes, file=sys.stderr)
            exit(1)
        fpath: pathlib.PosixPath | pathlib.WindowsPath
        fpath = self.tmpdir / fname
        with open(str(fpath), 'wb') as fp:
            fp.write(gzbys)
        return


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
