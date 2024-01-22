from flask import Flask, request
from flask_restful import Resource, Api
from code_exec_communication import run_code


app = Flask(__name__)
api = Api(app)


class CodeRunner(Resource):

    def get(self):
        return "Send a POST request with the code file to run", 400

    def post(self):
        code = request.form['code']
        lang = request.form['lang']
        name = "Solution" if 'name' not in request.form.keys() else request.form['name']
        if code is None or lang is None:
            return "Missing required form fields.", 400
        return run_code(code, lang, name)


api.add_resource(CodeRunner, "/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
