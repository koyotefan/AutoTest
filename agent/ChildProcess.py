# encoding=utf-8

import os
import time

class ChildProcess(object):
    def __init__(self):
        self.dir = ''
        self.exec_list = []
        self.pid_fname = ''

    def init(self, _dict):
        '''
        {
            "dir" : "/PG/AUTOV/SnrAgent/Simulator",
            "exec" : "python cds_sim.py",
            "env" : "cds_sim.env"
            "conf" : "cds_sim.conf",
            "pid" : "cds_sim.pid",
            "ret" : "cds_sim.ret"
            "allow_cmd" : ["RUN", "STOP", "SEND", "DISCONNECT", "CONNECT"]
        }
        '''
        if not _dict:
            return False

        self.dir = _dict["dir"]
        self.exec_list = _dict["exec"].split()
        self.exec_list.append(_dict["env"])
        self.exec_list.append(_dict["conf"])
        self.exec_list.append(_dict["pid"])
        self.exec_list.append(_dict["ret"])
        self.pid_fname = os.path.join(_dict["dir"], _dict["pid"])

        return True

    def run(self):
        pid_str = self._is_run()

        if pid_str:
            self._kill_process(pid_str)

        pid = os.fork()

        if pid == 0:
            from subprocess import call
            import sys

            '''
            # 부모로 부터 받은 listen fd 같은 걸 닫아야죠.
            import psutil
            proc = psutil.Process()
            l = proc.open_files()
            print type(l)
            print dir(l)

            for f in proc.open_files():
                if f.fd == -1:
                    continue
                print "------ {}".format(f.fd)
                os.close(f.fd)
            print "#$#$#$#$#$#$#$#$#"
            '''

            try:
                os.chdir(self.dir)
                os.execvp(self.exec_list[0], self.exec_list)
            except OSError:
                pass

            sys.exit()


        for cnt in range(10):
            if str(pid) == self._is_run():
                return True

            time.sleep(0.3)

        return False

    def _is_run(self):
        pid_str = ''

        try:
            with open(self.pid_fname, "r") as fd:
                pid_str = fd.readline()
        except IOError:
            return ''

        if not pid_str:
            return ''

        return self._check_proc(pid_str.strip())

    def _check_proc(self, _pid_str):
        try:
            line = ''
            with open(os.path.join('/proc', _pid_str, 'cmdline'), 'r') as fd:
                line = fd.readline()

                for _args in self.exec_list:
                    if _args == 'python':
                        continue

                    if _args in line:
                        return _pid_str
        except IOError:
            pass

        return ''

    def _kill_process(self, _pid_str):
        import signal

        for cnt in range(100):
            try:
                os.kill(int(_pid_str), signal.SIGTERM)
                time.sleep(0.1)
                os.kill(int(_pid_str), 0)
            except OSError:
                return True
        try:
            os.kill(int(_pid_str), signal.SIGKILL)
            time.sleep(0.3)
        except OSError:
            pass

        return True

    def stop(self):
        pid_str = self._is_run()

        if pid_str:
            return self._kill_process(pid_str)

        return True
