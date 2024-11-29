#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
######################################################################
####################  SOFTWARE LICENSE   #############################
######################################################################
#
# SNAKELAND, Instant python script installer.
# Copyright (C) 2023-2024 Mike Turkey
# contact: voice[ATmark]miketurkey.com
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
#     GPL-3 Licence, https://www.gnu.org/licenses/gpl-3.0.html.en
#     Mike Turkey.com, https://miketurkey.com
#

import sys
if sys.version_info.major == 3 and sys.version_info.minor < 4:
    errmes = 'Error: Need python 3.4 later. [python: {0}]'.format(
        sys.version.split(' ')[0])
    print(errmes, file=sys.stderr)
    exit(1)
import os
import time
import re
import shutil
import copy
import subprocess
import warnings
import hashlib
import string
import random
import unicodedata
import getpass
import glob


class Print_Derivative(object):
    @staticmethod
    def print_stderr(*mes, end='\n', pyexit: int = 0):
        meses: list = []
        meses = [unicodedata.normalize('NFD', s) for s in mes]
        [print(s, file=sys.stderr, end=end) for s in meses]
        if pyexit != 0:
            exit(pyexit)
        return

    @staticmethod
    def print_stdout(*mes, end='\n', file=sys.stdout):
        meses: list = []
        meses = [unicodedata.normalize('NFD', s) for s in mes]
        [print(s, file=file, end=end) for s in meses]
        return


print_err = Print_Derivative.print_stderr
print_mes = Print_Derivative.print_stdout


class Standalone(object):
    @staticmethod
    def removeprefix(ptn: str, raw: str) -> str:
        if raw.index(ptn) != 0:
            return raw

    @staticmethod
    def re_spanstring(matchobj) -> str:
        if matchobj == None:
            return ''
        matchobj_type = type(re.match('', ''))
        if isinstance(matchobj, matchobj_type) != True:
            errmes = 'matchobj is Not re.match object. [matchobj = {0}]'.format(
                repr(matchobj))
            raise TypeError(errmes)
        idx_s: int = 0
        idx_e: int = 0
        try:
            idx_s, idx_e = matchobj.span()
            matchedstr = matchobj.string[idx_s: idx_e]
        except:
            return ''
        return matchedstr


class Args_snakelands(object):
    def __init__(self):
        self.version: bool = False
        self.help: bool = False
        self.license: bool = False
        self.subcmd: str = ''
        self.config: str = ''
        self.later: str = ''
        self.older: str = ''
        self.latest: bool = False
        self.range: str = ''
        self.order: str = ''
        self._subcmds: list = ['install', 'uninstall', 'findpy3']
        self._pass_analyze: bool = False
        self._pass_check: bool = False
        self._pass_normalize: bool = False
        return

    def print_attribute(self):
        for k, v in self.__dict__.items():
            mes = '{0}= {1}'.format(k, v)
            print(mes)
        return

    def analyze(self):
        arg: str = ''
        errmes: str = ''
        on_later: bool = False
        on_older: bool = False
        on_range: bool = False
        on_order: bool = False
        for arg in sys.argv[1:]:
            if arg == '--license':
                self.license = True
                break
            if arg == '--version':
                self.version = True
                break
            if arg == '--help':
                self.help = True
                break
            if self.subcmd == '' and (arg in self._subcmds):
                self.subcmd = arg
                continue
            if self.subcmd == 'findpy3':
                if arg == '--latest':
                    self.latest = True
                    continue
                if on_later:
                    self.later = arg
                    on_later = False
                    continue
                if on_older:
                    self.older = arg
                    on_older = False
                    continue
                if on_range:
                    self.range = arg
                    on_range = False
                    continue
                if on_order:
                    self.order = arg
                    on_order = False
                    continue
                if arg == '--later':
                    on_later = True
                    continue
                if arg == '--older':
                    on_older = True
                    continue
                if arg == '--range':
                    on_range = True
                    continue
                if arg == '--order':
                    on_order = True
                    continue
            if self.config == '' and (self.subcmd in ['install', 'uninstall']):
                self.config = arg
                continue
            errmes = 'Error: Invalid argument. [{0}]'.format(arg)
            print_err(errmes)
            exit(1)
            continue
        chklst: list = [self.help, self.version, self.license]
        if self.subcmd == '' and chklst.count == 0:
            errmes = 'Error: Empty sub command.'
            print_err(errmes)
            exit(1)
        self._pass_analyze = True
        return

    def check(self):
        errmes: str = ''
        ptn: str = ''
        s: str = ''
        if self._pass_analyze != True:
            errmes = 'Error: The analyze() method is not passing.'
            print_err(errmes)
            exit(1)
        if self.version:
            Main_snakeland.show_version()
            exit(0)
        if self.help:
            Main_snakeland.show_help()
            exit(0)
        if self.license:
            Main_snakeland.show_license()
            exit(0)
        if self.subcmd == 'install':
            if os.path.isfile(self.config) != True and os.path.dirname(self.config):
                errmes = 'Error: Not found the config file. [{0}]'.format(
                    self.config)
                print_err(errmes)
                exit(1)
            try:
                with open(self.config, 'rt', encoding='utf-8') as fp:
                    fp.read(1)
            except:
                errmes = 'Error: Config is not readable.'
                print_err(errmes)
                exit(1)
        if self.later != '':
            ptn = r'3\.[1-9]?[0-9]'
            if re.match(ptn, self.later) == None:
                errmes = 'Error: Invalid --later option value. e.g. --later 3.6 [{0}]'.format(
                    self.later)
                print_err(errmes)
                exit(1)
        if self.older != '':
            ptn = r'3\.[1-9]?[0-9]'
            if re.match(ptn, self.older) == None:
                errmes = 'Error: Invalid --older option value. e.g. --older 3.6 [{0}]'.format(
                    self.older)
                print_err(errmes)
                exit(1)
        if self.range != '':
            ptn = r'3\.[1-9]?[0-9]\-3\.[1-9]?[0-9]'
            if re.match(ptn, self.range) == None:
                errmes = 'Error: Invalid --range option value. e.g. --range 3.6-3.10 [{0}]'.format(
                    self.range)
                print_err(errmes)
                exit(1)
        if self.order != '':
            ptn = r'3\.[1-9]?[0-9]'
            splitted = self.order.split(',')
            for s in splitted:
                if re.match(ptn, s) == None:
                    errmes = 'Error: Invalid --order option value. e.g. --order 3.6,3.7,3.8 [{0}]'.format(
                        self.order)
                    print_err(errmes)
                    exit(1)
        if self.subcmd == 'findpy3':
            templist = [self.later != '', self.older != '',
                        self.latest == True, self.range != '', self.order != '']
            if templist.count(True) >= 2:
                errmes = 'Error: Too many findpy3 option.'
                print_err(errmes)
                exit(1)
            if templist.count(True) == 0:
                errmes = 'Error: Empty findpy3 option.'
                print_err(errmes)
                exit(1)
        self._pass_check = True
        return

    def normalize(self):
        errmes: str = ''
        if self._pass_analyze != True:
            errmes = 'Error: The analyze() method is not passing.'
            print_err(errmes)
            exit(1)
        if self._pass_check != True:
            errmes = 'Error: The check() method is not passing.'
            print_err(errmes)
            exit(1)
        self.config = os.path.abspath(os.path.expanduser(self.config))
        self._pass_normalize = True
        return


class ConfParser_snakeland():
    def __init__(self):
        self.dfdict: dict = dict()
        self.srcdict: dict = dict()
        self._dfdict_keys: list = ['OSCHECK', 'DSTBASEDIR', 'INSTALLCMD', 'CMDNAME',
                                   'SHEBANG', 'TARGETPY3', 'TARGETCMD', 'PY3VERSION']
        self._srcdict_keys: list = ['DSTDIR', 'DSTABSDIR', 'FMODE']
        self._rawconflst: list = []
        self._pass_analyze: bool = False
        self._pass_check: bool = False
        self._pass_normalize: bool = False
        return

    def print_attribute(self):
        for k, v in self.__dict__.items():
            mes = '{0}= {1}'.format(k, v)
            print(mes)
        return

    @staticmethod
    def _get_sectionname(rawrow: str) -> str:
        row: str = rawrow.strip()
        if row.startswith('[') != True:
            return ''
        if row.endswith(']') != True:
            return ''
        s: str = row[1:len(row)-1]
        return s

    @staticmethod
    def _conflist2list(var: str) -> list:
        s: str = ''
        i: int = 0
        varstrings: str = ''
        s = var.lstrip("[")
        varstrings = s.rstrip("]")
        qte_idxs: int = 0
        qte_idxe: int = 0
        qte_mark: str = ''
        close_qte: bool = False
        retlist: list = list()
        for i in range(len(varstrings)):
            s = varstrings[i]
            if close_qte:
                qte_idxs = 0
                qte_idxe = 0
                qte_mark = ''
                close_qte = False
                continue
            if s == "'":
                if qte_mark == '':
                    qte_idxs = i
                    qte_mark = "'"
                    continue
                elif qte_mark == "'":
                    qte_idxe = i
                    close_qte = True
                    retlist.append(varstrings[qte_idxs + 1: qte_idxe - 1 + 1])
                    continue
        return retlist

    def _load_in_section(self, secname: str, dictkeys: list) -> dict:
        conflst: list = self._rawconflst
        retdict: dict = dict()
        secname_cfg: str = ''
        errmes: str = ''
        on_section: bool = False
        on_section = True if secname == '' or secname == 'default' else False
        for rawrow in conflst:
            row = rawrow
            if row.startswith('#') == True or row == '':
                continue  # Comment
            if row.startswith('['):
                secname_cfg = self._get_sectionname(row)
                if secname_cfg == secname:
                    on_section = True
                    continue
                else:
                    on_section = False
                    continue
            if on_section != True:
                continue
            if row[0] not in string.ascii_uppercase:
                errmes = 'Error: Invalid Config format. [{0}]'.format(row)
                print_err(errmes)
                exit(1)
            splitted = row.split('=', maxsplit=1)
            if len(splitted) != 2:
                errmes = 'Error: Invalid Config format. [{0}]'.format(row)
                print_err(errmes)
                exit(1)
            s = splitted[0]
            varname = s.strip()
            s = splitted[1]
            var = s.strip()
            if varname not in dictkeys:
                errmes = 'Error: Unknown config variable name. [{0},{1}]'.format(
                    varname, row)
                print_err(errmes)
                exit(1)
            if var[0] == "'":
                if var[len(var) - 1] == "'":
                    var = var.strip("'")
                else:
                    errmes = 'Error: Quote mark is not in place. [{0}]'.format(
                        row)
                    print_err(errmes)
                    exit(1)
            if var[0] == "[" and var[len(var) - 1] == "]":
                var = self._conflist2list(var)
            retdict[varname] = var
        return retdict

    def _load_df(self):
        dictkeys: list = self._dfdict_keys
        retdict: dict = dict()
        retdict = self._load_in_section('default', dictkeys)
        self.dfdict = retdict
        return

    def _load_src(self):
        def forif(row: str) -> bool:
            if row.startswith('#') == True or row == '':
                return False  # Comment
            if row.startswith('['):
                return True
            return False
        conflst: list = self._rawconflst
        dictkeys: list = self._srcdict_keys
        retdict: dict = dict()
        vdict: dict = dict()
        secname: str = ''
        secnames: list = list()
        secnames = [self._get_sectionname(row)
                    for row in conflst if forif(row) == True]
        for secname in secnames:
            vdict = self._load_in_section(secname, dictkeys)
            retdict[secname] = vdict
        self.srcdict = retdict
        return

    def load(self, conf: str):
        def rowstrip(s: str) -> str:
            s = s.strip('\n')
            return s.strip()
        with open(conf, 'rt', encoding='utf-8') as fp:
            self._rawconflst = [rowstrip(row) for row in fp]
        self._load_df()
        self._load_src()
        return

    def analyze(self):
        dfdictkeys_es: list = ['CMDNAME', 'DSTBASEDIR']
        srcdictkeys_es: list = ['DSTDIR']
        dfdictkeys_opt: list = ['OSCHECK', 'INSTALLCMD',
                                'TARGETPY3', 'TARGETCMD', 'SHEBANG', 'PY3VERSION']
        srcdictkeys_opt: list = ['FMODE']
        dfdict: dict = self.dfdict
        srcdict: dict = self.srcdict
        errmes: str = ''
        key: str = ''
        for key in dfdictkeys_es:
            if dfdict.get(key, None) == None:
                errmes = 'Error: Not found {0} value on default section of config.'.format(
                    key)
                print_err(errmes)
                exit(1)
        for srcfpath, v in srcdict.items():
            for key in srcdictkeys_es:
                if v.get(key, None) == None:
                    errmes = 'Error: Not found {0} value on source file section of config. [{1}]'.format(
                        key, srcfpath)
                    print_err(errmes)
                    exit(1)
        for key in dfdict.keys():
            if key in dfdictkeys_es:
                continue
            if key not in dfdictkeys_opt:
                errmes = 'Error: Invalid {0} value on default section of config.'.format(
                    key)
                print_err(errmes)
                exit(1)
        for srcfpath, v in srcdict.items():
            for key in v.keys():
                if key in srcdictkeys_es:
                    continue
                if key not in srcdictkeys_opt:
                    errmes = 'Error: Invalid {0} value on source file section of config.'.format(
                        key)
                    print_err(errmes)
                    exit(1)
        key1: str = 'TARGETPY3'
        key2: str = 'TARGETCMD'
        on_key1: bool = True if dfdict.get(key1, None) != None else False
        on_key2: bool = True if dfdict.get(key2, None) != None else False
        if on_key1 != True and on_key2 != True:
            errmes = 'Error: Not found {0} or {1} value on default section of config.'.format(
                key1, key2)
            print_err(errmes)
            exit(1)
        if on_key1 == True and on_key2 == True:
            errmes = 'Error: The keys({0}, {1}) do not allow access at the same time.'.format(
                key1, key2)
            print_err(errmes)
            exit(1)
        self._pass_analyze = True
        return

    @staticmethod
    def _check_PY3VERSION(var: str):
        ptn: str = ''
        errmes: str = ''
        s: str = ''
        if var.startswith('latest'):
            return
        if var.endswith('later'):
            ptn = r'3\.[1-9]?[0-9][ ]?later'
            if re.match(ptn, var) == None:
                errmes = 'Error: Invalid PY3VERSION strings. [{0}]'.format(var)
                print_err(errmes)
                exit(1)
            return
        if var.endswith('older'):
            ptn = r'3\.[1-9]?[0-9][ ]?older'
            if re.match(ptn, var) == None:
                errmes = 'Error: Invalid PY3VERSION strings. [{0}]'.format(var)
                print_err(errmes)
                exit(1)
            return
        ptn = r'3\.[1-9]?[0-9][ ]*[-][ ]*3\.[1-9]?[0-9]'
        if re.match(ptn, var) != None:
            return
        ptn = r'3\.[1-9]?[0-9]'
        splitted: list = []
        if re.match(ptn, var) != None:
            splitted = var.split(' ')
            for s in splitted:
                if re.match(ptn, s) == None:
                    errmes = 'Error: Invalid PY3VERSION strings. [{0}]'.format(
                        var)
                    print_err(errmes)
                    exit(1)
            return
        errmes = 'Error: Invalid PY3VERSION strings. [{0}]'.format(var)
        print_err(errmes)
        exit(1)

    def check(self):
        errmes: str = ''
        ptn: str = ''
        dfdict: dict = self.dfdict
        srcdict: dict = self.srcdict
        if self._pass_analyze != True:
            errmes = 'Error: The analyze method has not passed yet.'
            print_err(errmes)
            exit(1)
        ptn = r'[a-zA-Z0-9\-\_]+$'
        varname: str = 'CMDNAME'
        var: str = dfdict.get(varname, '')
        if re.match(ptn, var) == None:
            errmes = 'Error: Not match pattern(A-Z, a-z, 0-9, "-", "_") of CMDNAME. [{0}]'.format(
                varname)
            print_err(errmes)
            exit(1)
        varname = 'DSTBASEDIR'
        value = dfdict.get(varname, '')
        dstbasedir: str = value
        if os.path.isdir(value) != True:
            try:
                os.makedirs(value, mode=0o755)
            except:
                errmes = 'Error: Can not make the DSTBASEDIR directory. [{0}]'.format(
                    value)
                print_err(errmes)
                exit(1)
        if os.path.isabs(value) != True:
            errmes = 'Error: DSTBASEDIR is NOT absolute path. [{0}]'.format(
                value)
            print_err(errmes)
            exit(1)
        varname = 'OSCHECK'
        var = dfdict.get(varname, '')
        oscheck_list: list = ['Darwin', 'Linux', 'FreeBSD']
        if var != '':
            for s in var:
                if s not in oscheck_list:
                    errmes = 'Error: Invalid OSCHECK value. [{0}]'.format(var)
                    print_err(errmes)
                    exit(1)
        varname = 'INSTALLCMD'
        var = dfdict.get(varname, '')
        if var != '':
            if os.path.isdir(var) != True:
                errmes = 'Error: Not found INSTALLCMD directory. [{0}]'.format(
                    var)
                print_err(errmes)
                exit(1)
        varname = 'TARGETPY3'
        var = dfdict.get(varname, '')
        if var != '':
            if os.path.isabs(var) != True:
                errmes = 'Error: TARGETPY3 path is NOT absolute path. [{0}]'.format(
                    var)
                print_err(errmes)
                exit(1)
            if var.find(dstbasedir) != 0:
                errmes = 'Error: TARGETPY3 path is NOT based on DSTBASEDIR. [{0}]'.format(
                    var)
                print_err(errmes)
                exit(1)
        varname = 'TARGETCMD'
        var = dfdict.get(varname, '')
        if var != '':
            if os.path.isabs(var) != True:
                errmes = 'Error: TARGETCMD path is NOT absolute path. [{0}]'.format(
                    var)
                print_err(errmes)
                exit(1)
            if var.find(dstbasedir) != 0:
                errmes = 'Error: TARGETCMD path is NOT based on DSTBASEDIR. [{0}]'.format(
                    var)
                print_err(errmes)
                exit(1)
        varname = 'SHEBANG'
        var = dfdict.get(varname, '')
        if var != '':
            if os.path.isfile(var) != True:
                errmes = 'Error: Not found SHEBANG path. [{0}]'.format(var)
                print_err(errmes)
                exit(1)
        varname = 'PY3VERSION'
        var = dfdict.get(varname, '')
        self._check_PY3VERSION(var)
        for srcfpath, vdict in srcdict.items():
            varname = 'DSTDIR'
            value = vdict.get(varname, '')
            if os.path.isabs(os.path.expanduser(value)) == True:
                pass
            else:
                if os.path.isabs(value) == True:
                    errmes = 'Error: DSTDIR is Not Absolute path. [{0}]'.format(
                        value)
                    print_err(errmes)
                    exit(1)
                valueabs = os.path.abspath(dstbasedir + '/' + value) + '/'
                if valueabs.find(dstbasedir) != 0:
                    errmes = 'Error: DSTDIR is Not based DSTBASEDIR. [{0}]'.format(
                        valueabs)
                    print_err(errmes)
                    exit(1)
            varname = 'FMODE'
            value = vdict.get(varname, '')
            if value != '':
                ptn = r'[0-7][0-7][0-7]'
                if re.match(ptn, value) == None:
                    errmes = 'Error: FMODE pattern(e.g. 644, 755) is mismatched. [{0}]'.format(
                        value)
                    print_err(errmes)
                    exit(1)
        self._pass_check = True
        return

    @staticmethod
    def _normalize_pyminor(py3ver: str) -> int:
        splitted: list = py3ver.split('.', maxsplit=1)
        return int(splitted[1])

    def _normalize_PY3VERSION(self, value: str) -> str:
        ptn: str = ''
        errmes: str = ''
        s: str = ''
        i: int = 0
        templist: list = []
        py3later: int = 0
        splitted: list = []
        py3minor_s: int = 0
        py3minor_e: int = 0
        re_spanstring = Standalone.re_spanstring
        if value.startswith('latest'):
            templist = ['3.{0}'.format(i) for i in range(99, -1, -1)]
            return ' '.join(templist)
        if value.endswith('later'):
            ptn = r'3\.[1-9]?[0-9]'
            reobj = re.match(ptn, value)
            py3later = self._normalize_pyminor(re_spanstring(reobj))
            templist = ['3.{0}'.format(i) for i in range(99, py3later-1, -1)]
            return ' '.join(templist)
        if value.endswith('older'):
            ptn = r'3\.[1-9]?[0-9]'
            reobj = re.match(ptn, value)
            py3older = self._normalize_pyminor(re_spanstring(reobj))
            templist = ['3.{0}'.format(i) for i in range(py3older, -1, -1)]
            return ' '.join(templist)
        ptn = r'3\.[1-9]?[0-9][ ]*[-][ ]*3\.[1-9]?[0-9]'
        if re.match(ptn, value) != None:
            splitted = value.split('-', maxsplit=1)
            py3minor_s = self._normalize_pyminor(splitted[0])
            py3minor_e = self._normalize_pyminor(splitted[1])
            if py3minor_s == py3minor_e:
                return '3.{0}'.format(py3minor_s)
            if py3minor_s > py3minor_e:
                i = py3minor_s
                py3minor_s = py3minor_e
                py3minor_e = i
            templist = ['3.{0}'.format(i) for i in range(
                py3minor_e, py3minor_s - 1, -1)]
            return ' '.join(templist)
        ptn = r'3\.[1-9]?[0-9]'
        splitted: list = []
        templist = []
        if re.match(ptn, value) != None:
            splitted = value.split(' ')
            for s in splitted:
                if re.match(ptn, s) == None:
                    errmes = 'Error: Invalid PY3VERSION strings. [{0}]'.format(
                        value)
                    print_err(errmes)
                    exit(1)
            return value
        errmes = 'Error: Invalid PY3VERSION strings. [{0}]'.format(value)
        print_err(errmes)
        exit(1)

    def normalize(self):
        errmes: str = ''
        ptn: str = ''
        dfdict: dict = self.dfdict.copy()
        srcdict: dict = self.srcdict.copy()
        dstbasedir: str = dfdict['DSTBASEDIR']
        if self._pass_analyze != True:
            errmes = 'Error: The analyze method has not passed yet.'
            print_err(errmes)
            exit(1)
        if self._pass_check != True:
            errmes = 'Error: The check method has not passed yet.'
            print_err(errmes)
            exit(1)
        for varname in ['TARGETPY3', 'TARGETCMD']:
            var = dfdict.get(varname, '')
            if var != '':
                dfdict[varname] = os.path.normpath(var)
        varname = 'PY3VERSION'
        var = dfdict.get(varname, '')
        var = self._normalize_PY3VERSION(var)
        dfdict[varname] = var
        srcdict_new: dict = dict()
        vdict_new: dict = dict()
        for srcfpath, vdict in srcdict.items():
            vdict_new = dict()
            varname = 'DSTDIR'
            value = vdict.get(varname, '')
            if os.path.isabs(os.path.expanduser(value)) == True:
                vdict_new[varname] = os.path.isabs(os.path.expanduser(value))
            else:
                if os.path.isabs(value) == True:
                    errmes = 'Error: DSTDIR is Not Absolute path. [{0}]'.format(
                        value)
                    print_err(errmes)
                    exit(1)
                valueabs = os.path.abspath(dstbasedir + '/' + value) + '/'
                if valueabs.find(dstbasedir) != 0:
                    errmes = 'Error: DSTDIR is Not based DSTBASEDIR. [{0}]'.format(
                        valueabs)
                    print_err(errmes)
                    exit(1)
                else:
                    vdict_new[varname] = valueabs
            varname = 'FMODE'
            value = vdict.get(varname, '')
            if value != '':
                ptn = r'[0-7][0-7][0-7]'
                if re.match(ptn, value) == None:
                    errmes = 'Error: FMODE pattern(e.g. 644, 755) is mismatched. [{0}]'.format(
                        value)
                    print_err(errmes)
                    exit(1)
                vdict_new[varname] = value
            else:
                vdict_new[varname] = '644'
            srcdict_new[srcfpath] = vdict_new.copy()
            del vdict_new
        self.dfdict = dfdict
        self.srcdict = srcdict_new
        self._pass_normalize = True
        return


class Main_snakeland():
    version = '0.0.2'
    date = '26 Nov 2024'

    @staticmethod
    def show_version():
        mes = 'snakeland {0}'.format(Main_snakeland.version)
        print_mes(mes)
        return

    @staticmethod
    def show_help():
        mes: str
        scr_version: str = Main_snakeland.version
        scr_date:  str = Main_snakeland.date
        scr_fname: str = 'snakeland'
        meses = ['{0} created by MikeTurkey'.format(scr_fname),
                 'Version {0}, {1}'.format(scr_version, scr_date),
                 '2023-2024, COPYRIGHT MikeTurkey, All Right Reserved.',
                 'ABSOLUTELY NO WARRANTY. The License is based on GPLv3 Licence',
                 'URL: https://miketurkey.com',
                 '',
                 'Summary',
                 '  Instant Python3 script installer.',
                 'Synopsis',
                 '  snakeland --version --help --license',
                 '  snakeland install [CONFIG]',
                 '  snakeland findpy3 [--later 3.xx] | [--older 3.xx] | --latest',
                 '                    | [--range 3.xx-3.yy] | [--order 3.x,..,3.yy]',
                 'Sub command',
                 '  install: install python script.',
                 '  findpy3: find python3 command path.',
                 'Description',
                 '  --latest: Find latest python3.xx. ',
                 '  --later 3.xx: Find python3.xx later.  e.g. --later 3.7',
                 '  --older 3.xx: Find python3.xx older.  e.g. --older 3.7',
                 '  --range 3.xx-3.yy: Find python3.xx - python3.yy. e.g. --range 3.5-3.10',
                 '  --order 3.x,..3.yy: Find python3.xx .. 3.yy.',
                 '          e.g. --order 3.5,3.6,3.7,3.8,3.9,3,10',
                 '',
                 'e.g.',
                 '  {0} --version'.format(scr_fname),
                 '  {0} install snakeland-CMDNAME.conf'.format(scr_fname),
                 '  {0} findpy3 --later 3.6'.format(scr_fname),
                 '  {0} findpy3 --older 3.10'.format(scr_fname),
                 '  {0} findpy3 --range 3.5-3.10'.format(scr_fname),
                 '  {0} findpy3 --order 3.8,3.9,3.10'.format(scr_fname),
                 '']
        if scr_fname == '':
            raise RuntimeError()
        for mes in meses:
            mes = unicodedata.normalize('NFD', mes)
            print(mes)
        return

    @staticmethod
    def show_license():
        meses = ['SNAKELAND, Instant python script installer.',
                 'Copyright (C) 2023 Takaaki Watanabe as Mike Turkey',
                 'contact: voice[ATmark]miketurkey.com',
                 '',
                 'This program is free software: you can redistribute it and/or modify',
                 'it under the terms of the GNU General Public License as published by',
                 'the Free Software Foundation, either version 3 of the License, or',
                 '(at your option) any later version.',
                 '',
                 'This program is distributed in the hope that it will be useful,',
                 'but WITHOUT ANY WARRANTY; without even the implied warranty of',
                 'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the',
                 'GNU General Public License for more details.',
                 '',
                 'You should have received a copy of the GNU General Public License',
                 'along with this program.  If not, see <https://www.gnu.org/licenses/>.',
                 '',
                 'ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE',
                 '',
                 'In addition to the rights granted under the applicable license(GPL-3),',
                 'you are expressly prohibited from using any form of machine learning,',
                 'artificial intelligence, or similar technologies to analyze, process,',
                 'or extract information from this software, or to create derivative',
                 'works based on this software.',
                 '',
                 'This prohibition includes, but is not limited to, training machine',
                 'learning models, neural networks, or any other automated systems using',
                 'the code or output of this software.',
                 '',
                 'The purpose of this prohibition is to protect the integrity and',
                 'intended use of this software. If you wish to use this software for',
                 'machine learning or similar purposes, you must seek explicit written',
                 'permission from the copyright holder.',
                 '',
                 'see also ',
                 '  GPL-3 Licence, https://www.gnu.org/licenses/gpl-3.0.html.en',
                 '  Mike Turkey.com, https://miketurkey.com']
        for mes in meses:
            mes = unicodedata.normalize('NFD', mes)
            print(mes)
        return

    @staticmethod
    def oscheck(conf_oscheck: list):
        osname: str = ''
        errmes: str = ''
        for osname in conf_oscheck:
            if osname == 'Darwin' and sys.platform.startswith('darwin') == True:
                return
            if osname == 'FreeBSD' and sys.platform.startswith('freebsd') == True:
                return
            if osname == 'Linux' and sys.platform.startswith('linux') == True:
                return
        errmes = 'Error: The software do not run under the OS. [{0}]'.format(
            sys.platform)
        print_err(errmes)
        exit(1)

    @staticmethod
    def check_adminuser():
        errmes: str = ''
        if getpass.getuser() != 'root':
            errmes = 'Error: Current user is NOT root user. [{0}]'.format(
                getpass.getuser())
            print_err(errmes)
            exit(1)
        return

    @staticmethod
    def py3xhunt(py3xstr: str) -> str:
        def iter_py3xcmds_on_pathdir():
            osenv_path: list = os.environ['PATH'].split(':')
            fpath: str = ''
            ptn1 = r'python3$'
            ptn2 = r'python3\.[0-9]$'
            ptn3 = r'python3\.[0-9][0-9]$'
            recompiled_list = [re.compile(
                ptn1), re.compile(ptn2), re.compile(ptn3)]
            for d in osenv_path:
                if os.path.isdir(d) != True:
                    continue
                for fpath in glob.glob(os.path.normpath(d + '/python3*')):
                    if os.path.isfile(fpath) != True:
                        continue
                    if fpath.endswith('-config'):
                        continue  # e.g. python3.10-config

                    def f(x): return True if x != None else False
                    searchlist = [f(recompiled.search(fpath))
                                  for recompiled in recompiled_list]
                    if any(searchlist) == True:
                        yield fpath

        def int_pythonversion(py3ver: str) -> int:
            splitted: list = py3ver.split('.', maxsplit=2)
            r: int = 0
            r = int(splitted[0]) * 1000000
            r = r + int(splitted[1]) * 1000
            r = r + int(splitted[2])
            return r
        splitted: list = list()
        py3cmdlist = [fpath for fpath in iter_py3xcmds_on_pathdir()]
        cmd: str = ''
        tmpstr: str = ''
        tmptpl: tuple = tuple()
        py3xcmddict: dict = dict()
        cmdlist: list = list()
        for cmd in py3cmdlist:
            if sys.version_info.minor >= 5:
                retproc = subprocess.run(
                    [cmd, '--version'], capture_output=True)
                if retproc.returncode == 0:
                    splitted = retproc.stdout.split(maxsplit=1)
                    tmpstr = splitted[1].decode()
                    tmpstr = tmpstr.rstrip('\n')
                    tmptpl = (tmpstr, cmd)
                    cmdlist.append(tmptpl)
                    continue
            else:
                try:
                    tmpstr = subprocess.check_output(
                        [cmd, '--version'], encoding='utf-8')
                except:
                    continue
                splitted = tmpstr.split(maxsplit=1)
                tmpstr = splitted[1]
                tmpstr = tmpstr.rstrip('\n')
                tmptpl = (tmpstr, cmd)
                cmdlist.append(tmptpl)
                continue
        cmdlist.sort(key=lambda x: int_pythonversion(x[0]), reverse=True)
        for py3ver, cmd in cmdlist:
            splitted = py3ver.split('.', maxsplit=2)
            py3ver_short = splitted[0] + '.' + splitted[1]
            if py3xcmddict.get(py3ver_short, '') == '':
                py3xcmddict[py3ver_short] = cmd
                continue
        # e.g. '3.9 3.10 3.11' -> ['3.9', '3.10', '3.11']
        splitted = py3xstr.split()
        for s in splitted:
            cmd = py3xcmddict.get(s, '')
            if cmd != '':
                return cmd
        return ''

    @staticmethod
    def findpy3opt2str(args) -> str:
        n: int = 0
        ptn: str = ''
        errmes: str = ''
        tmplist: list = list()
        splitted: list = []
        if args.latest:
            tmplist = ['3.{0}'.format(i) for i in range(99, -1, -1)]
            return ' '.join(tmplist)
        if args.later != '':
            splitted = args.later.split('.', maxsplit=1)
            n = int(splitted[1])
            tmplist = ['3.{0}'.format(i) for i in range(99, n-1, -1)]
            return ' '.join(tmplist)
        if args.older != '':
            splitted = args.older.split('.', maxsplit=1)
            n = int(splitted[1])
            tmplist = ['3.{0}'.format(i) for i in range(n, -1, -1)]
            return ' '.join(tmplist)
        py3x1: str = ''
        py3_minor1: str = ''
        py3x2: str = ''
        py3_minor2: str = ''
        if args.range != '':
            splitted = args.range.split('-', maxsplit=1)
            py3x1 = splitted[0]
            py3x2 = splitted[1]
            splitted = py3x1.split('.')
            py3_minor1 = int(splitted[1])
            splitted = py3x2.split('.')
            py3_minor2 = int(splitted[1])
            if py3_minor1 == py3_minor2:
                return [py3x1]
            if py3_minor1 >= py3_minor2:
                n = py3_minor1
                py3_minor1 = py3_minor2
                py3_minor1 = n
            tmplist = ['3.{0}'.format(i)
                       for i in range(py3_minor2, py3_minor1-1, -1)]
            return ' '.join(tmplist)
        if args.order != '':
            splitted = args.order.split(',')
            ptn = r'3\.[1-9]?[0-9]$'
            for s in splitted:
                if re.match(ptn, s) == None:
                    errmes = 'Invalid --order option.  e.g. --order 3.5,3.6,3.7 [{0}]'.format(
                        s)
                    print_err(errmes)
                    exit(1)
            return ' '.join(splitted)
        return ''

    @staticmethod
    def copy(srcdict: dict, dstbasedir: str, config: str, dryrun: bool = False) -> list:
        errmes: str = ''
        f: str = ''
        fmode: int = 0
        srcfpath: str = ''
        dstfpath: str = ''
        configdir: str = os.path.dirname(config)
        receipt: list = list()
        if dryrun:
            print('Dryrun: make directory.')
        else:
            if os.path.isdir(dstbasedir) != True:
                try:
                    os.makedirs(dstbasedir)
                except:
                    errmes = 'Error: Can not make the directory. [{0}]'.format(
                        dstbasedir)
                    print_err(errmes)
                    exit(1)
        receipt.append(dstbasedir)
        for f, vdict in srcdict.items():
            srcfpath = os.path.abspath(configdir + '/' + f)
            fmode = int(vdict['FMODE'], base=8)
            if dryrun:
                print('Dryrun: copy, {0} to {1}'.format(
                    srcfpath, vdict['DSTDIR']))
            else:
                if os.path.isfile(srcfpath) != True:
                    errmes = 'Error: Not found the file. [{0}]'.format(
                        srcfpath)
                    print_err(errmes)
                    exit(1)
                try:
                    shutil.copy(srcfpath, vdict['DSTDIR'])
                except:
                    errmes = 'Error: Not copy the file. [{0}]'.format(srcfpath)
                    print_err(errmes)
                    exit(1)
            dstfpath = os.path.abspath(
                vdict['DSTDIR'] + '/' + os.path.basename(srcfpath))
            receipt.append(dstfpath)
            if dryrun:
                print('Dryrun: chmod, {0:o}, {1}'.format(fmode, dstfpath))
            else:
                try:
                    os.chmod(dstfpath, fmode)
                except:
                    errmes = 'Error: Not change fmode. [{0}, {1}]'.format(
                        fmode, dstfpath)
                    print_err(errmes)
                    exit(1)
        return receipt

    @staticmethod
    def _install_confpy(confpy3: str) -> str:
        py3cmdopt: str = ''
        ptn: str = ''
        errmes: str = ''
        tmplist: list = []
        if confpy3.startswith('latest'):
            py3cmdopt = '--latest'
            return py3cmdopt
        ptn = r'3\.[1-9]?[0-9][ ]*later$'
        reobj = re.match(ptn, confpy3)
        if reobj != None:
            ptn = r'3\.[1-9]?[0-9]'
            tmplist = re.findall(ptn, confpy3)
            if len(tmplist) != 1:
                errmes = 'Error: Invalid PY3VERSION later format. [{0}]'.format(
                    confpy3)
                print_err(errmes)
                exit(1)
            py3cmdopt = '--later {0}'.format(tmplist[0])
            return py3cmdopt
        ptn = r'3\.[1-9]?[0-9][ ]*older$'
        reobj = re.match(ptn, confpy3)
        if reobj != None:
            ptn = r'3\.[1-9]?[0-9]'
            tmplist = re.findall(ptn, confpy3)
            if len(tmplist) != 1:
                errmes = 'Error: Invalid PY3VERSION older format. [{0}]'.format(
                    confpy3)
                print_err(errmes)
                exit(1)
            py3cmdopt = '--older {0}'.format(tmplist[0])
            return py3cmdopt
        ptn = r'3\.[1-9]?[0-9][ ]*\-'
        rangemode = True if re.match(ptn, confpy3) != None else False
        ptn = r'3\.[1-9]?[0-9]'
        tmplist = re.findall(ptn, confpy3)
        if rangemode == True and len(tmplist) == 2:
            py3cmdopt = '--range {0}-{1}'.format(tmplist[0], tmplist[1])
            return py3cmdopt
        if len(tmplist) >= 1:
            py3cmdopt = '--order {0}'.format(','.join(tmplist))
            return py3cmdopt
        errmes: str = 'Error: Invalid PY3VERSION format.'
        print_err(errmes)
        exit(1)

    @staticmethod
    def make_pkgreceipt(pkgdir: str, dfdict: dict, dryrun: bool = False):
        appdir: str = ''
        mes: str = ''
        pkgdir_fmode: int = 0o644
        appdir_fmode: int = 0o644
        if os.path.isdir(pkgdir) != True:
            if dryrun:
                mes = 'Dryrun: Make directory. [{0}]'.format(pkgdir)
                print_mes(mes)
            else:
                try:
                    os.makedirs(pkgdir)
                    os.chmod(pkgdir, pkgdir_fmode)
                except:
                    errmes = 'Error: Can not make the directory. [{0}]'.format(
                        pkgdir)
                    print_err(errmes)
                    exit(1)
        appdir = os.path.abspath(pkgdir + '/' + dfdict['CMDNAME'])
        if os.path.isdir(appdir) != True:
            if dryrun:
                mes = 'Dryrun: Make directory. [{0}]'.format(appdir)
                print_mes(mes)
            else:
                try:
                    os.makedirs(appdir)
                    os.chmod(appdir, appdir_fmode)
                except:
                    errmes = 'Error: Can not make the directory. [{0}]'.format(
                        appdir)
                    print_err(errmes)
                    exit(1)
        return

    @staticmethod
    def install(dfdict: dict, py3ver: str, dryrun: bool = False) -> list:
        py3mode: bool = False
        cmdmode: bool = False
        meses: list = list()
        errmes: str = ''
        receipt: list = []
        py3mode = True if dfdict.get('TARGETPY3', '') != '' else False
        cmdmode = True if dfdict.get('TARGETCMD', '') != '' else False
        if [py3mode, cmdmode].count(True) >= 2:
            errmes = 'Error: Too many mode on install method.'
            print_err(errmes)
            exit(1)
        if [py3mode, cmdmode].count(True) == 0:
            errmes = 'Error: Empty mode on install method.'
            print_err(errmes)
            exit(1)
        if cmdmode:
            meses = ['#!/bin/sh',
                     'exec {0} "$@"'.format(dfdict['TARGETCMD'])]
            installcmd_dir = dfdict['INSTALLCMD']
            installcmd = os.path.abspath(
                installcmd_dir + '/' + dfdict['CMDNAME'])
            if dryrun:
                [print(s) for s in meses]
                print('cmd: ', installcmd)
            else:
                try:
                    with open(installcmd, 'wt', encoding='utf-8') as fp:
                        for s in meses:
                            print(s, file=fp)
                    os.chmod(installcmd, 0o775)
                except:
                    errmes = 'Error: Failure to create the command. [{0}]'.format(
                        installcmd)
                    print_err(errmes)
                    exit(1)
            receipt = [installcmd]
            return receipt
        if py3mode:
            py3cmdopt = Main_snakeland._install_confpy(py3ver)
            meses = ['#!/bin/sh',
                     'PYTHON=$(snakeland findpy3 {0})'.format(py3cmdopt),
                     'if ! test -x "$PYTHON"; then',
                     '    echo "$PYTHON"; exit 1; fi',
                     'exec "$PYTHON" {0} "$@"'.format(dfdict['TARGETPY3'])]
            installcmd_dir = dfdict['INSTALLCMD']
            installcmd = os.path.abspath(
                installcmd_dir + '/' + dfdict['CMDNAME'])
            if dryrun:
                [print(s) for s in meses]
                print('cmd: ', installcmd)
            else:
                try:
                    with open(installcmd, 'wt', encoding='utf-8') as fp:
                        for s in meses:
                            print(s, file=fp)
                    os.chmod(installcmd, 0o775)
                except:
                    errmes = 'Error: Failure to create the command. [{0}]'.format(
                        installcmd)
                    print_err(errmes)
                    exit(1)
            receipt = [installcmd]
            return receipt
        errmes = 'The script is attempting to execute a prohibited row.'
        raise RuntimeError(errmes)


def main_snakeland():
    pkgdir: str = '/usr/local/libexec/snakeland/pkg/'
    devmode = False
    if sys.version_info.major == 3 and sys.version_info.minor < 4:
        errmes = 'Error: Need python 3.6 later. [python: {0}]'.format(
            sys.version.split(' ')[0])
        print(errmes, file=sys.stderr)
        exit(1)
    if devmode:
        print('Develop mode: True')
    args: Args_snakelands = Args_snakelands()
    args.analyze()
    args.check()
    args.normalize()
    if args.subcmd == 'findpy3':
        py3xstr = Main_snakeland.findpy3opt2str(args)
        python3xpath = Main_snakeland.py3xhunt(py3xstr)
        if python3xpath == '':
            errmes = 'Error: Not found python3 command.'
            print_err(errmes)
            exit(1)
        print(python3xpath)
        exit(0)
    if args.subcmd == 'install':
        conf: ConfParser_snakeland = ConfParser_snakeland()
        conf.load(args.config)
        conf.analyze()
        rawconf = copy.copy(conf)
        conf.check()
        conf.normalize()
        Main_snakeland.oscheck(conf.dfdict['OSCHECK'])
        if devmode != True:
            Main_snakeland.check_adminuser()
        python3xpath = Main_snakeland.py3xhunt(conf.dfdict['PY3VERSION'])
        if python3xpath == '':
            errmes = 'Error: Not found python3 command to run the script.  [{0}]'
            errmes = errmes.format(rawconf.dfdict['PY3VERSION'])
            print_err(errmes)
            exit(1)
        dstbasedir: str = conf.dfdict['DSTBASEDIR']
        receipt: list = list()
        receipt = Main_snakeland.copy(
            conf.srcdict, dstbasedir, args.config, dryrun=False)
        templist = Main_snakeland.install(
            conf.dfdict, rawconf.dfdict['PY3VERSION'], dryrun=False)
        receipt += templist
        Main_snakeland.make_pkgreceipt(pkgdir, conf.dfdict, dryrun=False)
        s = 'Success: {0} has been installed.'.format(conf.dfdict['CMDNAME'])
        print(s, file=sys.stdout)
        exit(0)
    return


if __name__ == '__main__':
    main_snakeland()
    exit(0)
