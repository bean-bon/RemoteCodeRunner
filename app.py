from flask import Flask, request
from flask_restful import Resource, Api

from code_runner import run_file, CommandExitCode

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
        errors = None
        if runner_result.errors is not None:
            errors = runner_result.errors.decode()
        exit_code = runner_result.exit_code.value + (" (with errors)" if errors != "" else "")
        return {"output": runner_result.output.decode() + (f"\nStacktrace:\n{errors}" if errors != "" else ""),
                "exit_code": exit_code}, 400 if exit_code != CommandExitCode.SUCCESS or errors != "" else 200


api.add_resource(CodeRunner, "/")

if __name__ == '__main__':
    app.run()
