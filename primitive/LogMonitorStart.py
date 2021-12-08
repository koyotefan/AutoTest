# encoding=utf-8

import json
from src.common.TargetAgent import TargetAgent

'''
{
    "TASK_ID" : "테스트.snr_20161124_132214_861",
    "FILES": ["/data/PG/LOG/RT/SESSION.CDS*.01.20161118",
              "/data/PG/LOG/RT/SESSION.P_SDM*.01.20161118"],
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class LogMonitorStart(TargetAgent):
    '''
    LOG-MONITOR-START primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.task_id = ''
        self.file_list = []
        self.exp_dict = {}

    def __str__(self):
        return 'LogMonitorStart'


    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])
        self.task_id = l_dict["TASK_ID"]

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            #elif key == "TARGET_AGENT":
            #    TargetAgent.set(self, l_dict[key])
            elif key == 'TARGET':
            #    TargetAgent.set(self, l_dict["TARGET_AGENT"])
                self.file_list = TargetAgent.get_log_file_list(self, l_dict[key])
                self.file_list = self._reflect_to_list(self.file_list, l_dict)
            else:
                pass

        return self._verify(_constant)

    def _reflect_to_list(self, _obj_list, _l_dict):
        return [stmt.replace("$YYYYMMDD", _l_dict["YYYYMMDD"]) for stmt in _obj_list]

    def _verify(self, _constant):
        if not self.file_list:
            return False

        return True


    def request(self):
        ret_dict = {}

        ret_dict["TASK_ID"] = self.task_id
        ret_dict["FILES"] = self.file_list
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)


    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)


    def do(self, _req_dict):
        '''
        파일에다가, 파일의 offset 을 표시해 둡니다.
        '''

        res_dict = {}
        res_dict["RESULT"] = "OK"

        import os
        from src.common.Misc import read_json_file, get_logset_file_name

        fname = get_logset_file_name()

        logset_dict = {}
        try:
            logset_dict = read_json_file(fname[:fname.rfind(os.sep)],
                                         fname[fname.rfind(os.sep)+1:])
        except IOError:
            pass

        # 본인의 Task ID 를 찾습니다.
        task_id = _req_dict["TASK_ID"]
        if task_id not in logset_dict.keys():
            logset_dict[task_id] = {}

        for target in _req_dict["FILES"]:
            try:
                logset_dict[task_id][target] = os.stat(target).st_size
            except OSError:
                logset_dict[task_id][target] = 0L

        logset_dict = self._clear_pg_log(logset_dict)

        try:
            self._write_file(fname,
                             json.dumps(logset_dict,
                                        sort_keys=True,
                                        indent=4,
                                        separators=(',', ': ')))
        except IOError:
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "can't set"

        return res_dict


    def _write_file(self, _fname, _data):
        with open(_fname, 'w') as fd:
            fd.write(_data)

    def _clear_pg_log(self, _logset_dict):
        from datetime import datetime, timedelta
        yesterday = (datetime.now() + timedelta(days=-1)).strftime('%Y%m%d')

        task_id_list = _logset_dict.keys()
        for fname in task_id_list:
            unit_list = fname.split('_')

            if yesterday > unit_list[-3]:
                _logset_dict.pop(fname)

        return _logset_dict
