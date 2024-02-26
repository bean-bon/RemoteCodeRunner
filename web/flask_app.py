from flask import Flask, request
from flask_restful import Resource, Api
from code_exec_communication import run_code


app = Flask(__name__)
api = Api(app)


class CodeRunner(Resource):

    def get(self):
        return "Send a POST request with the code file to run", 400

    def post(self):
        form_dict = request.form.to_dict()
        code = form_dict['code']
        lang = form_dict['lang']
        name = "Solution" if 'name' not in form_dict.keys() else form_dict['name']
        if code is None or lang is None:
            return "Missing required form fields.", 400
        return run_code(code, lang, name)


api.add_resource(CodeRunner, "/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
