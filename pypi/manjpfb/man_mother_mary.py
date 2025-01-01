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


class MmanStdError(Exception):
    pass


class Mainfunc(object):
    @staticmethod
    def os2_to_general_osname(os2: str) -> str:
        s: str = Mainfunc.os2dict.get(os2, '')
        return s

    @staticmethod
    def getid_linux() -> str:
        if sys.platform != 'linux':
            return ''
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
                raise MmanStdError(errmes)
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
                    raise MmanStdError(errmes)
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
                    raise MmanStdError(errmes)
            if isinstance(urls, list) != True:
                errmes = 'Error: urls on root.toml is NOT list type.'
                raise MmanStdError(errmes)
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
                raise MmanStdError(errmes)
            except urllib.error.HTTPError as e:
                errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
                raise MmanStdError(errmes)
            except Exception as e:
                errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(
                    e, urlpath)
                raise MmanStdError(errmes)
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
                raise MmanStdError(errmes)
            except urllib.error.HTTPError as e:
                errmes = 'Error: HTTP Error. {0}, URL: {1}'.format(e, urlpath)
                raise MmanStdError(errmes)
            except Exception as e:
                errmes = 'Error: Runtime Error. {0}, URL: {1}'.format(
                    e, urlpath)
                raise MmanStdError(errmes)
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


class _Mmanfunc_createstr(object):
    @staticmethod
    def createstr_cmdname(os2: str, lang: str, arch: str) -> str:
        mmanfunc = Mmanfunc
        errmes: str = ''
        if mmanfunc.os2dict.get(os2, False) == False:
            errmes = 'Error: Not found os2. [{0}]'.format(os2)
            raise MmanStdError(errmes)
        lang2: str = mmanfunc.lang2dict.get(lang, '')
        if lang2 == '':
            errmes = 'Error: Not found lang. [{0}]'.format(lang)
            raise MmanStdError(errmes)
        cmdname: str = 'man{0}{1}'.format(lang2, os2)
        return cmdname

    @staticmethod
    def createstr_license(os2: str, lang: str, arch: str, gui: bool = False, mkall: bool = False) -> str:
        mmanfunc = Mmanfunc
        errmes: str = ''
        if mmanfunc.os2dict.get(os2, '') == '':
            errmes = 'Error: Not found os2. [{0}]'.format(os2)
            raise MmanStdError(errmes)
        cmdname: typing.Final[str] = mmanfunc.createstr_cmdname(
            os2, lang, arch)
        cmdsummary: typing.Final[str] = mmanfunc.createstr_cmdsummary(
            os2, lang, arch)
        s: str = ''
        license_list: list = list()
        s = MMAN_CONSTANT_SOFTWARE_LICENSE_STRING
        s = s.format(cmdname, cmdsummary)
        license_list.append(s)
        s = MMAN_CONSTANT_DOCLICENSE_OWNERS
        license_list.append(s)
        chklist: list = [(os2 == 'fb' and lang != 'eng'), gui, mkall]
        if any(chklist) == True:
            s = MMAN_CONSTANT_DOCLICENSE_TRANSRATED_FREEBSD_MAN
            license_list.append(s)
        chklist: list = [(os2 == 'fb' and lang == 'eng'), gui, mkall]
        if any(chklist) == True and lang == 'eng':
            s = MMAN_CONSTANT_DOCLICENSE_FREEBSD_ENGLISH_MAN
            license_list.append(s)
        chklist: list = [(os2 == 'ob' and lang == 'eng'), gui, mkall]
        if any(chklist) == True:
            s = MMAN_CONSTANT_DOCLICENSE_OPENBSD_ENGLISH_MAN
            license_list.append(s)
        retstr: typing.Final[str] = ''.join(license_list)
        return retstr

    @staticmethod
    def createstr_cmdsummary(os2, lang, arch, mmangui: bool = False,
                             mmancui: bool = False) -> str:
        mmanfunc = Mmanfunc
        retstr: str = ''
        if mmancui:
            retstr = 'Multi-Language, Multi-Platform Man Pagers.'
            return retstr
        if mmangui:
            retstr = 'Multi-Language, Multi-Platform Man Pager on GUI.'
            return retstr
        longosname: str = mmanfunc.os2_to_long_osname(os2, erraction=True)
        language: str = mmanfunc.lang3_to_language(lang, erraction=True)
        retstr: str = '{0} {1} Man Pager.'.format(longosname, language)
        return retstr


class Mmanfunc(object):
    os2dict: typing.Final[dict] = {'fb': ('FreeBSD', 'FreeBSD'),
                                   'ob': ('OpenBSD', 'OpenBSD'),
                                   'al': ('AlpnLNX', 'Alpine Linux'),
                                   'dl': ('DebGLNX', 'Debian GNU/Linux')}
    longlangdict: typing.Final[dict] = {'eng': 'English', 'jpn': 'Japanese'}
    lang2dict: typing.Final[dict] = {'eng': 'en', 'jpn': 'jp'}
    iso_639_3_codes: typing.Final[tuple] = (
        "aar", "abk", "ace", "ach", "ada", "ady", "afa", "afh", "afr", "ain", "aka", "akk",
        "ale", "alg", "alt", "amh", "ang", "anp", "apa", "ara", "arc", "arg", "arn", "arp",
        "art", "arw", "asm", "ast", "ath", "aus", "ava", "ave", "awa", "aym", "aze", "bad",
        "bai", "bak", "bal", "bam", "ban", "bas", "bat", "bej", "bel", "bem", "ben", "ber",
        "bho", "bih", "bik", "bin", "bis", "bla", "bnt", "bos", "bra", "bre", "btk", "bua",
        "bug", "bul", "bur", "byn", "cad", "cai", "car", "cat", "cau", "ceb", "cel", "ces",
        "cha", "chb", "che", "chg", "chi", "chk", "chm", "chn", "cho", "chp", "chr", "chu",
        "chv", "chy", "cmc", "cnr", "cop", "cor", "cos", "cpe", "cpf", "cpp", "cre", "crh",
        "crp", "csb", "cus", "cym", "cze", "dak", "dan", "dar", "day", "del", "den", "deu",
        "dgr", "din", "div", "doi", "dra", "dsb", "dua", "dum", "dyu", "dzo", "efi", "egy",
        "eka", "ell", "elx", "eng", "enm", "epo", "est", "eus", "ewe", "ewo", "fan", "fao",
        "fas", "fat", "fij", "fil", "fin", "fiu", "fon", "fra", "fre", "frm", "fro", "frr",
        "frs", "fry", "ful", "fur", "gaa", "gay", "gba", "gem", "gez", "gil", "gla", "gle",
        "glg", "glv", "gmh", "goh", "gon", "gor", "got", "grb", "grc", "gre", "grn", "gsw",
        "guj", "gwi", "hai", "hat", "hau", "haw", "heb", "her", "hil", "him", "hin", "hit",
        "hmn", "hmo", "hrv", "hsb", "hun", "hup", "hye", "iba", "ibo", "ido", "iii", "ijo",
        "iku", "ile", "ilo", "ina", "ind", "inh", "ipk", "isl", "ita", "jav", "jbo", "jpn",
        "jpr", "jrb", "kaa", "kab", "kac", "kal", "kam", "kan", "kar", "kas", "kat", "kau",
        "kaw", "kaz", "kbd", "kha", "khi", "khm", "kho", "kik", "kin", "kir", "kmb", "kok",
        "kom", "kon", "kor", "kos", "kpe", "krc", "krl", "kro", "kru", "kua", "kum", "kur",
        "kut", "lad", "lah", "lam", "lao", "lat", "lav", "lez", "lim", "lin", "lit", "lol",
        "loz", "ltz", "lua", "lub", "lug", "lui", "lun", "luo", "lus", "mad", "mag", "mah",
        "mai", "mak", "mal", "man", "mao", "map", "mar", "mas", "mdf", "mdr", "men", "mga",
        "mic", "min", "mis", "mkd", "mkh", "mlg", "mlt", "mnc", "mni", "mno", "moh", "mon",
        "mos", "mri", "msa", "mul", "mun", "mus", "mwl", "mwr", "mya", "myn", "myv", "nah",
        "nai", "nap", "nau", "nav", "nbl", "nde", "ndo", "nds", "nep", "new", "nia", "nic",
        "niu", "nld", "nno", "nob", "nog", "non", "nor", "nqo", "nso", "nub", "nwc", "nya",
        "nym", "nyn", "nyo", "nzi", "oci", "oji", "ori", "orm", "osa", "oss", "ota", "oto",
        "paa", "pag", "pal", "pam", "pan", "pap", "pau", "peo", "phi", "phn", "pli", "pol",
        "pon", "por", "pra", "pro", "pus", "que", "raj", "rap", "rar", "roa", "roh", "rom",
        "ron", "rum", "run", "rup", "rus", "sad", "sag", "sah", "sai", "sal", "sam", "san",
        "sas", "sat", "scn", "sco", "sel", "sem", "sga", "sgn", "shn", "sid", "sin", "sio",
        "sit", "sla", "slk", "slo", "slv", "sma", "sme", "smi", "smj", "smn", "smo", "sms",
        "sna", "snd", "snk", "sog", "som", "son", "sot", "spa", "sqi", "srd", "srn", "srp",
        "srr", "ssa", "ssw", "suk", "sun", "sus", "sux", "swa", "swe", "syc", "syr", "tah",
        "tam", "tat", "tel", "tem", "ter", "tet", "tgk", "tgl", "tha", "tib", "tig", "tir",
        "tiv", "tkl", "tlh", "tli", "tmh", "tog", "ton", "tpi", "tsi", "tsn", "tso", "tuk",
        "tum", "tur", "tut", "tvl", "twi", "tyv", "udm", "uga", "uig", "ukr", "umb", "und",
        "urd", "uzb", "vai", "ven", "vie", "vol", "vot", "wak", "wal", "war", "was", "wel",
        "wln", "wol", "xal", "xho", "yao", "yap", "yid", "yor", "ypk", "zap", "zbl", "zen",
        "zgh", "zha", "zho", "zul", "zun", "zza")
    __cls = _Mmanfunc_createstr
    createstr_cmdname = __cls.createstr_cmdname
    createstr_license = __cls.createstr_license
    createstr_cmdsummary = __cls.createstr_cmdsummary

    @staticmethod
    def os2_to_long_osname(os2: str, erraction: bool = False) -> str:
        t: tuple = Mmanfunc.os2dict.get(os2, tuple())
        s: str = t[1] if len(t) == 2 else ''
        if erraction == True and s == '':
            errmes: str = 'Error: Not found os2dict key. [{0}]'.format(os2)
            raise MmanStdError(errmes)
        return s

    @staticmethod
    def long_osname_to_os2(losname: str, erraction: bool = False) -> str:
        templist: list = [os2 for os2,
                          t in Mmanfunc.os2dict.items() if t[1] == losname]
        if len(templist) == 0:
            if erraction:
                errmes: str = 'Error: Not found os2dict value. [{0}]'.format(
                    losname)
                raise MmanStdError(errmes)
            else:
                return ''
        s: str = templist[0]
        return s

    @staticmethod
    def lang3_to_language(lang3: str, erraction: bool = False) -> str:
        s: str = Mmanfunc.longlangdict.get(lang3, '')
        if erraction == True and s == '':
            errmes: str = 'Error: Not found language. [{0}]'.format(lang3)
            raise MmanStdError(errmes)
        return s

    @staticmethod
    def language_to_lang3(language: str, erraction: bool = False) -> str:
        templist: list = [
            lang3 for lang3, longlang in Mmanfunc.longlangdict.items() if language == longlang]
        if len(templist) == 0:
            if erraction:
                errmes: str = 'Error: Not found longlangdict value. [{0}]'.format(
                    language)
                raise MmanStdError(errmes)
            else:
                return ''
        s: str = templist[0]
        return s


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
                raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
        if self.tmpdir.is_dir() != True:
            errmes = 'Error: Not found cache directory. [{0}]'.format(
                self.tmpdir)
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
        fname: str = splitted[1]
        ptn: str = r'man.+(?:amd64|arm64)_hash_2[0-9]{3}[0-1][0-9][0-3][0-9]\.toml\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not man.toml.gz format. [{0}]'.format(fname)
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
        if self.tmpdir.is_dir() != True:
            errmes = 'Error: Not found cache directory. [{0}]'.format(
                self.tmpdir)
            raise MmanStdError(errmes)
        splitted: list = url.rsplit('/', 1)
        if len(splitted) != 2:
            errmes = 'Error: Not url format. [{0}]'.format(url)
            raise MmanStdError(errmes)
        fname: str = splitted[1]
        ptn = r'man.+(?:amd64|arm64)_hash_2[0-9]{3}[0-1][0-9][0-3][0-9]\.toml\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not man.toml.gz format. [{0}]'.format(fname)
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
        if self.tmpdir.is_dir() != True:
            errmes = 'Error: Not found cache directory. [{0}]'.format(
                self.tmpdir)
            raise MmanStdError(errmes)
        splitted: list = url.rsplit('/', 2)
        if len(splitted) != 3:
            errmes = 'Error: Not url format. [{0}]'.format(url)
            raise MmanStdError(errmes)
        fname: str = splitted[2]
        hashdg: str = splitted[1]
        ptn: str = r'[0-9a-f]{64}$'
        if re.match(ptn, hashdg) == None:
            errmes = 'Error: Not hash digest format. [{0}]'.format(hashdg)
            raise MmanStdError(errmes)
        ptn = r'[0-9a-f]{6}\.[1-9a-z]\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not pager file format. [{0}]'.format(fname)
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
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
            raise MmanStdError(errmes)
        fname: str = splitted[1]
        ptn: str = r'[0-9a-f]{6}\.[1-9a-z]\.gz$'
        if re.match(ptn, fname) == None:
            errmes = 'Error: Not pager format. [{0}]'.format(fname)
            raise MmanStdError(errmes)
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


MMAN_CONSTANT_SOFTWARE_LICENSE_STRING: typing.Final[str] =\
    '''
{0}, {1}
COPYRIGHT 2024-2025 MikeTurkey 
Contact: voice[ATmark]miketurkey.com
License: GPLv3 License including a prohibition clause for AI training.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE
In addition to the rights granted under the applicable license(GPL-3),
you are expressly prohibited from using any form of machine learning,
artificial intelligence, or similar technologies to analyze, process,
or extract information from this software, or to create derivative
works based on this software.
This prohibition includes, but is not limited to, training machine
learning models, neural networks, or any other automated systems using
the code or output of this software.
The purpose of this prohibition is to protect the integrity and
intended use of this software. If you wish to use this software for
machine learning or similar purposes, you must seek explicit written
permission from the copyright holder.
see also 
    GPL-3 Licence: https://www.gnu.org/licenses/gpl-3.0.html.en
    Mike Turkey.com: https://miketurkey.com/
'''
MMAN_CONSTANT_DOCLICENSE_TRANSRATED_FREEBSD_MAN: typing.Final[str] =\
    '''
COPYRIGHT 2024-2025 MikeTurkey 
FreeBSD man documents were translated by MikeTurkey using Deep-Learning.
Contact: voice[ATmark]miketurkey.com
License: FreeBSD Document License including a prohibition clause
	 for AI training.
Redistribution and use in source (AsciiDoc) and 'compiled' forms (HTML,
PDF, EPUB and so forth) with or without modification, are permitted
provided that the following conditions are met:
1.  Redistributions of source code (AsciiDoc) must retain the above
    copyright notice, this list of conditions and the following
    disclaimer as the first lines of this file unmodified.
2.  Redistributions in compiled form (Converted to PDF, EPUB and other
    formats) must reproduce the above copyright notice, this list of
    conditions and the following disclaimer in the documentation and/or
    other materials provided with the distribution.
3.  ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE:  
    You may not use this documentation or any part thereof for the
    purpose of training or developing machine learning models,
    algorithms, or systems, without prior written permission from the
    copyright holder. This prohibition applies to any use that
    involves automated extraction of knowledge or features from the
    documentation, including but not limited to training neural
    networks, statistical models, or other artificial intelligence
    technologies.
THIS DOCUMENTATION IS PROVIDED BY MIKETURKEY "AS IS" AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL MIKETURKEY BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS DOCUMENTATION, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
Manual Pages
Some FreeBSD manual pages contain text from the IEEE Std 1003.1, 2004
Edition, Standard for Information Technology - Portable Operating System
Interface (POSIX®) specification. These manual pages are subject to the
following terms:
  The Institute of Electrical and Electronics Engineers and The Open
  Group, have given us permission to reprint portions of their
  documentation.
  In the following statement, the phrase "this text" refers to portions
  of the system documentation.
  Portions of this text are reprinted and reproduced in electronic form
  in the FreeBSD manual pages, from IEEE Std 1003.1, 2004 Edition,
  Standard for Information Technology - Portable Operating System
  Interface (POSIX), The Open Group Base Specifications Issue 6,
  Copyright© 2001-2004 by the Institute of Electrical and Electronics
  Engineers, Inc and The Open Group. In the event of any discrepancy
  between these versions and the original IEEE and The Open Group
  Standard, the original IEEE and The Open Group Standard is the referee
  document. The original Standard can be obtained online at
  https://www.opengroup.org/membership/forums/platform/unix.
  This notice shall appear on any product containing this material.
See also:
    FDL: https://www.freebsd.org/copyright/freebsd-doc-license/
    Mike Turkey: https://miketurkey.com/
'''
MMAN_CONSTANT_DOCLICENSE_OWNERS: typing.Final[str] =\
    '''
COPYRIGHT 2024-2025 MikeTurkey
Man documents were translated by MikeTurkey using Deep-Learning.
Contact: voice[ATmark]miketurkey.com
License: GFDL1.3 License including a prohibition clause for AI training.
Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.3
or any later version published by the Free Software Foundation;
with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
A copy of the license is included in the section entitled "GNU
Free Documentation License".
ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE
In addition to the rights granted under the GNU Free Documentation
License, Version 1.3, you are expressly prohibited from using any form
of machine learning, artificial intelligence, or similar technologies
to analyze, process, or extract information from this document, or to
create derivative works based on this document.
This prohibition includes, but is not limited to, training machine
learning models, neural networks, or any other automated systems using
the content of this document.
The purpose of this prohibition is to protect the integrity and
intended use of this document. If you wish to use this document for
machine learning or similar purposes, you must seek explicit written
permission from the copyright holder.
Additional Term: Documentation
"Documentation" refers to any written or electronic materials,
including but not limited to manuals, guides, help files, and any
other accompanying explanatory materials, that are provided or made
available along with the software. The Documentation may be in printed
or digital format and is an integral part of the software package.
The Documentation is licensed under the terms of the GNU Free
Documentation License (GFDL) version 1.3, a copy of which can be found
at [https://www.gnu.org/licenses/fdl-1.3.txt]. Users are granted the
right to copy, distribute, and/or modify the Documentation under the
terms of the GFDL, but not to modify it in any way that would cause
the Documentation to become subject to any license other than the
GFDL.
Users are expressly prohibited from sublicensing or otherwise
transferring their rights to the Documentation. Any reproduction,
distribution, or modification of the Documentation must retain the
notices and disclaimers of the GFDL.
This Additional Term forms an integral part of the overall software
document license and should be interpreted in conjunction with the
main terms and conditions outlined in the license agreement.
See also:
    GFDL1.3: https://www.gnu.org/licenses/fdl-1.3.txt
    Mike Turkey: https://miketurkey.com/
'''
MMAN_CONSTANT_DOCLICENSE_TRANSLATED_OPENBSD_MAN: typing.Final[str] =\
    '''
COPYRIGHT 2024-2025 MikeTurkey
OpenBSD man documents were translated by MikeTurkey using Deep-Learning.
Contact: voice[ATmark]miketurkey.com
License: 3-Clause BSD License including a prohibition clause
	 for AI training.
Redistribution and use of this documentation, with or without
modification, are permitted provided that the following conditions are
met:
1. Redistributions of the original documentation must retain the above
   copyright notice, this list of conditions, and the following
   disclaimer.
2. Redistributions of derivative works must reproduce the
   above copyright notice, this list of conditions, and the following
   disclaimer in the documentation and/or other materials provided with
   the redistribution.
3. Neither the name of the MikeTurkey nor the names
   of contributors may be used to endorse or promote derivative works
   without specific prior written permission.
4. ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE:
   You may not use this documentation or any part thereof for the purpose
   of training or developing machine learning models, algorithms, or
   systems, without prior written permission from the copyright
   holder. This prohibition applies to any use that involves automated
   extraction of knowledge or features from the documentation, including
   but not limited to training neural networks, statistical models, or
   other artificial intelligence technologies.
THIS DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDER(S) AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER(S) OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS DOCUMENTATION, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
'''
MMAN_CONSTANT_DOCLICENSE_FREEBSD_ENGLISH_MAN: typing.Final[str] =\
    '''
Copyright 1994-2025 The FreeBSD Project.
Redistribution and use in source (AsciiDoc) and 'compiled' forms (HTML,
PDF, EPUB and so forth) with or without modification, are permitted
provided that the following conditions are met:
1.  Redistributions of source code (AsciiDoc) must retain the above
    copyright notice, this list of conditions and the following
    disclaimer as the first lines of this file unmodified.
2.  Redistributions in compiled form (Converted to PDF, EPUB and other
    formats) must reproduce the above copyright notice, this list of
    conditions and the following disclaimer in the documentation and/or
    other materials provided with the distribution.
THIS DOCUMENTATION IS PROVIDED BY THE FREEBSD DOCUMENTATION PROJECT "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE FREEBSD
DOCUMENTATION PROJECT BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
Manual Pages
Some FreeBSD manual pages contain text from the IEEE Std 1003.1, 2004
Edition, Standard for Information Technology -  Portable Operating System
Interface (POSIX®) specification. These manual pages are subject to the
following terms:
  The Institute of Electrical and Electronics Engineers and The Open
  Group, have given us permission to reprint portions of their
  documentation.
  In the following statement, the phrase "this text" refers to portions
  of the system documentation.
  Portions of this text are reprinted and reproduced in electronic form
  in the FreeBSD manual pages, from IEEE Std 1003.1, 2004 Edition,
  Standard for Information Technology -  Portable Operating System
  Interface (POSIX), The Open Group Base Specifications Issue 6,
  Copyright© 2001-2004 by the Institute of Electrical and Electronics
  Engineers, Inc and The Open Group. In the event of any discrepancy
  between these versions and the original IEEE and The Open Group
  Standard, the original IEEE and The Open Group Standard is the referee
  document. The original Standard can be obtained online at
  https://www.opengroup.org/membership/forums/platform/unix.
  This notice shall appear on any product containing this material.
See also:
    FDL: https://www.freebsd.org/copyright/freebsd-doc-license/
'''
MMAN_CONSTANT_DOCLICENSE_OPENBSD_ENGLISH_MAN: typing.Final[str] =\
    '''
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of the University nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
The Institute of Electrical and Electronics Engineers and the American
National Standards Committee X3, on Information Processing Systems have
given us permission to reprint portions of their documentation.
In the following statement, the phrase ``this text'' refers to portions
of the system documentation.
Portions of this text are reprinted and reproduced in electronic form in
the second BSD Networking Software Release, from IEEE Std 1003.1-1988, IEEE
Standard Portable Operating System Interface for Computer Environments
(POSIX), copyright C 1988 by the Institute of Electrical and Electronics
Engineers, Inc.  In the event of any discrepancy between these versions
and the original IEEE Standard, the original IEEE Standard is the referee
document.
In the following statement, the phrase ``This material'' refers to portions
of the system documentation.
This material is reproduced with permission from American National
Standards Committee X3, on Information Processing Systems.  Computer and
Business Equipment Manufacturers Association (CBEMA), 311 First St., NW,
Suite 500, Washington, DC 20001-2178.  The developmental work of
Programming Language C was completed by the X3J11 Technical Committee.
The views and conclusions contained in the software and documentation are
those of the authors and should not be interpreted as representing official
policies, either expressed or implied, of the Regents of the University
of California.
See also:
    OpenBSD Directory: /usr/shara/man/COPYRIGHT'''
