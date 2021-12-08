# encoding=utf-8

import os
import sys
import json
from collections import OrderedDict

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from src.common.PrivateLog import Log
from src.primitive.Primitive import Primitive
from src.common.Misc import get_agent_log_dir

log_inst = Log('DEB',
                os.path.join(get_agent_log_dir(), 'TempSnrAgent.log'), True)
log = log_inst.get()

app = Flask(__name__)
api = Api(app)

class Agent(Resource):
    def post(self, primitive_name):
        i_dict = request.get_json(force=True)
        log.info('[{:10}] INPUT --------------'.format(primitive_name) )
        log.info(i_dict)

        p_inst = self._create(primitive_name)
        r_dict = p_inst.do(json.loads(i_dict, object_pairs_hook=OrderedDict))

        log.info('[{:10}] OUTPUT -------------'.format(primitive_name) )
        log.info(r_dict)

        return r_dict, 200


    def _create(self, _primitive_name):
        c_name = 'src.primitive.' + _primitive_name

        components = c_name.split('.')

        mod = __import__(c_name, fromlist=_primitive_name)
        obj = getattr(mod, components[-1])()

        return obj


api.add_resource(Agent, '/<primitive_name>')

if __name__ == '__main__':

    import signal
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    app.run(host='', port=9091, debug=False)