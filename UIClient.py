# encoding=utf-8
import os
import sys
#import json
#from collections import OrderedDict

from Common import Misc

class UIClient(object):
    '''
    임시로 만들었습니다. 향후에는 WEB 또는 CLI 로 변경해야 합니다.
    '''
    def __init__(self):
        self.cmd = ''
        self.groupName = ''
        self.cmdSession = Misc.Session()
        self.monitorSession = Misc.Session()

    def Init(self, _argv):
        if len(_argv) > 1:
            self.groupName = _argv[1]
        self.cmd = _argv[0]

        self.readConfig()

    def readConfig(self):
        cfgDir = os.path.join(os.environ['AUTOV_BASE_DIR'], self.__class__.__name__)
        d = Misc.ReadJsonFile(cfgDir, self.__class__.__name__ + '.conf')

        self.cmdSession.SetPort(d['cmd-port'])
        self.monitorSession.SetPort(d['monitor-port'])

    def Do(self):
        if self.groupName:
            self.sendCmd(self.cmd, self.groupName)
        else:
            self.startMonitor()

        return True

    def sendCmd(self, _cmd, _groupName):
        if not self.cmdSession.Connect():
            print "can't connect to SnrExecute for command"
            return

        if not self.cmdSession.Send('{0} {1}\n'.format(_cmd, _groupName)):
            print "can't send to SnrExecute [{0}:{1}]".format(_cmd, _groupName)
        else:
            print "sent to SnrExecute [{0}:{1}]".format(_cmd, _groupName)


    def startMonitor(self):
        if not self.monitorSession.Connect():
            print "can't connect to SnrExecute for command"
            return

        while True:
            try:
                print self.monitorSession.Recv()
            except:
                break

    def Clear(self):
        if self.cmdSession:
            self.cmdSession.Clear()

        if self.monitorSession:
            self.monitorSession.Clear()

if __name__ == '__main__':

    if len(sys.argv) !=3 and len(sys.argv) != 2:
        print 'invalid argument'
        print '    ex) python UIClient.py start|stop [snr group name]'
        print '    ex) python UIClient.py monitor'
        sys.exit()

    uc = UIClient()

    if uc.Init(sys.argv[1:]):
        uc.Do()

    uc.Clear()