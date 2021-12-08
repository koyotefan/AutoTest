# encoding=utf-8

import time
from src.common.TargetAgent import TargetAgent

'''
{
    "TIME" : ""
}
'''

class  Sleep(TargetAgent):
    '''
    SLEEP 을 만나면, Config 를 적용하여 쉬면 됩니다.
    '''

    def __init__(self):
        TargetAgent.__init__(self)

        self.param_dict = {}

    def __str__(self):
        return 'Sleep'

    def make_request_data(self, _constant):
        l_dict = _constant.get_var()

        try:
            self.param_dict["SLEEP_TIME"] = l_dict["SLEEP_TIME"]
        except KeyError:
            self.param_dict["SLEEP_TIME"] = "0.3"

        return self._verify(_constant)

    def _verify(self, _constant):

        if not self.param_dict:
            return False

        for val in self.param_dict.values():
            if val.startswith('$'):
                return False

        return True

    def request(self):
        return {}

    def uri(self):
        return {}

    def do(self):
        time.sleep(float(self.param_dict["SLEEP_TIME"]))
