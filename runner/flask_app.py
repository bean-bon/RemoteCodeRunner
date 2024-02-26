from os import environ
from flask import Flask, request
from flask_restful import Resource, Api
from code_runner import run_code_file
from shared_types import CommandExitCode

app = Flask(__name__)
api = Api(app)


class Runner(Resource):

    def post(self):
        VOLUME_FILE_PATH = environ["VOLUME_FILE_PATH"]
        filename = request.form['filename']
        extension = request.form['extension']
        runner_result = run_code_file(VOLUME_FILE_PATH, filename, extension)
        errors = None
        if runner_result.errors is not None:
            errors = runner_result.errors
        exit_code = runner_result.exit_code.value + (" (with errors)" if errors != "" else "")
        return {"output": runner_result.output + (f"\nStacktrace:{errors}" if errors != "" else ""),
                "exit_code": exit_code}, 400 if exit_code != CommandExitCode.SUCCESS else 200


api.add_resource(Runner, "/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)