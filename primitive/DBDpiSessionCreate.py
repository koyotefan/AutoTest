# encoding=utf-8

import sys
import traceback
import json
from src.common.TargetAgent import TargetAgent

'''
"TARGET_DB": {
        #"HOST": ["192.168.10.106", "20305"],
        #"DATABASE": "pcrf",
        #"DRIVER": "/altibase/altibase_home/lib/libaltibase_odbc-64bit-ul32.so",
        #"ID": "pcrf",
        #"PW": "pcrf1234"
        "DSN_NAME" : "PDB_SESSION_P_45",
        "TABLE_INDEX" : "04"
    },
    "PARAMETER": {
        "SESSION_ID": "20161121_100506_70",
        "MIN": "1099998888",
        "MSISDN": "821099998888",
        "IMSI": "450051099998888",
        "SESSION_STATUS": "2",
        "CONTROLABLE_USER": "",
        "OPEN_DATE": "20161121",
        "OPEN_TIME": "100506",
        "UPDATE_DATE": "",
        "UPDATE_TIME": "",
        "LOCATION_ID": "12345:3",
        "LOCATION_STATUS": "0",
        "PRODUCT_POLICY": "",
        "DPI_SERVICE_ID": "",
        "RULE_BASE_NAME": "",
        "QCI_LEVEL": "",
        "DATA_USAGE_LEVEL": "0",
        "MVOIP_LIMIT_OVER_FG": "N",
        "CCR_TYPE": "2",
        "CCR_RECORD_NO": "1",
        "IP_ADDR": "0.0.0.0",
        "CLIENT_HOST": "ltepgw01.skt.net",
        "CLIENT_REALM": "skt.net",
        "BEARER_ID": " ",
        "PROC_SYSTEM": "P",
        "FEMTOCELL_CTRL": " ",
        "APN_TYPE": "2",
        "APN": "test1.sktelecom.com",
        "RM_PROCESSING": "N",
        "SERVICE_ID": "000002",
        "DESTINATION_HOST": "ltepcrf01",
        "RAT_TYPE": "L",
        "R4": " ",
        "R3": " ",
        "R2": " ",
        "R1": " ",
        "ADDITIONAL_SERVICE_RULE": "",
        "VOMS_POLICY_ID": "",
        "IP_VERSION": "4",
        "SGSN_MCC_MNC": "45005",
        "DPI_SERVICE_INFO": "",
        "DPI_SERVICE_INFO_STORE": "",
        "BIND": " ",
        "LOOKUP": " "
    },
    "EXPECT": {
        "r$RESULT": "OK"
    }
}

'''

class  DBDpiSessionCreate(TargetAgent):
    '''
    DB-DPI-세션-생성 primitive 에 대한 구현체 입니다.
    세션 테이블이 변경되면, DB_PGW_세션_테이블.conf 변경이 필요 합니다.
    '''
    def __init__(self):
        TargetAgent.__init__(self)

        self.db_dict = None
        self.param_dict = None
        self.exp_dict = {}

    def __str__(self):
        return 'DBDpiSessionCreate'

    def make_request_data(self, _constant):
        # conf 에서 T_SUBSCRIBER_INFO 의 Column 및 default 값을 config 에서 읽어 옵니다.
        # 읽은 값에 대고, _constant 가 그동안 축적한 값을 반영시킵니다.
        self.param_dict = _constant.get_template("DB_DPI_세션_테이블.conf")
        l_dict = _constant.get_var()
        TargetAgent.set(self, l_dict["TARGET_AGENT"])

        for key in l_dict:
            if key.startswith('r$'):
                self.exp_dict[key] = l_dict[key]
            elif key == 'TARGET_DB':
                self.db_dict = _constant.get_targetdb(l_dict[key], l_dict["MIN"])
            else:
                _constant.reflect_to_dict(self.param_dict, l_dict)

        return self._verify(_constant, l_dict["MIN"])

    def _verify(self, _constant, _min):

        if self.db_dict == None:
            self.db_dict = _constant.get_targetdb("$PDB_SESSION_P", _min)

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
        sql = self._delete_sql(_req_dict["PARAMETER"], _req_dict["TARGET_DB"])

        try:
            db.execute(sql)
        except:
            pass

        # DB 생성
        sql = self._insert_sql(_req_dict["PARAMETER"], _req_dict["TARGET_DB"])

        try:
            db.execute(sql)
        except:
            _, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_value,
                                             exc_value,
                                             exc_traceback)

            db.close()
            res_dict["RESULT"] = "NOK"
            res_dict["REASON"] = "DB Insert Fail"

            return res_dict

        db.close()
        return res_dict

        # 수정 해야 ...
    def _insert_sql(self, _param_dict, _db_dict):
        sql_list = []

        sql_list.append("INSERT INTO T_DPI_SESSION_INFO_{} (".format(_db_dict["TABLE_INDEX"]))
        for param in _param_dict.keys():
            sql_list.append(param)
            sql_list.append(",")

        # 마지막 , 를 날리고요.
        sql_list[-1] = ") VALUES ("
        for param in _param_dict.keys():
            sql_list.append("'{}'".format(_param_dict[param]))
            sql_list.append(",")

        # 마지막 , 를 날리고요.
        sql_list[-1] = ")"

        return ''.join(sql_list)

        # 수정해야..
    def _delete_sql(self, _param_dict, _db_dict):
        return "DELETE FROM T_DPI_SESSION_INFO_{} WHERE MIN='{}'".format(_db_dict["TABLE_INDEX"], _param_dict["MIN"])
