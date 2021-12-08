# encoding=utf-8

from collections import OrderedDict
from src.common.Misc import read_json_file, get_executor_dir, get_primitive_dir
from src.common.Misc import conv_mdn_to_min, conv_mdn_to_imsi, conv_mdn_to_msisdn
from src.common.Misc import gen_seq, get_date, get_time


class SnrConstant(object):
    def __init__(self, _L):
        self.L = _L

        self.gloval_dict = read_json_file(get_executor_dir(), 'global.conf')
        self.local_dict_list = []
        self.primitive_dict = None

    def push_var(self):
        local = OrderedDict()
        self.local_dict_list.append(local)

    def pop_var(self):
        self.local_dict_list.pop(-1)

    def get_var_depth(self):
        return len(self.local_dict_list)

    def set_var(self, _dict):
        local = self.local_dict_list[-1]

        for key in _dict.keys():
            if key == 'PRIMITIVE' or key == 'SCENARIO':
                continue
            local[key] = _dict[key]

    def set_primitive_var(self, _dict):
        self.primitive_dict = {}

        for key in _dict.keys():
            if key == 'PRIMITIVE' or key == 'SCENARIO':
                continue
            self.primitive_dict[key] = _dict[key]

    def get_template(self, _conf_fname):
        return read_json_file(get_primitive_dir(), _conf_fname)


    def get_var(self):
        # 여기서, 각 변수들을 누적시켜서 반환합니다.
        ret_dict = {}

        # 0. 기타 변수를 등록합니다.
        ret_dict["SEQ"] = gen_seq()
        ret_dict["YYYYMMDD"] = get_date()
        ret_dict["hhmmss"] = get_time()
        ret_dict["YYYYMMDDhhmmss"] = get_date() + get_time()

        # 1. Global 변수들을 반영합니다.
        ret_dict["TARGET_AGENT"] = self.gloval_dict["TARGET_AGENT"]
        for key in self.gloval_dict["COMMON"]:
            self._accumulate(ret_dict, key, self.gloval_dict["COMMON"][key])

        # 2. Step Local 변수들을 반영합니다.
        for local_dict in self.local_dict_list:
            for key in local_dict:
                self._accumulate(ret_dict, key, local_dict[key])

        # 3. primitive 변수들을 반영합니다.
        if not self.primitive_dict:
            return ret_dict

        for key in self.primitive_dict:
            self._accumulate(ret_dict, key, self.primitive_dict[key])

        return ret_dict


    def _accumulate(self, _ret_dict, _key, _val):
        if (isinstance(_val, str) or isinstance(_val, unicode)) and _val.startswith('$'):
            if _val[1:] in _ret_dict.keys():
                _ret_dict[_key] = _ret_dict[_val[1:]]
                return

        _ret_dict[_key] = _val

        if _key == 'MDN':
            _ret_dict["MIN"] = conv_mdn_to_min(_val)
            _ret_dict["MSISDN"] = conv_mdn_to_msisdn(_val)
            _ret_dict["IMSI"] = conv_mdn_to_imsi(_val)

        if _key == 'NEW_MDN':
            _ret_dict["NEW_MIN"] = conv_mdn_to_min(_val)

    def get_targetdb(self, _val, _min=''):
        if not _val.startswith('$'):
            return {}

        val = _val[1:]

        if val not in self.gloval_dict["DB"].keys():
            return {}

        ret_dict = {}

        #ret_dict["ID"] = self.gloval_dict["DB"][val]["ID"]
        #ret_dict["PW"] = self.gloval_dict["DB"][val]["PW"]
        #ret_dict["DATABASE"] = self.gloval_dict["DB"][val]["DATABASE"]
        # ret_dict["DRIVER"] = self.gloval_dict["DB"][val]["DRIVER"]
        # ret_dict["DSN_NAME"] = self.gloval_dict["DB"][val]["DSN_NAME"]

        # SESSION DB 를 찾는거죠
        if _min:
            mod_v = len(self.gloval_dict["DB"][val]["HOST"])
            table_index = long(_min) % (mod_v * 2)
            index = table_index / 2
            #ret_dict["HOST"] = self.gloval_dict["DB"][val]["HOST"][index]
            ret_dict["DSN_NAME"] = self.gloval_dict["DB"][val]["DSN_NAME"][index]
            ret_dict["TABLE_INDEX"] = '{:02d}'.format(table_index)
        else:
            #ret_dict["HOST"] = self.gloval_dict["DB"][val]["HOST"]
            ret_dict["DSN_NAME"] = self.gloval_dict["DB"][val]["DSN_NAME"]

        return ret_dict


    def reflect_to_dict(self, _obj_dict, _ref_dict):
        for key in _obj_dict.keys():
            if key in _ref_dict.keys():
                _obj_dict[key] = _ref_dict[key]

            if (isinstance(_obj_dict[key], str) or isinstance(_obj_dict[key], unicode)) and \
                _obj_dict[key].startswith("$"):
                if _obj_dict[key][1:] in _ref_dict.keys():
                    _obj_dict[key] = _ref_dict[_obj_dict[key][1:]]

    def reflect_to_str(self, _obj_str, _ref_dict):
        if '$' not in _obj_str:
            return _obj_str

        temp_list = []
        for word in _obj_str.split():
            if word.startswith("$"):
                if word[1:] in _ref_dict.keys():
                    temp_list.append(_ref_dict[word[1:]])
                    continue

            # ' ' 로 둘러쌓인 경우, 보존을 위해서요..
            if word.startswith("'$"):
                if word[2:-1] in _ref_dict.keys():
                    temp_list.append("'" + _ref_dict[word[2:-1]] + "'")
                    continue

            temp_list.append(word)

        return ' '.join(temp_list)