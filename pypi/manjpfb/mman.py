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
import shutil
import unicodedata
import tomllib
import types
import typing
import pydoc
import copy
import gzip
import hashlib
import pathlib
import tempfile
import multiprocessing
import urllib.request
if __name__ == '__main__':
    from man_mother_mary import MmanStdError, Mainfunc, Mmanfunc, Man_cache, Man_pagercache
else:
    try:
        from .man_mother_mary import MmanStdError, Mainfunc, Mmanfunc, Man_cache, Man_pagercache
    except:
        from man_mother_mary import MmanStdError, Mainfunc, Mmanfunc, Man_cache, Man_pagercache


class Opt_http_header(object):
    __slots__ = ['_x_mman_enable',
                 '_user_agent',
                 '_x_mman_roottomlid',
                 '_x_mman_mantomlid']

    def __init__(self):
        self._x_mman_enable: str = ''
        self._user_agent: str = ''
        self._x_mman_roottomlid: str = ''
        self._x_mman_mantomlid: str = ''
        return

    @property
    def x_mman_enable(self) -> str:
        return self._x_mman_enable

    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def x_mman_roottomlid(self) -> str:
        return self._x_mman_roottomlid

    @property
    def x_mman_mantomlid(self) -> str:
        return self._x_mman_mantomlid

    @x_mman_enable.setter
    def x_mman_enable(self, v: str):
        if isinstance(v, str) != True:
            errmes: str = 'Error: x_mman_enable is NOT string type.'
            raise TypeError(errmes)
        self._x_mman_enable = v.upper()
        return

    @user_agent.setter
    def user_agent(self, v: str):
        ptn: str = r'^m[0-9a-z]+\/[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]'
        if re.match(ptn, v) == None:
            errmes: str = 'Error: Invalid user-agent. [{0}]'.format(v)
            raise MmanStdError(errmes)
        self._user_agent = v
        return

    @x_mman_roottomlid.setter
    def x_mman_roottomlid(self, v: str):
        ptn: str = r'^[0-9a-f]{64}'
        if re.match(ptn, v) == None:
            errmes: str = 'Error: Invalid x-mman-roottomlid [{0}]'.format(v)
            raise MmanStdError(errmes)
        self._x_mman_roottomlid = v
        return

    @x_mman_mantomlid.setter
    def x_mman_mantomlid(self, v: str):
        ptn: str = r'^[0-9a-f]{64}'
        if re.match(ptn, v) == None:
            errmes: str = 'Error: Invalid x-mman-mantomlid [{0}]'.format(v)
            raise MmanStdError(errmes)
        self._x_mman_mantomlid = v
        return

    def print_attributes(self):
        for rawvname in self.__slots__:
            vname = rawvname.removeprefix('_')
            v = getattr(self, rawvname)
            mes: str = '{0} : {1}'.format(vname, v)
            print(mes)


class Man_loadurl_getnpdata(typing.NamedTuple):
    data: bytes
    url: str

    def string(self) -> str:
        return self.data.decode('UTF-8')

    def gzdecompress(self) -> bytes:
        return gzip.decompress(self.data)

    def gzdecompress_string(self) -> bytes:
        b: bytes = gzip.decompress(self.data)
        return b.decode('UTF-8')

    def compare(self, hashdg: str) -> bool:
        ptn: str = r'^[0-9a-f]{64}$'
        if re.match(ptn, hashdg) == None:
            errmes = 'Error: Not hashdigest.'
            raise MmanStdError(errmes)
        hobj = hashlib.new('SHA3-256')
        hobj.update(self.data)
        hashdg_body: str = hobj.hexdigest()
        if hashdg != hashdg_body:
            warnmes = 'Warning: Not match hashdigest, [{0}]'.format(self.url)
            print(warnmes)
            print('  hashdg      :', hashdg)
            print('  hashdg(body):', hashdg_body)
            return False
        return True


class Man_loadurl_chkretfc(object):
    @staticmethod
    def chkfc_hashdgsha3(body: bytes) -> bool:
        urlstring: str = body.decode('UTF-8')
        if urlstring.startswith('SHA3-256(') != True:
            return False
        splitted: list = urlstring.rsplit(')= ', 1)
        if len(splitted) != 2:
            return False
        hashdg_sec: str = splitted[1].strip()
        ptn: str = r'[0-9a-f]{64}$'
        reobj = re.match(ptn, hashdg_sec)
        if reobj == None:
            return False
        return True

    @staticmethod
    def retfc_hashdgsha3(body: bytes) -> bytes:
        if isinstance(body, bytes) != True:
            errmes: str = 'Error: body is not bytes type.'
            raise TypeError(errmes)
        if body.startswith(b'SHA3-256(') != True:
            return b''
        splitted: list = body.rsplit(b')= ', 1)
        if len(splitted) != 2:
            return b''
        hashdg: bytes = splitted[1].strip()
        ptnstr: str = r'[0-9a-f]{64}$'
        ptn: bytes = ptnstr.encode()
        reobj = re.match(ptn, hashdg)
        if reobj == None:
            return ''
        return hashdg


class Man_loadurl(object):
    __slots__ = ['_header_x_mman_enable',
                 '_header_user_agent',
                 '_header_x_mman_roottomlid',
                 '_header_x_mman_mantomlid', '_urls',
                 '_fastestdomain', '_timeout',
                 '_request_starttime',
                 '_pobjlist']

    def __init__(self):
        self._header_x_mman_enable: str = ''
        self._header_user_agent: str = ''
        self._header_x_mman_roottomlid: str = ''
        self._header_x_mman_mantomlid: str = ''
        self._urls: tuple[str] = tuple([''])
        self._fastestdomain: str = ''
        self._timeout: float = 10
        self._request_starttime: float = 0.0
        self._pobjlist: tuple = tuple()
        return

    @property
    def header_x_mman_enable(self) -> str:
        return self._header_x_mman_enable

    @property
    def header_user_agent(self) -> str:
        return self._header_user_agent

    @property
    def header_x_mman_roottomlid(self) -> str:
        return self._header_x_mman_roottomlid

    @property
    def header_x_mman_mantomlid(self) -> str:
        return self._header_x_mman_mantomlid

    @property
    def urls(self) -> tuple[str]:
        return self._urls

    @property
    def fastestdomain(self) -> str:
        return self._fastestdomain

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def request_starttime(self) -> float:
        return self._request_starttime

    @header_x_mman_enable.setter
    def header_x_mman_enable(self, v: str):
        if isinstance(v, str) != True:
            errmes: str = 'Error: x_mman_enable is NOT string type.'
            raise TypeError(errmes)
        self._header_x_mman_enable = v.upper()
        return

    @header_user_agent.setter
    def header_user_agent(self, v: str):
        ptn: str = r'^m[a-z]+\/[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]'
        if re.match(ptn, v) == None:
            errmes: str = 'Error: Invalid user-agent. [{0}]'.format(v)
            raise MmanStdError(errmes)
        self._header_user_agent = v
        return

    @header_x_mman_roottomlid.setter
    def header_x_mman_roottomlid(self, v: str):
        ptn: str = r'^[0-9a-f]{64}'
        if re.match(ptn, v) == None:
            errmes: str = 'Error: Invealid x-mman-roottomlid [{0}]'.format(v)
            raise MmanStdError(errmes)
        self._header_x_mman_roottomlid = v
        return

    @header_x_mman_mantomlid.setter
    def header_x_mman_mantomlid(self, v: str):
        ptn: str = r'^[0-9a-f]{64}'
        if re.match(ptn, v) == None:
            errmes: str = 'Error: Invalid x-mman-mantomlid [{0}]'.format(v)
            raise MmanStdError(errmes)
        self._header_x_mman_mantomlid = v
        return

    @urls.setter
    def urls(self, v: list | tuple):
        chklist: list = [isinstance(v, list), isinstance(v, tuple)]
        if chklist.count(True) == 0:
            errmes: str = 'Error: urls is not list or tuple.'
            raise MmanStdError(errmes)
        if len(v) == 0:
            errmes: str = 'Error: urls is empty.'
            raise MmanStdError(errmes)
        self._urls = tuple(v)
        return

    @fastestdomain.setter
    def fastestdomain(self, v: str):
        if isinstance(v, str) != True:
            errmes: str = 'Error: fastestdomain is NOT string type.'
            raise TypeError(errmes)
        s1: str = v.removeprefix('https://') if v.startswith('https://') else v
        splitted: list = s1.split('/', maxsplit=1)
        self._fastestdomain = splitted[0]
        return

    @timeout.setter
    def timeout(self, v: float | int):
        if isinstance(v, float) != True and isinstance(v, int) != True:
            errmes: str = 'Error: timeout is NOT float or integer type.'
            raise TypeError(errmes)
        if v < 0:
            errmes = 'Error: timeout is NOT positive. [{0}]'.format(v)
            raise ValueError(errmes)
        self._timeout = v
        return

    def _fastesturl(self) -> str:
        if len(self.urls) == 0:
            errmes: str = 'Error: empty Man_loadurl.urls'
            raise MmanStdError(errmes)
        if self.fastestdomain == '':
            return self.urls[0]
        for url in self.urls:
            splitted: tuple = tuple(url.split('://'))
            if len(splitted) != 2:
                errmes = 'Error: Invalid url. [{0}]'.format(url)
                raise MmanStdError(errmes)
            s: str = splitted[1]
            if s.startswith(self.fastestdomain):
                return url
        return self.urls[0]

    def print_attributes(self):
        for vname in self.__slots__:
            v = getattr(self, vname)
            mes: str = '{0}: {1}'.format(vname, v)
            print(mes)
        return

    def getdata(self, exception: bool = True,
                chkfc: typing.Callable = lambda x: True if x != b'' else False,
                retfc: typing.Callable = lambda x: x) -> Man_loadurl_getnpdata:
        def urliter(self):
            urlpath: str = self._fastesturl()
            yield urlpath
            for url in self.urls:
                if url == urlpath:
                    continue
                yield url
            return
        errmes: str = ''
        errmeslist: list = list()
        for urlpath in urliter(self):
            request = urllib.request.Request(urlpath)
            chklist: list = [(self.header_x_mman_enable, 'x-mman-enable'),
                             (self.header_user_agent, 'user-agent'),
                             (self.header_x_mman_roottomlid, 'x-mman-roottomlid'),
                             (self.header_x_mman_mantomlid, 'x-mman-mantomlid')]
            for hvalue, hname in chklist:
                if hvalue != '':
                    request.add_header(hname, hvalue)
            html_content: bytes = b''
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    html_content = response.read()
                    self._request_starttime = time.time()
            except urllib.error.URLError as e:
                errmes = 'Error: URL Error. {0}, URL: {1}'.format(e, urlpath)
                errmeslist.append(errmes)
            except urllib.error.HTTPError as e:
                errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
                errmeslist.append(errmes)
            except Exception as e:
                errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(
                    e, urlpath)
                errmeslist.append(errmes)
            if chkfc(html_content):
                break
        if html_content == b'' and len(errmeslist) >= 1 and exception == True:
            errmes = '\n'.join(errmeslist)
            raise MmanStdError(errmes)
        elif html_content == b'' and len(errmeslist) >= 1:
            retobj: Man_loadurl_getnpdata = Man_loadurl_getnpdata(
                data=b'', url=urlpath)
            return retobj
        retfc_content: bytes = retfc(html_content)
        if isinstance(retfc_content, bytes) != True:
            errmes = 'Error: retfc_content is not bytes type.'
            raise MmanStdError(errmes)
        retobj: Man_loadurl_getnpdata = Man_loadurl_getnpdata(
            data=retfc_content, url=urlpath)
        return retobj

    @staticmethod
    def _loadurl_by_request(request, retqueue, rettype: str, timeout: float):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                html_content = response.read()
        except:
            html_content: bytes = b''
        result: tuple = tuple()
        if rettype == 'bytes':
            result = (request.full_url, html_content)
        elif rettype == 'string':
            result = (request.full_url, html_content.decode('UTF-8'))
        timeout: int = int(time.time()) + 3
        while timeout > int(time.time()):
            try:
                retqueue.put_nowait(result)
            except:
                time.sleep(0.07)
            break
        return

    def getdata_1stmp(self, exception: bool = True,
                      chkfc: typing.Callable[[bytes], bool] = None,
                      retfc: typing.Callable[[bytes], bytes] = lambda x: x)\
            -> Man_loadurl_getnpdata:
        timeout: int = 10
        requests: list = list()
        for urlpath in self.urls:
            request = urllib.request.Request(urlpath)
            chklist: list = [(self.header_x_mman_enable, 'x-mman-enable'),
                             (self.header_user_agent, 'user-agent'),
                             (self.header_x_mman_roottomlid, 'x-mman-roottomlid'),
                             (self.header_x_mman_mantomlid, 'x-mman-mantomlid')]
            for hvalue, hname in chklist:
                if hvalue != '':
                    request.add_header(hname, hvalue)
            requests.append(request)
        if len(self._pobjlist) >= 1:
            self.close()
        retqueue: multiprocessing.queues.Queue = multiprocessing.Queue()
        func: typing.Callable = self._loadurl_by_request
        pobjlist: list = list()
        for request in requests:
            funcargs: list = [request, retqueue, 'bytes', self.timeout]
            pobj = multiprocessing.Process(target=func, args=funcargs)
            pobjlist.append(pobj)
        self._pobjlist = tuple(pobjlist)
        [pobj.start() for pobj in pobjlist]
        self._request_starttime = time.time()
        t: tuple = tuple()
        returl: str = ''
        retbody: bytes = b''
        time_end: int = int(time.time()) + timeout

        def default_chkfc(retbody: bytes):
            ret: bool = True if retbody != b'' else False
            return ret
        if chkfc == None:
            chkfc = default_chkfc
        while time_end >= int(time.time()):
            try:
                t = retqueue.get_nowait()
                returl = t[0]
                retbody = t[1]
            except:
                time.sleep(0.1)
                continue
            if chkfc(retbody):
                break
            if retbody != b'':
                break
        if retbody == b'':
            returl = ''
        retfc_retbody = retfc(retbody)
        if isinstance(retfc_retbody, bytes) != True:
            errmes = 'Error: retrc_retbody is not bytes type.'
            raise TypeError(errmes)
        npdata: Man_loadurl_getnpdata = Man_loadurl_getnpdata(
            data=retfc_retbody, url=returl)
        return npdata

    def close(self):
        if len(self._pobjlist) == 0:
            return
        timeout: typing.Final[float] = self._request_starttime + \
            self.timeout + 0.2
        while timeout > time.time():
            chklist: list = [
                True for pobj in self._pobjlist if pobj.is_alive() == True]
            if len(chklist) == 0:
                return
            time.sleep(0.1)
        for pobj in self._pobjlist:
            if pobj.is_alive():
                pobj.terminate()
                while pobj.is_alive():
                    time.sleep(0.1)
        return


class Man_roottoml_subroutine(object):
    @staticmethod
    def get_hashdg_url(roottomlurl_sha3: str) -> str:
        mainfunc = Mainfunc
        mmanfunc = Mmanfunc
        warnmes: str = ''
        if isinstance(roottomlurl_sha3, str) != True:
            errmes = 'Error: url is NOT string type on get_hashdg_url()'
            raise TypeError(errmes)
        urlstring: str = ''
        urlstring = mmanfunc.loadstring_url(roottomlurl_sha3, exception=False)
        if urlstring == '':
            return ''
        if urlstring.startswith('SHA3-256(') != True:
            warnmes = 'Warning: Not SHA3-256 hashdigest format.'
            print(warnmes, file=sys.stderr)
            return ''
        splitted: list = urlstring.rsplit(')= ', 1)
        if len(splitted) != 2:
            warnmes = 'Warning: Invalid root.toml.gz.SHA3-256 format. [{0}]'.format(
                roottomlurl_sha3)
            print(warnmes, file=sys.stderr)
            return ''
        hashdg_sec: str = splitted[1].strip()
        ptn: str = r'[0-9a-f]{64}$'
        reobj = re.match(ptn, hashdg_sec)
        if reobj == None:
            warnmes = 'Warning: Not found SHA3-256 hashdigest pattern. [{0}]'.format(
                roottomlurl_sha3)
            print(warnmes, file=sys.stderr)
            return ''
        hashdg_url: str = reobj.group(0) if reobj is not None else ''
        return hashdg_url


class Man_roottoml(object):
    __root_sites: typing.Final[list] = [
        (104, 116, 116, 112, 115, 58, 47, 47, 100, 49, 101, 101, 56,
         110, 49, 121, 105, 108, 101, 50, 117, 122, 46, 99, 108, 111,
         117, 100, 102, 114, 111, 110, 116, 46, 110, 101, 116),
        (104, 116, 116, 112, 115, 58, 47, 47, 109, 105, 107, 101,
         116, 117, 114, 107, 101, 121, 46, 99, 111, 109)]
    __root_dir: typing.Final[str] = '/clidirs/man{0}/{1}/'
    __root_name: typing.Final[str] = 'root.toml.gz'
    __root_dir_suffixes: typing.Final[dict] = {
        ('fb', 'jpn', 'arm64'): 'jpfb',
        ('fb', 'eng', 'arm64'): 'enfb',
        ('ob', 'eng', 'arm64'): 'enob'}
    __webdbnums: typing.Final[dict] =\
        {('fb', 'jpn', 'arm64'): '1002',
         ('fb', 'eng', 'arm64'): '1002',
         ('ob', 'eng', 'arm64'): '1002'}

    def __init__(self):
        self.og_vernamekey: str = ''
        self.og_manhashfpath: str = ''
        self.og_roottomlfpath: str = ''
        self.og_manenv_os2: str = ''
        self.og_manenv_lang: str = ''
        self.og_manenv_arch: str = ''
        self.og_cache_rooturls: tuple = tuple()
        self.og_cmdname: str = ''
        self.og_cmdversion: str = ''
        self.og_cmddate: str = ''
        self._og_http_header: Opt_http_header = Opt_http_header()
        self._status: str = ''
        self._thedate: str = ''
        self._osname: str = ''
        self._urls: list = list()
        self._baseurls: tuple[str] = tuple()
        self._message: str = ''
        self._rooturls: tuple[str] = tuple()
        self._manhashfpath: str = ''
        self._fastestdomain: str = ''
        self._rootstr: str = ''
        self._roottomlurl: str = ''
        self._rootdic: dict = dict()
        self._mantomlurls: list = list()
        return

    @property
    def og_http_header(self) -> Opt_http_header:
        return self._og_http_header

    @property
    def status(self) -> str:
        return self._status

    @property
    def thedate(self) -> str:
        return self._thedate

    @property
    def osname(self) -> str:
        return self._osname

    @property
    def urls(self) -> list:
        return self._urls

    @property
    def baseurls(self) -> tuple:
        return self._baseurls

    @property
    def message(self) -> str:
        return self._message

    @property
    def rooturls(self) -> tuple:
        return self._rooturls

    @property
    def manhashfpath(self) -> str:
        return self._manhashfpath

    @property
    def fastestdomain(self) -> str:
        return self._fastestdomain

    @og_http_header.setter
    def og_http_header(self, header: Opt_http_header):
        if isinstance(header, Opt_http_header) != True:
            errmes: str = 'Error: header object is Not Opt_http_header.'
            raise TypeError(errmes)
        self._og_http_header = header
        return

    def print_attributes(self):
        for k, v in self.__dict__.items():
            print('k: ', k)
            print('  v:', v)
        return

    def _getrooturl(self, cache_rooturls: tuple = tuple()):
        t: tuple = (self.og_manenv_os2, self.og_manenv_lang,
                    self.og_manenv_arch)
        errmes: str = ''
        root_dir_suffix: str = self.__root_dir_suffixes.get(t, '')
        if root_dir_suffix == '':
            errmes = 'Error: Not found __root_dir_suffixes key. [{0}]'.format(
                t)
            raise MmanStdError(errmes)
        webdbnum: str = self.__webdbnums.get(t, '')
        if webdbnum == '':
            errmes = 'Error: Not found __webdbnums key. [{0}]'.format(t)
            raise MmanStdError(errmes)
        if len(cache_rooturls) >= 1:
            root_sites: tuple = cache_rooturls
        else:
            root_sites = tuple([''.join([chr(i) for i in t])
                               for t in self.__root_sites])

        def func(x): return x + self.__root_dir.format(root_dir_suffix,
                                                       webdbnum) + self.__root_name
        roottomlurls: list = [func(root_site) for root_site in root_sites]
        return roottomlurls

    def _load_roottomlurls(self, roottomlurls: tuple, cache: Man_cache) -> tuple[str, str]:
        mainfunc = Mainfunc
        subr = Man_roottoml_subroutine
        debug: bool = False
        errmes: str = ''
        if isinstance(roottomlurls, tuple) != True:
            errmes = 'Error: roottomlurls is not tuple type.'
            raise TypeError(errmes)
        for url in roottomlurls:
            if url.endswith('toml.gz') != True:
                errmes = 'Error: Not root.toml.gz file. [{0}]'.format(url)
                raise MmanStdError(errmes)
        roottomlsha3urls: list = [url + '.SHA3-256' for url in roottomlurls]
        loadurl = Man_loadurl()
        loadurl.header_x_mman_enable = self.og_http_header.x_mman_enable
        loadurl.header_user_agent = self.og_http_header.user_agent
        loadurl.timeout = 0.8
        loadurl.urls = tuple(roottomlsha3urls)
        sha3chkfc: typing.Callable = Man_loadurl_chkretfc.chkfc_hashdgsha3
        sha3retfc: typing.Callable = Man_loadurl_chkretfc.retfc_hashdgsha3
        npdata: Man_loadurl_getnpdata = loadurl.getdata_1stmp(
            chkfc=sha3chkfc, retfc=sha3retfc)
        roottomlurl_sha3: str = npdata.url
        hashdg_url: str = npdata.string()
        if hashdg_url == '':
            errmes = 'Error: Can not download the url. [{0}]'.format(
                loadurl.urls)
            raise MmanStdError(errmes)
        self._fastestdomain = roottomlurl_sha3
        self.og_http_header.x_mman_roottomlid = hashdg_url
        loadurl.close()
        hit: bool
        rootstr: str
        hit, rootstr = cache.get_roottoml(hashdg_url)
        hit = False
        gzbys: bytes = b''
        if hit != True:
            loadurl = Man_loadurl()
            loadurl.header_x_mman_enable = self.og_http_header.x_mman_enable
            loadurl.header_user_agent = self.og_http_header.user_agent
            loadurl.header_x_mman_roottomlid = self.og_http_header.x_mman_roottomlid
            loadurl.timeout = 1.5
            loadurl.fastestdomain = self.fastestdomain
            loadurl.urls = tuple(roottomlurls)
            npdata: Man_loadurl_getnpdata = loadurl.getdata()
            npdata.compare(hashdg_url)
            roottomlurl: str = npdata.url
            gzbys: bytes = npdata.data
            rootstr = npdata.gzdecompress_string()
        else:
            roottomlurl = ''
        if debug:
            print('hit of root:', hit)
        cache.store_roottoml(hit, gzbys)
        return rootstr, roottomlurl

    def _load_mantomlurls(self, mantomlurls: list, cache: Man_cache) -> dict:
        mainfunc = Mainfunc
        subr = Man_roottoml_subroutine
        debug: bool = False
        if len(mantomlurls) < 1:
            errmes = 'Error: mantomlurls length is zero.'
            raise MmanStdError(errmes)
        for url in mantomlurls:
            if url.endswith('.toml.gz') != True:
                errmes = 'Error: url is invalid extension. [{0}]'.format(url)
                raise MmanStdError(errmes)
        mantomlsha3urls: list = [url + '.SHA3-256' for url in mantomlurls]
        loadurl = Man_loadurl()
        loadurl.header_x_mman_enable = self.og_http_header.x_mman_enable
        loadurl.header_user_agent = self.og_http_header.user_agent
        loadurl.header_x_mman_roottomlid = self.og_http_header.x_mman_roottomlid
        loadurl.timeout = 0.8
        loadurl.fastestdomain = self.fastestdomain
        loadurl.urls = tuple(mantomlsha3urls)
        sha3chkfc: typing.Callable = Man_loadurl_chkretfc.chkfc_hashdgsha3
        sha3retfc: typing.Callable = Man_loadurl_chkretfc.retfc_hashdgsha3
        npdata: Man_loadurl_getnpdata = loadurl.getdata(
            chkfc=sha3chkfc, retfc=sha3retfc)
        hashdg_url = npdata.string()
        if hashdg_url == '':
            errmes = 'Error: Can not load the url.\n'
            for url in mantomlsha3urls:
                errmes += '  URL: {0}\n'.format(url)
            raise MmanStdError(errmes)
        ptn: str = r'[0-9a-f]{64}$'
        if re.match(ptn, hashdg_url) == None:
            errmes = 'Error: hashdg_url is NOT hashdg. [{0}]'.format(
                hashdg_url)
            raise MmanStdError(errmes)
        self.og_http_header.x_mman_mantomlid = hashdg_url
        gzbys: bytes = b''
        mantomlstr: str = ''
        tomldic: dict = dict()
        hit: bool = False
        hit, mantomlstr = cache.get_mantoml(mantomlurls[0], hashdg_url)
        if not hit:
            loadurl = Man_loadurl()
            loadurl.header_x_mman_enable = self.og_http_header.x_mman_enable
            loadurl.header_user_agent = self.og_http_header.user_agent
            loadurl.header_x_mman_roottomlid = self.og_http_header.x_mman_roottomlid
            loadurl.header_x_mman_mantomlid = self.og_http_header.x_mman_mantomlid
            loadurl.header_x_mman_mantomlid = hashdg_url
            loadurl.timeout = 0.8
            loadurl.fastestdomain = self.fastestdomain
            loadurl.urls = tuple(mantomlurls)
            mantoml: Man_loadurl_getnpdata = loadurl.getdata()
            mantoml.compare(hashdg_url)
            gzbys: bytes = mantoml.data
            mantomlstr: str = mantoml.gzdecompress_string()
        if debug:
            print('hit of man.toml.gz:', hit)
            print('mantomlurl:', mantomlurls[0])
        cache.store_mantoml(hit, mantomlurls[0], gzbys)
        tomldic = tomllib.loads(mantomlstr)
        return copy.copy(tomldic)

    def make(self):
        mainfunc = Mainfunc
        cache = Man_cache()
        cache.init(self.og_manenv_os2, self.og_manenv_lang, self.og_manenv_arch,
                   self.og_cmdversion, self.og_cmddate)
        enable_cache: bool = True
        if len(self.og_cache_rooturls) >= 1 and enable_cache == True:
            tmplist: list = self._getrooturl(
                cache_rooturls=self.og_cache_rooturls)
            roottomlurls: tuple[str] = tuple(tmplist)
        else:
            roottomlurls = tuple(self._getrooturl())
        if not enable_cache:
            mes: str = 'Warning: Disable cache, roottomlurls'
            print(mes)
        errmes: str
        vname: str
        chklist: list = [('og_veramekey', self.og_vernamekey),
                         ('og_manhashfpath', self.og_manhashfpath),
                         ('og_roottomlfpath', self.og_roottomlfpath)]
        for vname, v in chklist:
            if isinstance(v, str) != True:
                errmes = 'Error: {0} is NOT string type.'.format(vname)
                raise TypeError(errmes)
        if self.og_vernamekey == '':
            errmes = 'Error: Not og_vernamekey value.'
            raise ValueError(errmes)
        rootdic: dict
        rootstr: str
        gzbys: bytes
        rootbys: bytes
        s: str
        if self.og_roottomlfpath != '':
            if self.og_roottomlfpath.endswith('.toml'):
                with open(self.og_roottomlfpath, 'rt') as fp:
                    rootstr = fp.read()
            elif self.og_roottomlfpath.endswith('.toml.gz'):
                with open(self.og_roottomlfpath, 'rb') as fp:
                    gzbys = fp.read()
                rootbys = gzip.decompress(gzbys)
                rootstr = rootbys.decode('UTF-8')
        else:
            rootstr, roottomlurl = self._load_roottomlurls(roottomlurls, cache)
            self._roottomlurl = roottomlurl
        rootdic = tomllib.loads(rootstr)
        self._rootstr = rootstr
        self._rootdic = copy.copy(rootdic)
        for vname in ['rooturls', 'baseurls']:
            tmplist: list = rootdic.get(vname, [])
            if len(tmplist) == 0:
                errmes = 'Error: Empty {0} values in root.toml'.format(vname)
                raise MmanStdError(errmes)
            setattr(self, '_' + vname, tuple(tmplist))
        self._message = rootdic.get('message', '')
        url: str
        tpl: tuple
        vernamekey: str = ''
        if self.og_manhashfpath == '':
            tpl = mainfunc.geturlpath_man(self._rootdic, self.og_vernamekey)
            self._mantomlurls, self._osname, self._status, self._thedate, vernamekey = tpl
            tomldic: dict = self._load_mantomlurls(self._mantomlurls, cache)
        else:
            with open(self.og_manhashfpath, 'rb') as fp:
                tomldic = tomllib.load(fp)
        return copy.copy(tomldic)


class Man_mantoml_retmake(typing.NamedTuple):
    pagerurls: tuple
    hashdg: str


class Man_mantoml(object):
    def __init__(self):
        self.og_tomldic: dict = dict()
        self.og_osname_root: str = ''
        self.og_mannum: str = ''
        self.og_manname: str = ''
        self.og_baseurls: tuple = tuple()
        self.og_fnamemode: str = 'hash'
        self._osname: str = ''
        self._arch: str = ''
        self._lang: str = ''
        self._retmake: list[tuple] = list()
        return

    @property
    def osname(self) -> str:
        return self._osname

    @property
    def arch(self) -> str:
        return self._arch

    @property
    def lang(self) -> str:
        return self._lang

    @property
    def retmake(self) -> list[tuple]:
        return self._retmake

    def vcheck_og_tomldic(self):
        vname: str
        for vname in self.og_tomldic.keys():
            if vname == 'OSNAME':
                return
        errmes: str = 'Error: RuntimeError, Invalid tomldic.'
        raise MmanStdError(errmes)

    def vcheck_og_osname_root(self):
        ptns: typing.Final[tuple] = ('FreeBSD', 'OpenBSD')
        ptn: str
        for ptn in ptns:
            if self.og_osname_root.startswith(ptn):
                return
        errmes: str = 'Error: Invalid OSNAME on man metadata.'
        raise MmanStdError(errmes)

    def vcheck_og_mannum(self):
        ptns: typing.Final[tuple] = ('', '1', '2', '3', '4',
                                     '5', '6', '7', '8', '9')
        ptn: str = ''
        for ptn in ptns:
            if self.og_mannum == ptn:
                return
        errmes: str = 'Error: Invalid Man section number(1-9). [{0}]'.format(
            self.og_mannum)
        raise MmanStdError(errmes)

    def vcheck_og_manname(self):
        ptn: typing.Final[str] = r'^[A-Za-z0-9\_\-\[]+'
        reobj: typing.Final = re.match(ptn, self.og_manname)
        if reobj == None:
            errmes: str = 'Error: Invalid man name string. [{0}]'.format(
                self.og_manname)
            raise MmanStdError(errmes)
        return

    def vcheck_og_baseurls(self):
        errmes: str
        url: str
        if isinstance(self.og_baseurls, tuple) != True:
            errmes = 'Error: Man_mantoml.og_baseurls is NOT tuple type.'
            raise TypeError(errmes)
        if len(self.og_baseurls) == 0:
            errmes = 'Error: Runtime Error, Empty Man_mantoml.og_baseurls.'
            raise ValueError(errmes)
        for url in self.og_baseurls:
            if isinstance(url, str) != True:
                errmes = 'Error: Man_mantoml.og_baseurls element is NOT string type.'
                raise TypeError(errmes)
            if url.startswith('https://') != True:
                errmes = 'Error: baseurl protocol is NOT "https://". [{0}]'.format(
                    url)
                raise MmanStdError(errmes)
            if ('miketurkey.com' not in url) and ('cloudfront.net' not in url):
                errmes = 'Error: baseurl is NOT "miketurkey.com". [{0}]'.format(
                    url)
                raise MmanStdError(errmes)
        return

    def vcheck_og_fnamemode(self):
        errmes: str
        if isinstance(self.og_fnamemode, str) != True:
            errmes = 'Error: og_fnamemode is NOT string type.'
            raise TypeError(errmes)
        if self.og_fnamemode not in ('raw', 'hash'):
            errmes = 'Error: og_fnamemode is NOT raw and hash.'
            raise MmanStdError(errmes)
        return

    @staticmethod
    def _mkfname_webdb(fname: str, hashdg: str, fnamemode: str) -> str:
        errmes: str = ''
        ptn_hashdg: typing.Final[str] = r'[0-9a-f]{64}'
        ptn_fname:  typing.Final[str] = r'.+\.[1-9]'
        if re.fullmatch(ptn_fname, fname) == None:
            errmes = 'Error: Invalid fname. [{0}]'.format(fname)
            raise MmanStdError(errmes)
        if re.fullmatch(ptn_hashdg, hashdg) == None:
            errmes = 'Error: Runtime Error, Invalid hashdg pattern. [{0}]'.format(
                hashdg)
            raise MmanStdError(errmes)
        if fnamemode == 'raw':
            return fname
        templist: list
        if fnamemode == 'hash':
            templist = fname.rsplit('.', 1)
            fname_ext: typing.Final[str] = templist[1]
            retstr: typing.Final[str] = hashdg[0:6] + '.' + fname_ext + '.gz'
            return retstr
        errmes = 'Error: Runtime Error, Invalid fnamemode. [{0}]'.format(
            fnamemode)
        raise MmanStdError(errmes)

    def print_attributes(self):
        for k, v in self.__dict__.items():
            print('k: ', k)
            print('  v:', v)
        return

    def make(self) -> list[tuple]:
        retempty: Man_mantoml_retmake = Man_mantoml_retmake(
            pagerurls=tuple(), hashdg='')
        self.vcheck_og_tomldic()
        self.vcheck_og_osname_root()
        self.vcheck_og_mannum()
        self.vcheck_og_manname()
        self.vcheck_og_baseurls()
        self.vcheck_og_fnamemode()
        fnameurldic: dict = dict()
        for k, v in self.og_tomldic.items():
            if k in ('OSNAME', 'ARCH', 'LANG'):
                self._osname = v if k == 'OSNAME' else self._osname
                self._arch = v if k == 'ARCH' else self._arch
                self._lang = v if k == 'LANG' else self._lang
                continue
            fname: str = k
            hashdg: str = v['hash']
            fname_new: str = self._mkfname_webdb(
                fname, hashdg, self.og_fnamemode)

            def inloop1(baseurl: str, hashdg: str, fname: str) -> tuple[str, str]:
                mainfunc = Mainfunc
                s: typing.Final[str] = baseurl + '/' + \
                    hashdg[0:2] + '/' + hashdg + '/' + fname
                return mainfunc.normurl(s)
            pagerurls: list = [inloop1(baseurl, hashdg, fname_new)
                               for baseurl in self.og_baseurls]
            np: Man_mantoml_retmake = Man_mantoml_retmake(
                pagerurls=tuple(pagerurls), hashdg=hashdg)
            fnameurldic[fname] = np
        if self.og_osname_root != self.osname:
            errmes = 'Error: Mismatch OSNAME. [{0}, {1}]'.format(
                self.og_osname_root, self.osname)
            raise MmanStdError(errmes)
        fnameurldictkeys: list
        if self.og_mannum != '':
            fnameurldictkeys = [self.og_manname + '.' + self.og_mannum]
        else:
            fnameurldictkeys = ['{0}.{1}'.format(
                self.og_manname, i) for i in range(1, 10)]
        for fname in fnameurldictkeys:
            retnp: Man_mantoml_retmake = fnameurldic.get(fname, retempty)
            if retnp != retempty:
                break
        return retnp


class Np_getstring_pagerurl(typing.NamedTuple):
    pagerstr: str
    gzbys: bytes


class _Main_man(object):
    @staticmethod
    def enable_terminal() -> tuple[bool | None, str]:
        rettrue: typing.Final[tuple] = (True, '')
        retnone: typing.Final[tuple] = (None, '')
        if sys.platform in ['darwin', 'win32']:
            return rettrue
        ttyname: str = os.ttyname(sys.stdout.fileno())
        if sys.platform.startswith('freebsd'):
            if ttyname.startswith('/dev/pts'):
                return rettrue
            elif ttyname.startswith('/dev/ttyv'):
                return False, 'FreeBSD_vt'
            else:
                return retnone
        elif sys.platform.startswith('openbsd'):
            if ttyname.startswith('/dev/ttyp'):
                return rettrue
            elif ttyname.startswith('/dev/ttyC'):
                return False, 'OpenBSD_vt'
            else:
                return retnone
        elif sys.platform.startswith('linux'):
            if ttyname.startswith('/dev/pts'):
                return rettrue
            else:
                return retnone
        return retnone

    @staticmethod
    def norm_punctuation(pagerstr: str) -> str:
        ptn = r'[\u2011]|[\u2012]|[\u2013]'
        return re.sub(ptn, '-', pagerstr)

    @staticmethod
    def show_license(os2: str, lang: str, arch: str, mman: bool = False):
        mmanfunc = Mmanfunc
        license: str = ''
        if mman:
            license = mmanfunc.createstr_license(os2, lang, arch, mkall=True)
        else:
            license = mmanfunc.createstr_license(os2, lang, arch)
        print(license)
        exit(0)

    @staticmethod
    def show_listman_n(secnum: int, vernamekey: str, os2: str, lang: str, arch: str, gui: bool, cache: Man_cache,
                       cmdversion: str, cmddate: str) -> str | None:
        mmanfunc = Mmanfunc
        http_header: Opt_http_header = Opt_http_header()
        http_header.x_mman_enable = 'YES'
        http_header.user_agent = mmanfunc.createstr_cmdname(
            os2, lang, arch) + '/{0}'.format(cmdversion)
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = '@LATEST-RELEASE'
        roottomlobj.og_manhashfpath = ''
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = os2
        roottomlobj.og_manenv_lang = lang
        roottomlobj.og_manenv_arch = arch
        roottomlobj.og_cmdversion = cmdversion
        roottomlobj.og_cmddate = cmddate
        roottomlobj.og_rooturls = cache.load_rooturls()
        roottomlobj.og_http_header = http_header
        tomldic: typing.Final[dict] = roottomlobj.make()

        def inloop(name: str, secnum: int) -> str:
            ptns = ('.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9')
            ptn: str = ptns[secnum - 1]
            if name.endswith(ptn):
                return name.removesuffix(ptn)
            return ''
        mannames = [inloop(name, secnum) for name,
                    d in tomldic.items() if isinstance(d, dict) == True]
        mannames = [name for name in mannames if name != '']
        mannames.sort()
        if gui:
            tmplist: list = [name for name in mannames]
            return '\n'.join(tmplist)
        for name in mannames:
            print(name)
        exit(0)

    @staticmethod
    def show_listman(vernamekey: str, os2: str, lang: str, arch: str, gui: bool, cache: Man_cache,
                     cmdversion: str, cmddate: str) -> str | None:
        mmanfunc = Mmanfunc
        http_header: Opt_http_header = Opt_http_header()
        http_header.x_mman_enable = 'YES'
        http_header.user_agent = mmanfunc.createstr_cmdname(
            os2, lang, arch) + '/{0}'.format(cmdversion)
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = '@LATEST-RELEASE'
        roottomlobj.og_manhashfpath = ''
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = os2
        roottomlobj.og_manenv_lang = lang
        roottomlobj.og_manenv_arch = arch
        roottomlobj.og_cmdversion = cmdversion
        roottomlobj.og_cmddate = cmddate
        roottomlobj.og_rooturls = cache.load_rooturls()
        roottomlobj.og_http_header = http_header
        tomldic: typing.Final[dict] = roottomlobj.make()

        def inloop(name: str) -> str:
            ptns = ('.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9')
            for ptn in ptns:
                if name.endswith(ptn):
                    return name.removesuffix(ptn)
            return name
        mannames = [inloop(name) for name, d in tomldic.items()
                    if isinstance(d, dict) == True]
        mannames.sort()
        if gui:
            tmplist: list = [name for name in mannames]
            return '\n'.join(tmplist)
        for name in mannames:
            print(name)
        exit(0)

    @staticmethod
    def show_listos(os2: str, lang: str, arch: str, cache: Man_cache,
                    cmdversion: str, cmddate: str):
        mainfunc = Mainfunc
        mmanfunc = Mmanfunc
        http_header: Opt_http_header = Opt_http_header()
        http_header.x_mman_enable = 'YES'
        http_header.user_agent = mmanfunc.createstr_cmdname(
            os2, lang, arch) + '/{0}'.format(cmdversion)
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = '@LATEST-RELEASE'
        roottomlobj.og_manhashfpath = ''
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = os2
        roottomlobj.og_manenv_lang = lang
        roottomlobj.og_manenv_arch = arch
        roottomlobj.og_cmdversion = cmdversion
        roottomlobj.og_cmddate = cmddate
        roottomlobj.og_rooturls = cache.load_rooturls()
        roottomlobj.og_http_header = http_header
        roottomlobj.make()
        rootdic: typing.Final[dict] = roottomlobj._rootdic
        osnames = [osname for vername, osname, status,
                   thedate, urls in mainfunc.iter_rootdic(rootdic)]
        [print(s) for s in osnames]
        exit(0)

    @staticmethod
    def getstring_pagerurl(pagerurls: tuple, hashdg: str,
                           http_header: Opt_http_header,
                           fastestdomain: str) -> Np_getstring_pagerurl:
        retempty: typing.Final[Np_getstring_pagerurl] = Np_getstring_pagerurl(
            pagerstr='', gzbys=b'')
        chklist: list = [True for url in pagerurls if url.endswith('.gz')]
        if len(chklist) == len(pagerurls):
            loadurl = Man_loadurl()
            loadurl.header_x_mman_enable = http_header.x_mman_enable
            loadurl.header_user_agent = http_header.user_agent
            loadurl.header_x_mman_roottomlid = http_header.x_mman_roottomlid
            loadurl.header_x_mman_mantomlid = http_header.x_mman_mantomlid
            loadurl.timeout = 0.8
            loadurl.fastestdomain = fastestdomain
            loadurl.urls = pagerurls
            pager: Man_loadurl_getnpdata = loadurl.getdata()
            if not pager.compare(hashdg):
                return retempty
            gzbys: bytes = pager.data
            pagerstr: str = pager.gzdecompress_string()
            ret: typing.Final = Np_getstring_pagerurl(
                pagerstr=pagerstr, gzbys=gzbys)
            return ret
        print('Warning: Non-gz files are deprecated and will no longer be supported in the future.')
        loadurl = Man_loadurl()
        loadurl.header_x_mman_enable = http_header.x_mman_enable
        loadurl.header_user_agent = http_header.user_agent
        loadurl.header_x_mman_roottomlid = http_header.x_mman_roottomlid
        loadurl.header_x_mman_mantomlid = http_header.x_mman_mantomlid
        loadurl.timeout = 0.8
        loadurl.fastestdomain = fastestdomain
        loadurl.urls = pagerurls
        pager: Man_loadurl_getnpdata = loadurl.getdata()
        if not pager.compare(hashdg):
            return retempty
        pagerstr: str = pager.gzdecompress_string()
        ret: typing.Final = Np_getstring_pagerurl(pagerstr=pagerstr, gzbys=b'')
        return ret


class Main_manXXYY(object):
    version:     typing.Final[str] = '0.0.9'
    versiondate: typing.Final[str] = '13 Jan 2025'

    def __init__(self):
        self._manenv_os2: str = ''
        self._manenv_lang: str = ''
        self._manenv_arch: str = ''
        self._cmdname: str = ''
        return

    @property
    def manenv_os2(self) -> str:
        return self._manenv_os2

    @property
    def manenv_lang(self) -> str:
        return self._manenv_lang

    @property
    def manenv_arch(self) -> str:
        return self._manenv_arch

    @property
    def cmdname(self) -> str:
        return self._cmdname

    @staticmethod
    def show_helpmes(os2: str, lang: str):
        version: str = Main_manXXYY.version
        versiondate: str = Main_manXXYY.versiondate
        langptn: dict = {'eng': 'English', 'jpn': 'Japanese'}
        language: str = langptn[lang]
        cmdnames: dict = {('fb', 'eng'): 'manenfb', ('fb', 'jpn'): 'manjpfb',
                          ('ob', 'eng'): 'manenob'}
        cmdname: str = cmdnames[(os2, lang)]
        doclicenses: dict = {'fb': 'FDL License including a prohibition clause for AI training.',
                             'ob': '3-Clause BSD License including a prohibition clause for AI training.'}
        doclicense: str = doclicenses[os2]
        osnames: dict = {'fb': 'FreeBSD', 'ob': 'OpenBSD'}
        osname: str = osnames[os2]
        copyright_engmans: dict = {('fb', 'eng'): 'Copyright of man pages: FreeBSD Project.',
                                   ('ob', 'eng'): 'Copyright of man pages: The copyright belongs to the authors of the man pages.'}
        copyright_engman: str = copyright_engmans.get((os2, lang), '')
        meses: list = list()
        meses_eng: list = list()
        meses =\
            ['{0} written by MikeTurkey'.format(cmdname),
             'ver {0}, {1}'.format(version, versiondate),
             '2024-2025 Copyright MikeTurkey ALL RIGHT RESERVED.',
             'ABSOLUTELY NO WARRANTY.',
             'Software: GPLv3 License including a prohibition clause for AI training.',
             'Document: {0}'.format(doclicense),
             '{0} man documents were translated by MikeTurkey using Deep-Learning.'.format(
                 osname),
             '',
             'SYNOPSIS',
             '  {0} [OPT] [mannum] [name]'.format(cmdname),
             '',
             'Summary',
             '  {0} {1}-man Pager.'.format(osname, language),
             '',
             'Description',
             '  {0} is pager of {1} {2} man using python3.'.format(
                 cmdname, osname, language),
             '  The program does not store man-data and download it with each request.',
             '  Since it is a Python script, it is expected to run on many operating systems in the future.',
             '  We can read the {0} {1} man on many Operating Systems.'.format(
                 osname, language),
             '  There is man-data that is not fully translated, but this is currently by design.',
             '  Please note that I do not take full responsibility for the translation of the documents.',
             '',
             'Example',
             '  $ {0} ls'.format(cmdname),
             '      print ls man.',
             '  $ {0} 1 head'.format(cmdname),
             '      print head 1 section man.',
             '  $ {0} --version'.format(cmdname),
             '      Show the message',
             '  $ {0} --listman'.format(cmdname),
             '      Show man page list.',
             '  $ {0} --listman1'.format(cmdname),
             '      Show man 1 page list.',
             '  $ {0} --listos'.format(cmdname),
             '      Show os name list of man.',
             '']
        meses_eng =\
            ['{0} written by MikeTurkey'.format(cmdname),
             'ver {0}, {1}'.format(version, versiondate),
             '2024-2025 Copyright MikeTurkey ALL RIGHT RESERVED.',
             'ABSOLUTELY NO WARRANTY.',
             'Software: GPLv3 License including a prohibition clause for AI training.',
             '{0}'.format(copyright_engman),
             '',
             'SYNOPSIS',
             '  {0} [OPT] [mannum] [name]'.format(cmdname),
             '',
             'Summary',
             '  {0} {1}-man Pager.'.format(osname, language),
             '',
             'Description',
             '  {0} is pager of {1} {2} man using python3.'.format(
                 cmdname, osname, language),
             '  The program does not store man-data and download it with each request.',
             '  Since it is a Python script, it is expected to run on many operating systems in the future.',
             '  We can read the {0} {1} man on many Operating Systems.'.format(
                 osname, language),
             '',
             'Example',
             '  $ {0} ls'.format(cmdname),
             '      print ls man.',
             '  $ {0} 1 head'.format(cmdname),
             '      print head 1 section man.',
             '  $ {0} --version'.format(cmdname),
             '      Show the message',
             '  $ {0} --listman'.format(cmdname),
             '      Show man page list.',
             '  $ {0} --listman1'.format(cmdname),
             '      Show man 1 page list.',
             '  $ {0} --listos'.format(cmdname),
             '      Show os name list of man.',
             '']
        new_meses: list = list()
        new_meses = meses_eng if lang == 'eng' else meses
        for s in new_meses:
            print(s)
        exit(0)

    def set_manenv(self, os2: str, lang: str, arch: str):
        mmanfunc = Mmanfunc
        os2_ptn:  typing.Final[tuple] = ('fb', 'ob')
        lang_ptn: typing.Final[tuple] = ('eng', 'jpn')
        arch_ptn: typing.Final[tuple] = ('arm64',)
        errmes: str = ''
        if os2 not in os2_ptn:
            errmes = 'Error: Invalid os2 type. [{0}]'.format(os2)
            raise MmanStdError(errmes)
        if lang not in lang_ptn:
            errmes = 'Error: Invalid lang type. [{0}]'.format(lang)
            raise MmanStdError(errmes)
        if arch not in arch_ptn:
            errmes = 'Error: Invalid arch type. [{0}]'.format(arch)
            raise MmanStdError(errmes)
        self._manenv_os2 = os2
        self._manenv_lang = lang
        self._manenv_arch = arch
        self._cmdname = mmanfunc.createstr_cmdname(os2, lang, arch)
        return

    def check_terminal(self, lang: str):
        subr = _Main_man
        errmes: str = ''
        warnmes: str = ''
        if lang == 'eng':
            return
        enable_term: bool | None
        kind: str
        enable_term, kind = subr.enable_terminal()
        if enable_term == True:
            return
        elif enable_term == False:
            if kind == 'FreeBSD_vt':
                errmes = 'Error: Can not print on virtual console. e.g. /dev/ttyv0\n'\
                    '  Psendo Terminal only(X terminal, Network terminal). e.g. /dev/pts/0'
            elif kind == 'OpenBSD_vt':
                errmes = 'Error: Can not print on virtual console. e.g. /dev/ttyC0\n'\
                    '  Psendo Terminal only(X terminal, Network terminal). e.g. /dev/ttyp0'
            print(errmes, file=sys.stderr)
            exit(1)
        elif enable_term == None:
            warnmes = 'Warning: Not support terminal.'
            print(warnmes)
            return
        errmes = 'Error: Runtime Error in check_terminal()'
        print(errmes, file=sys.stderr)
        exit(1)

    @staticmethod
    def change_pager(lang: str):
        mainfunc = Mainfunc
        linuxid: str = ''
        if lang == 'eng':
            return
        if sys.platform == 'linux':
            linuxid = mainfunc.getid_linux()
        if linuxid == 'alpine':
            os.environ['PAGER'] = 'more'
            return
        return

    @staticmethod
    def make_initopt():
        opt = types.SimpleNamespace(manhashfpath='', mannum='', manname='',
                                    listos=False, listman=False, release='',
                                    listman1=False, listman2=False, listman3=False,
                                    listman4=False, listman5=False, listman6=False,
                                    listman7=False, listman8=False, listman9=False,
                                    showtmpdir=False, license=False)
        return opt

    def main(self, os2: str = '', lang: str = '', arch: str = '',
             gui: bool = False, manname: str = '', mannum: str = '', listman: str = '') -> str:
        mainfunc = Mainfunc
        _main_man = _Main_man
        mmanfunc = Mmanfunc
        self.set_manenv(os2, lang, arch)
        cache = Man_cache()
        cache.init(os2, lang, arch, self.version, self.versiondate)
        cache.mktempdir_ifnot()
        if not gui:
            arg1, arg2, opt = self.create_mainargs()
            vernamekey = opt.release if opt.release != '' else '@LATEST-RELEASE'
            if opt.listos:
                _main_man.show_listos(self.manenv_os2, self.manenv_lang, self.manenv_arch, cache,
                                      self.version, self.versiondate)
                exit(0)
            if opt.listman:
                _main_man.show_listman(vernamekey, self.manenv_os2, self.manenv_lang,
                                       self.manenv_arch, False, cache, self.version, self.versiondate)
            chklist: list = [False, opt.listman1, opt.listman2, opt.listman3, opt.listman4,
                             opt.listman5, opt.listman6, opt.listman7, opt.listman8, opt.listman9]
            if any(chklist):
                n: int = chklist.index(True)
                if 1 <= n <= 9:
                    _main_man.show_listman_n(n, vernamekey, self.manenv_os2, self.manenv_lang,
                                             self.manenv_arch, False, cache, self.version, self.versiondate)
                errmes = 'Error: Runtime Error. Invalid --listman[N]'
                raise MmanStdError(errmes)
            if opt.license:
                _main_man.show_license(os2, lang, arch)
            self.check_terminal(lang)
            if arg2 == '':
                opt.manname = arg1
            else:
                opt.mannum = arg1
                opt.manname = arg2
        if gui:
            opt = self.make_initopt()
            opt.manname = manname  # e.g. args: ls
            opt.mannum = mannum
            vernamekey = opt.release if opt.release != '' else '@LATEST-RELEASE'
        s: str = ''
        if gui == True and listman == 'all':
            s = _main_man.show_listman(vernamekey, self.manenv_os2, self.manenv_lang,
                                       self.manenv_arch, gui, cache, self.version, self.versiondate)
            return s
        chktpl: tuple = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        if gui == True and (listman in chktpl):
            n = int(listman)
            s = _main_man.show_listman_n(n, vernamekey, self.manenv_os2, self.manenv_lang,
                                         self.manenv_arch, gui, cache, self.version, self.versiondate)
            return s
        http_header: Opt_http_header = Opt_http_header()
        http_header.x_mman_enable = 'YES'
        http_header.user_agent = mmanfunc.createstr_cmdname(
            os2, lang, arch) + '/{0}'.format(self.version)
        rooturls = cache.load_rooturls()
        roottomlobj = Man_roottoml()
        roottomlobj.og_vernamekey = vernamekey
        roottomlobj.og_manhashfpath = opt.manhashfpath
        roottomlobj.og_roottomlfpath = ''
        roottomlobj.og_manenv_os2 = self.manenv_os2
        roottomlobj.og_manenv_lang = self.manenv_lang
        roottomlobj.og_manenv_arch = self.manenv_arch
        roottomlobj.og_cmdversion = self.version
        roottomlobj.og_cmddate = self.versiondate
        roottomlobj.og_rooturls = cache.load_rooturls()
        roottomlobj.og_http_header = http_header
        tomldic = roottomlobj.make()
        print_fastestdomain = False
        if print_fastestdomain:
            print('fastestdomain: ', roottomlobj.fastestdomain)
        cache.store_rooturls(roottomlobj.rooturls)
        http_header.x_mman_roottomlid = roottomlobj.og_http_header.x_mman_roottomlid
        http_header.x_mman_mantomlid = roottomlobj.og_http_header.x_mman_mantomlid
        mantomlobj = Man_mantoml()
        mantomlobj.og_tomldic = tomldic.copy()
        mantomlobj.og_osname_root = roottomlobj.osname
        mantomlobj.og_mannum = opt.mannum
        mantomlobj.og_manname = opt.manname
        mantomlobj.og_baseurls = roottomlobj.baseurls
        mantomlobj.og_fnamemode = 'hash'
        manpg: tuple = mantomlobj.make()
        pagerurls: tuple = manpg.pagerurls
        hashdg: str = manpg.hashdg
        if len(manpg.pagerurls) == 0 and gui == False:
            errmes = 'Error: Not found the manual name. [{0}]'.format(
                opt.manname)
            raise MmanStdError(errmes)
        elif len(manpg.pagerurls) == 0 and gui == True:
            return ''
        pagerstr: str = ''
        gzbys: bytes = b''
        pcache = Man_pagercache()
        pcache.init(cache.tmpdir)
        pagerurl: str = manpg.pagerurls[0]
        hit, pagerstr = pcache.get_pager(pagerurl)
        hit = False
        if hit != True:
            pagerstr, gzbys = _main_man.getstring_pagerurl(manpg.pagerurls, manpg.hashdg,
                                                           http_header,
                                                           roottomlobj.fastestdomain)
        if pagerstr == '':
            errmes = 'Error: Not found the url. [{0}]'.format(pagerurl)
            raise MmanStdError(errmes)
        pcache.store_pager(hit, pagerurl, gzbys)
        if gui:
            cache.remove_oldcache()
            return pagerstr
        s = pagerstr
        if sys.platform == 'darwin':
            s = unicodedata.normalize('NFD', s)
        elif sys.platform == 'win32':
            s = unicodedata.normalize('NFC', s)
        s = _main_man.norm_punctuation(s)
        self.change_pager(lang)
        pydoc.pager(s)
        print('OSNAME(man):', mantomlobj.osname)
        print(roottomlobj.message)
        cache.remove_oldcache()
        if opt.showtmpdir:
            print('tmpdir:', cache.tmpdir)
        exit(0)

    def create_mainargs(self) -> [str, str, types.SimpleNamespace]:
        opt = self.make_initopt()
        arg1 = ''
        arg2 = ''
        on_manhash = False
        on_release = False
        listmandict: dict = {'--listman1': 'listman1', '--listman2': 'listman2',
                             '--listman3': 'listman3', '--listman4': 'listman4',
                             '--listman5': 'listman5', '--listman6': 'listman6',
                             '--listman7': 'listman7', '--listman8': 'listman8',
                             '--listman9': 'listman9'}
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
            if arg in ('--help', '-h'):
                self.show_helpmes(self.manenv_os2, self.manenv_lang)
                exit(0)
            if arg == '--version':
                print(self.version)
                exit(0)
            if arg == '--showtmpdir':
                opt.showtmpdir = True
                continue
            if arg == '--listos':
                opt.listos = True
                break
            if arg == '--listman':
                opt.listman = True
                break
            if arg == '--license':
                opt.license = True
                break
            if arg in listmandict.keys():
                setattr(opt, listmandict[arg], True)
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
        return arg1, arg2, opt


class Main_mman(object):
    version: str = Main_manXXYY.version
    versiondate: str = Main_manXXYY.versiondate

    def show_helpmes(self):
        version: str = self.version
        versiondate: str = self.versiondate
        meses: typing.Final[list] =\
            ['mman written by MikeTurkey',
             'ver {0}, {1}'.format(version, versiondate),
             '2024-2025 Copyright MikeTurkey ALL RIGHT RESERVED.',
             'ABSOLUTELY NO WARRANTY.',
             'Software: GPLv3 License including a prohibition clause for AI training.',
             '',
             'Summary',
             '  Multi-Language, Multi-Platform Man Pager',
             '  Choose your language.',
             '',
             'How to use.',
             '  1) Select your language and platform.',
             '     FreeBSD, English -> manenfb',
             '  2) Run manpage command.',
             '     $ python3.xx -m manenfb test',
             '     or',
             '     $ manenfb test',
             '  3) More Information.',
             '     $ python3.xx -m manenfb --help',
             '',
             'English:',
             '  manenfb: FreeBSD English man pager.',
             '  manenob: OpenBSD English man pager.',
             '',
             'Japanese:',
             '  manjpfb: FreeBSD Japanese man pager.',
             '']
        for s in meses:
            print(s)
        return

    def main(self):
        for arg in sys.argv[1:]:
            if arg == '--version':
                print(self.version)
                exit(0)
            if arg == '--help':
                break
        self.show_helpmes()
        exit(0)


def main_manenfb():
    cls = Main_manXXYY()
    try:
        cls.main(os2='fb', lang='eng', arch='arm64')
    except MmanStdError as e:
        print(e, file=sys.stderr)
        exit(1)
    return


def main_manjpfb():
    cls = Main_manXXYY()
    try:
        cls.main(os2='fb', lang='jpn', arch='arm64')
    except MmanStdError as e:
        print(e, file=sys.stderr)
        exit(1)
    return


def main_manenob():
    cls = Main_manXXYY()
    try:
        cls.main(os2='ob', lang='eng', arch='arm64')
    except MmanStdError as e:
        print(e, file=sys.stderr)
        exit(1)
    return


def main_mman():
    cls = Main_mman()
    cls.main()
    return


if __name__ == '__main__':
    main_mman()
    exit(0)
