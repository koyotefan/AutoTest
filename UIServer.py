# encoding=utf-8

import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.common.Misc import get_executor_log_dir, get_group_name_list
from src.executor.SnrExecutor import SnrExecutor
from src.common.PrivateLog import Log

# curl http://localhost:9090 -d "group=그룹 명" -X PUT -v
# curl http://localhost:9090 -d "group=가입자_전체.grp" -X PUT -v
# curl http://localhost:9090 -X DELETE -v
# curl http://localhost:9090/list

log_inst = Log('DEB',
                os.path.join(get_executor_log_dir(), 'TempSnrExecutor.log'), True)
log = log_inst.get()


app = Flask(__name__)
api = Api(app)

put_parser = reqparse.RequestParser()
#put_parser.add_argument('group', location='args')
put_parser.add_argument('group', location='form')

'''
marshal_with 버전
resource_put_fields = {
    'group' : fields.String
}
'''

class GroupList(Resource):
    '''
    Group List 에 대한 응답을 합니다.
    '''
    def get(self):

        try:
            names = get_group_name_list()
        except Exception as e:
            # abort(500, 'exception {} {}'.format(e, e.args))
            return 'exception {} {}'.format(e, e.args), 500
        return names


class Executor(Resource):
    def get(self):

        # 현재 작업 중인 현황으로 보여주면 좋아요..
        # 총 몇개의 대상 시나리오 중에서, 몇 개를 했고, 몇 개가 망했고.. 등등.
        return 'Executor-get'

    def put(self):
        # marshal_with 버전
        #@marshal_with(resource_put_fields, envelope='resource')
        args = put_parser.parse_args()

        print args
        self.thr = SnrExecutor(log)

        try:
            print args['group'].encode('utf-8').split()
            # print args['group'].decode('utf-8').split()
            self.thr.init(args['group'].split())
            self.thr.start()
        except Exception as e:
            # abort(500, 'exception {} {}'.format(e, e.args))
            return 'exception {} {}'.format(e, e.args), 500

        return 'Executor-put %s' % args['group'], 200

    def delete(self):

        # 현재 작업 중인 쓰레드를 죽입니다.
        # 만약 죽일께 없으면, 404 를 보내냐요?
        # 죽인게 있다면, 201 을 보내구요?

        try:
            self.thr.stop()
            self.thr.wait_terminated()
            self.thr = None
        except Exception as e:
            return 'Executor is not found', 404
            # abort(404, 'thread is not found')

        return 'Executor-delete'


api.add_resource(GroupList, '/list')
api.add_resource(Executor, '/')

if __name__ == '__main__':
    app.run(host='', port=9090, debug=False)
