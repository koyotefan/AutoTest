# encoding=utf-8

import os
import sys
import time
import random
import traceback
import json
from collections import OrderedDict

def read_json_file(_dir, _filename):
    txt = ''

    with open(os.path.join(_dir, _filename), 'r') as f:
        line = ''
        while True:
            line = f.readline()

            if not line:
                break

            if len(line.strip()) > 0 and line[0] == '#':
                continue

            txt += line

    return json.loads(txt, object_pairs_hook=OrderedDict)


def get_group_name_list():
    '''
    Group Dir 에서 grp 파일들만 찾습니다.
    '''
    group_dir = get_snr_group_dir()
    ret_list = []

    for _, _, files in os.walk(group_dir):
        for name in files:
            if name.endswith(('.grp')):
                ret_list.append(name)

    return ret_list


def get_executor_dir():
    return os.path.join(os.environ['AUTOV_BASE_DIR'], 'SnrExecutor')


def get_primitive_dir():
    return os.path.join(os.environ['AUTOV_BASE_DIR'], 'SnrExecutor', 'Primitive')


def get_snr_dir():
    return os.path.join(os.environ['AUTOV_BASE_DIR'], 'SnrExecutor', 'SnrList')


def get_snr_group_dir():
    return os.path.join(os.environ['AUTOV_BASE_DIR'], 'SnrExecutor', 'SnrGroup')


def get_snr_name_list(_group_file_name):
    json_data = read_json_file(get_snr_group_dir(), _group_file_name)
    return json_data['snrs']


def get_agent_dir():
    return os.path.join(os.environ['AUTOV_BASE_DIR'], 'SnrAgent')

def get_sim_info(_sim_name):
    json_data = read_json_file(get_agent_dir(), 'Simulator.conf')

    if _sim_name not in json_data.keys():
        return None
    return json_data[_sim_name]


def get_agent_log_dir():
    return os.path.join(get_agent_dir(), 'log')


def get_executor_log_dir():
    return os.path.join(get_executor_dir(), 'log')

def get_history_dir():
    return os.path.join(get_executor_dir(), 'history')

def conv_mdn_to_min(_mdn):
    # 그냥 대충 했어요...
    if len(_mdn) == 10:
        return _mdn
    else:
        return _mdn[1:]


def conv_mdn_to_msisdn(_mdn):
    # 대충 했어요.
    return '82' + _mdn[1:]


def conv_mdn_to_imsi(_mdn):
    # 대충 했다구요.
    return '45005' + _mdn[1:]


def gen_seq():
    return time.strftime("%Y%m%d_%H%M%S_") + str(random.randrange(1, 1000))


def get_date():
    return time.strftime("%Y%m%d")


def get_time():
    return time.strftime("%H%M%S")


def get_logset_file_name():
    '''
    Agent 측에서 불리 웁니다.
    '''
    return os.path.join(os.environ['AUTOV_BASE_DIR'], 'SnrAgent', 'work', 'log.set')

def pretty_json(_dict):
    if isinstance(_dict, str) or isinstance(_dict, unicode):
        _dict = json.loads(_dict, object_pairs_hook=OrderedDict)

    return json.dumps(_dict, sort_keys=False, indent=4, separators=(',', ': '))

def print_add_result(_src, _add_word, length=80):
    return "{}{:.>{prec}}".format(_src, _add_word, prec=length-len(_src))