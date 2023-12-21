from typing import Any

from flask import Flask, request
from flask_restful import Resource, Api

from code_runner import CommandExitCode, run_code

app = Flask(__name__)
api = Api(app)


class CodeRunner(Resource):

    def get(self):
        return "Send a POST request with the code file to run", 400

    def post(self):
        code = request.form['code']
        lang = request.form['lang']
        if code is None or lang is None:
            return "Missing form fields 'code' or 'lang'.", 400
        runner_result = run_code(code, lang)
        errors = None
        if runner_result.errors is not None:
            errors = runner_result.errors.decode()
        exit_code = runner_result.exit_code.value + (" (with errors)" if errors != "" else "")
        return {"output": runner_result.output.decode() + (f"\nStacktrace:\n{errors}" if errors != "" else ""),
                "exit_code": exit_code}, 400 if exit_code != CommandExitCode.SUCCESS or errors != "" else 200


api.add_resource(CodeRunner, "/")

if __name__ == '__main__':
    app.run()
