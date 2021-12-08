# encoding=utf-8

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1' : {'task': 'build an API'},
    'todo2' : {'task': '????'},
    'todo3' : {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
print '1 ----------'
print parser
print dir(parser)

# parser 에 task 를 넣어 둔 것은... 앞으로 데이터가 들어올때... task 가 들어올 테니...
# POST 데이터가 오면.. task 라는 이름으로 갖겠다 ??
parser.add_argument('task')
parser.add_argument('abc')


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        print '2 ----------'
        print args

        task = {'task' : args['task']}
        TODOS[todo_id] = task
        return task, 201

class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):

        # 실제적으로 parser 를 가지고 파싱한 결과를 갖고 있습니다.
        args = parser.parse_args()

        print '3 ----------'
        print args

        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id


        TODOS[todo_id] = {'task':args['task'] }
        return TODOS[todo_id], 201

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)


# curl http://localhost:5000/todos
# curl http://localhost:5000/todos/todo3
# curl http://localhost:5000/todos/todo2 -X DELETE -v
# curl http://localhost:5000/todos -d "task=something new" -X POST -v
# curl http://localhost:5000/todos -d "task=something new" -d "abc=1234" -X POST -v
# curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v

