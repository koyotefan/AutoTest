# encoding=utf-8

import sys
import traceback
import json
from src.common.TargetAgent import TargetAgent

'''
{
    "TARGET_DB": {
        #"HOST": ["192.168.10.45", "20303"],
        #"DATABASE": "pcrf",
        #"DRIVER": "/altibase/altibase_home/lib/libaltibase_odbc-64bit-ul32.so",
        #"ID": "pcrf",
        #"PW": "pcrf1234"
        "DSN_NAME" : "PDB_SUBS_P"
    },
    "PARAMETER": {
        "MDN": "01028071121"
    },
    "EXPECT": {
        "r$RESULT": "OK"
    }
}
'''

class  DBSubsDelete(TargetAgent):
    '''
    DB-가입자-삭제 primitive 에 대한 구현체 입니다.
    가입자 테이블이 변경되면, DB_가입자_테이블.conf 변경이 필요 합니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.db_dict = None
        self.param_dict = None
        self.exp_dict = {}

    def __str__(self):
        return 'DBSubsDelete'

    def make_request_data(self, _constant):
        # conf 에서 T_SUBSCRIBER_INFO 의 Column 및 default 값을 config 에서 읽어 옵니다.
        # 읽은 값에 대고, _constant 가 그동안 축적한 값을 반영시킵니다.
        #self.param_dict = _constant.get_template("DB_가입자_테이블.conf")
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        self.param_dict = {"MDN" : l_dict["MDN"]}

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            #elif key == "TARGET_AGENT":
            #    TargetAgent.set(self, l_dict[key])
            elif key == 'TARGET_DB':
                self.db_dict = _constant.get_targetdb(l_dict[key])
            else:
                _constant.reflect_to_dict(self.param_dict, l_dict)

        return self._verify(_constant)

    def _verify(self, _constant):

        if self.db_dict == None:
            self.db_dict = _constant.get_targetdb("$PDB_SUBS_P")

        for val in self.db_dict.values():
            if isinstance(val, str) and val.startswith('$'):
                return False

        if not self.param_dict:
            return False

        for val in self.param_dict.values():
            if val.startswith('$'):
                return False

        for val in self.exp_dict.values():
            if val.startswith('$'):
                return False

        return True

    def request(self):
        ret_dict = {}

        ret_dict["TARGET_DB"] = self.db_dict
        ret_dict["PARAMETER"] = self.param_dict
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

        # DB 삭제
        sql = self._delete_sql(_req_dict["PARAMETER"])
        try:
            db.execute(sql)
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            db.close()
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Delete Fail"

            return res_dict

        db.close()
        return res_dict

    def _delete_sql(self, _dict):
        return "DELETE FROM T_SUBSCRIBER_INFO WHERE MDN='{}'".format(_dict["MDN"])