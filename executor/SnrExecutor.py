# encoding=utf-8

import sys
import time
import threading
import json

from src.common.Misc import get_snr_name_list, gen_seq, pretty_json
from src.common.PrivateLog import Log
from src.common.SnrFileReader import SnrFileReader
from src.common.HistoryWriter import HistoryWriter
from src.executor.SnrAgentClient import SnrAgentClient
from src.executor.SnrConstant import SnrConstant
from src.primitive.Primitive import Primitive

class SnrExecutor(threading.Thread):
    def __init__(self, log):
        threading.Thread.__init__(self)

        self.runf = True
        self.terminatef = False
        self.snr_group_list = []

        self.log_inst = None
        self.L = log

        self.reader = None

        self.constant = None
        self.client = None

        self.history = None

    def init(self, _snr_group_list):
        self.snr_group_list = _snr_group_list

        self.reader = SnrFileReader(self.L)
        self.client = SnrAgentClient(self.L)
        self.constant = SnrConstant(self.L)

        self.history = HistoryWriter()

        self.L.info('SnrExecutor init success')
        return True

    def clear(self):
        self.stop()
        # publishing session 정리 필요..

    def stop(self):
        self.runf = False
        self.L.info('called stop')

    def is_running(self):
        return not self.terminatef

    def wait_terminated(self):
        while True:
            if not self.is_running():
                break

            time.sleep(0.2)

    def run(self):
        self.L.info('[STARTED] SnrExecutor')
        if not self.history.start():
            self.L.warning("[STARTED] History can't start")
            self.clear()
            self.L.info('[{:10}] SnrExecutor'.format('TERMINATED'))
            self.terminatef = True
            return

        for group_name in self.snr_group_list:
            self.L.info('[{:10}] {}'.format('GROUP', group_name))

            if not self.runf:
                self.L.info('[{:10}] run flag is False'.format('SCENARIO'))
                break

            snrs = get_snr_name_list(group_name)

            self.history.start_group(group_name, len(snrs))
            for snr in snrs:
                self.L.info('[{:10}] {}'.format('SCENARIO', snr))

                if not self.runf:
                    self.L.info('[{:10}] run flag is False'.format('SCENARIO'))
                    break

                ret_f = self.wrapper_execute(snr)

                if not ret_f:
                    self.L.warning('[{:10}] {} is NOK'.format('SCENARIO', snr))
                    continue
            self.history.end_group()

        self.history.stop()
        self.clear()
        self.L.info('[{:10}] SnrExecutor'.format('TERMINATED'))
        self.terminatef = True

    def wrapper_execute(self, _snr_name):
        # task_id_dict = self._gen_task_id(_snr_name)
        task_id = _snr_name + '_' + gen_seq()

        self.constant.push_var()
        self.constant.set_var({"TASK_ID": task_id})

        self.history.start_snr(_snr_name, task_id, self.constant.get_var_depth())
        ret_f = self.execute(_snr_name)
        self.history.end_snr(_snr_name, ret_f, self.constant.get_var_depth())

        self.constant.pop_var()

        return ret_f


    def execute(self, _snr_name):
        self.L.info('[{:10}] {} - START'.format('SCENARIO', _snr_name))
        self.reader.read(_snr_name)

        for i in range(self.reader.count()):
            step = self.reader.get(i)

            self.L.debug("\t[{:10}] READ \n\t{}".format('STEP', pretty_json(step)))
            self.history.detail('STEP', pretty_json(step))

            if 'SCENARIO' in step.keys():
                return self.wrapper_execute(step['SCENARIO'])

            if not 'PRIMITIVE' in step.keys():
                self.L.warning("\t[{:10}] - there's not 'PRIMITIVE' tag".format('STEP'))
                self.history.end_step('', False)
                return False

            if step['PRIMITIVE'] == 'LOCAL-VAR-SET':
                self.constant.set_var(step)
                self.history.end_step('LOCAL-VAR-SET', True)
                continue
            else:
                self.constant.set_primitive_var(step)

            primitive = Primitive(step["PRIMITIVE"])

            if not primitive.make_request_data(self.constant):
                self.L.warning("\t[{:10}] - that's because it doesn't know mandatory variable".format('STEP'))
                self.history.end_step(step["PRIMITIVE"], False)
                return False

            if step['PRIMITIVE'] == 'SLEEP':
                primitive.do()
                self.history.end_step('SLEEP', True)
                continue

            self.L.debug("\t[{:10}] REQUEST  - {}".format('STEP', step["PRIMITIVE"]))
            self.L.debug("\t[{:10}]\n{}".format('STEP', pretty_json(primitive.request())))
            self.history.detail('REQUEST', pretty_json(primitive.request()))

            (result, response) = self.client.request(primitive.uri(), primitive.request())

            self.L.debug("\t[{:10}] RESPONSE - {}".format('STEP', step["PRIMITIVE"]))
            self.L.debug("\t[{:10}]\n{}".format('STEP', pretty_json(response)))
            self.history.detail('RESPONSE', pretty_json(response))

            if not result:
                self.history.end_step(step['PRIMITIVE'], False)
                return result

            self.history.end_step(step['PRIMITIVE'], True)

        return True

if __name__ == '__main__':

    log_inst = Log('DEB', 'TempSnrExecutor.log', True)
    log = log_inst.get()

    se = SnrExecutor(log)

    #if not se.init(['가입자_전체.grp']):
    if not se.init(['테스트.grp']):
        print 'ERR| init fail'
        sys.exit()

    se.start()
    while True:
        time.sleep(1)

        if not se.is_running():
            break

    print 'Terminated'
    se.clear()
