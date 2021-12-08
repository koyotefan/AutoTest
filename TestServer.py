# encoding=utf-8

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return { todo_id: todos[todo_id] }

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

class Todo3(Resource):
    def get(self, todo_id):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag', 'some-opaque-string'}



api.add_resource(HelloWorld, '/', '/hello')
api.add_resource(TodoSimple, '/<string:todo_id>')
api.add_resource(Todo3, '/todo/<int:todo_id>', endpoint='todo_ep')

if __name__ == '__main__':
    app.run(debug=True)

# client Test
# curl http://localhost:5000/todo2 -d "data=Change brakepads" -X PUT
# curl http://localhost:5000/todo2

'''
>>> from requests import put, get
>>> put('http://localhost:5000/todo1', data={'data': 'Remember the milk'}).json()
{u'todo1': u'Remember the milk'}
>>> get('http://localhost:5000/todo1').json()
{u'todo1': u'Remember the milk'}
>>> put('http://localhost:5000/todo2', data={'data': 'Change my brakepads'}).json()
{u'todo2': u'Change my brakepads'}
>>> get('http://localhost:5000/todo2').json()
{u'todo2': u'Change my brakepads'}
'''
