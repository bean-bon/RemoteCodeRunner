import os

from flask import Flask, request
from flask_restful import Resource, Api
from code_runner import run_file, CodeRunnerResult, CommandExitCode, CODE_OUTPUT_FILE

app = Flask(__name__)
api = Api(app)


class CodeRunner(Resource):

    def get(self):
        return "Send a POST request with the code file to run", 400

    def post(self):
        if len(request.files) != 1:
            return "Invalid file count", 400
        code_file = request.files[list(request.files.keys())[0]]
        runner_result = run_file(code_file)
        exit_code = runner_result.exit_code
        if exit_code != CommandExitCode.SUCCESS or runner_result.stderr != "":
            return f"""Code output:\n{runner_result.stdout}\n\n"
                    Errors:\n{runner_result.stderr}\n 
                    {exit_code.value if exit_code != CommandExitCode.SUCCESS else ''}""", 400
        else:
            return runner_result.stdout, 200


api.add_resource(CodeRunner, "/")

if __name__ == '__main__':
    app.run()
