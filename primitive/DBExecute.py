# encoding=utf-8

import sys
import traceback
import json
from src.common.TargetAgent import TargetAgent

'''
{
    "TARGET_DB": {
        "HOST": ["192.168.10.45", "20304"],
        "DATABASE": "pg",
        "DRIVER": "/altibase/altibase_home/lib/libaltibase_odbc-64bit-ul32.so",
        "ID": "pg",
        "PW": "pg1234"
    },
    "EXPECT": {
        "r$RESULT": "OK"
    },
    "SQL": ["delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = 192.0.0.1",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = 192.0.0.2",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = 192.0.0.3",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = 192.0.1.1",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = 192.0.1.2",
            "delete from T_PGW_GROUP_INFO WHERE CLIENT_IP = 192.0.1.3"]
}
'''

class DBExecute(TargetAgent):
    '''
    MMSC-SIM-START primitive 에 대한 구현체 입니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.db_dict = None
        self.sql_list = []
        self.exp_dict = {}


    def __str__(self):
        return 'DBExecute'


    def make_request_data(self, _constant):
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            elif key == 'TARGET_DB':
                self.db_dict = _constant.get_targetdb(l_dict[key])
            elif key == 'SQL':
                if not isinstance(l_dict[key], list):
                    self.sql_list = []
                    continue

                for stmt in l_dict[key]:
                    stmt = _constant.reflect_to_str(stmt, l_dict)
                    self.sql_list.append(stmt)
            else:
                pass

        return self._verify(_constant)

    def _verify(self, _constant):
        if self.db_dict == None:
            self.db_dict = _constant.get_targetdb("$PDB_PG_P")

        if not self.sql_list:
            return False

        for stmt in self.sql_list:
            if "$" in stmt:
                return False

        return True


    def request(self):
        ret_dict = {}

        ret_dict["TARGET_DB"] = self.db_dict
        ret_dict["SQL"] = self.sql_list
        ret_dict["EXPECT"] = self.exp_dict

        return json.dumps(ret_dict, sort_keys=False)


    def uri(self):
        return TargetAgent.uri(self, self.__class__.__name__)


    def do(self, _req_dict):
        res_dict = {}
        res_dict["RESULT"] = "OK"

        # 파라메터와 TARGET_DB 를 찾아야 합니다.
        if ("TARGET_DB" or "PARAMETER") not in _req_dict.keys():
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "Missing TARGET_DB or PARAMETER tag"
            return res_dict

        from src.common.DB import PDB
        db = PDB()

        try:
            db.init(_req_dict["TARGET_DB"]["DSN_NAME"])
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Connection Error"
            return res_dict

        # DB 실행
        sql_list = _req_dict["SQL"]

        try:
            for stmt in sql_list:
                db.execute(stmt)
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            db.close()
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Execute Fail"

            return res_dict

        db.close()
        return res_dict
