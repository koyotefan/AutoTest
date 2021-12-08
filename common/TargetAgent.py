# encoding=utf-8

import os
import sys
import json

from src.common.Misc import read_json_file, get_executor_dir

class TargetAgent(object):
    '''
    시나리오의 Primtive 를 어떤 시스템에게 시킬 때, 대상 시스템에 대한 정보를 관리한다.
    '''
    def __init__(self):
        self.name = ''
        self.json_data = None

    def __str__(self):
        return 'TargetAgent - {name}'.format(name=self.name)

    def set(self, _name):
        self.name = _name
        self.json_data = read_json_file(get_executor_dir(), self.name + '.conf')

    def uri(self, _path_name):
        return 'http://{host}:{port}/{path}'.format(host=self.json_data["HOST"]["IP"],
                                                    port=self.json_data["HOST"]["PORT"],
                                                    path=_path_name)

    def get_log_file_list(self, _process_list):

        ret_list = []

        for p_name in _process_list:
            if not self.json_data["PROCESSES"].keys():
                continue

            for name in self.json_data["PROCESSES"][p_name]["NAMES"]:
                fname = self.json_data["PROCESSES"][p_name]["LOG_NAME"].replace("$NAME", name)
                ret_list.append(os.path.join(self.json_data["PROCESSES"][p_name]["LOG_PATH"],
                                             fname))

        return ret_list
