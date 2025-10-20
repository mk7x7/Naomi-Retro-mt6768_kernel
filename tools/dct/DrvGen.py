#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2016 MediaTek Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See http://www.gnu.org/licenses/gpl-2.0.html for more details.

import os
import sys
import getopt
import traceback
import subprocess
import xml.dom.minidom

sys.dont_write_bytecode = True

sys.path.append('.')
sys.path.append('..')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tools/dct/obj')))

from obj.ChipObj import ChipObj
from obj.ChipObj import MT6797
from obj.ChipObj import MT6757
from obj.ChipObj import MT6757_P25
from obj.ChipObj import MT6570
from obj.ChipObj import MT6799
from obj.ChipObj import MT6759
from obj.ChipObj import MT6763
from obj.ChipObj import MT6750S
from obj.ChipObj import MT6758
from obj.ChipObj import MT6739
from obj.ChipObj import MT8695
from obj.ChipObj import MT6771
from obj.ChipObj import MT6775
from obj.ChipObj import MT6779
from obj.ChipObj import MT6768
from obj.ChipObj import MT6785

from utility.util import LogLevel
from utility.util import log


def usage():
    print('''
usage: DrvGen [dws_path] [file_path] [log_path] [paras]...

options and arguments:

dws_path    :    dws file path
file_path   :    where you want to put generated files
log_path    :    where to store the log files
paras       :    parameter for generate wanted file
''')


def is_oldDws(dws_path, gen_spec, gen_path, log_path):
    if not os.path.exists(dws_path):
        log(LogLevel.error, f'Can not find {dws_path}')
        sys.exit(-1)

    try:
        root = xml.dom.minidom.parse(dws_path)
    except Exception as e:
        log(LogLevel.warn, f'{dws_path} is not xml format, try to use old DCT!')
        if len(gen_spec) == 0:
            log(LogLevel.warn, 'Please use old DCT UI to gen all files!')
            return True
        old_dct = os.path.join(sys.path[0], 'old_dct', 'DrvGen')
        cmd = f'{old_dct} {dws_path} {gen_path} {log_path} {gen_spec[0]}'
        if subprocess.call(cmd, shell=True) == 0:
            return True
        else:
            log(LogLevel.error, f'{dws_path} format error!')
            sys.exit(-1)

    return False


def cmp_py3(a, b):
    """Simula cmp do Python 2 em Python 3"""
    return (a > b) - (a < b)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], '')
    except getopt.GetoptError as e:
        usage()
        log(LogLevel.error, f'Getopt error: {e}')
        sys.exit(-1)

    if len(args) == 0:
        msg = 'Too few arguments!'
        usage()
        log(LogLevel.error, msg)
        sys.exit(-1)

    dws_path = ''
    gen_path = ''
    log_path = ''
    gen_spec = []

    # get DWS file path from parameters
    dws_path = os.path.abspath(args[0])

    # get parameters from input
    if len(args) == 1:
        gen_path = os.path.dirname(dws_path)
        log_path = os.path.dirname(dws_path)

    elif len(args) == 2:
        gen_path = os.path.abspath(args[1])
        log_path = os.path.dirname(dws_path)

    elif len(args) == 3:
        gen_path = os.path.abspath(args[1])
        log_path = os.path.abspath(args[2])

    elif len(args) >= 4:
        gen_path = os.path.abspath(args[1])
        log_path = os.path.abspath(args[2])
        for i in range(3, len(args)):
            gen_spec.append(args[i])

    log(LogLevel.info, f'DWS file path is {dws_path}')
    log(LogLevel.info, f'Gen files path is {gen_path}')
    log(LogLevel.info, f'Log files path is {log_path}')

    for item in gen_spec:
        log(LogLevel.info, f'Parameter is {item}')

    # check existence of paths
    if not os.path.exists(dws_path):
        log(LogLevel.error, f'Can not find "{dws_path}", file not exist!')
        sys.exit(-1)

    if not os.path.exists(gen_path):
        log(LogLevel.error, f'Can not find "{gen_path}", gen path not exist!')
        sys.exit(-1)

    if not os.path.exists(log_path):
        log(LogLevel.error, f'Can not find "{log_path}", log path not exist!')
        sys.exit(-1)

    if is_oldDws(dws_path, gen_spec, gen_path, log_path):
        sys.exit(0)

    chipId = ChipObj.get_chipId(dws_path)
    log(LogLevel.info, f'chip id: {chipId}')
    chipObj = None

    # Usando cmp_py3 para substituir cmp do Python2
    if cmp_py3(chipId, 'MT6797') == 0:
        chipObj = MT6797(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6757') == 0:
        chipObj = MT6757(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6757-P25') == 0:
        chipObj = MT6757_P25(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6570') == 0:
        chipObj = MT6570(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6799') == 0:
        chipObj = MT6799(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6763') == 0:
        chipObj = MT6763(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6759') == 0:
        chipObj = MT6759(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6750S') == 0:
        chipObj = MT6750S(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6758') == 0:
        chipObj = MT6758(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6739') == 0:
        chipObj = MT6739(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT8695') == 0 or cmp_py3(chipId, 'MT8168') == 0:
        chipObj = MT8695(dws_path, gen_path)
    elif (cmp_py3(chipId, 'MT6771') == 0 or
          cmp_py3(chipId, 'MT6775') == 0 or
          cmp_py3(chipId, 'MT6765') == 0 or
          cmp_py3(chipId, 'MT3967') == 0 or
          cmp_py3(chipId, 'MT6761') == 0):
        chipObj = MT6771(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6779') == 0:
        chipObj = MT6779(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6768') == 0:
        chipObj = MT6768(dws_path, gen_path)
    elif cmp_py3(chipId, 'MT6785') == 0:
        chipObj = MT6785(dws_path, gen_path)
    else:
        chipObj = ChipObj(dws_path, gen_path)

    if not chipObj.parse():
        log(LogLevel.error, f'Parse {dws_path} fail!')
        sys.exit(-1)

    if not chipObj.generate(gen_spec):
        log(LogLevel.error, 'Generate files fail!')
        sys.exit(-1)

    sys.exit(0)
