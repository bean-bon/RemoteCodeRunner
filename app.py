from flask import Flask, request
from flask_restful import Resource, Api
from code_runner import run_file, CommandExitCode, CODE_OUTPUT_FILE

app = Flask(__name__)
api = Api(app)


class CodeRunner(Resource):

    def get(self):
        return "Send a POST request with the code file to run", 400

    def post(self):
        if len(request.files) != 1:
            return "Invalid file count", 400
        code_file = request.files[list(request.files.keys())[0]]
        return_code = run_file(code_file)
        with open(CODE_OUTPUT_FILE, "r") as f:
            contents = f.read()
            if return_code != CommandExitCode.SUCCESS:
                return contents, 400
            else:
                return contents, 200


api.add_resource(CodeRunner, "/")

if __name__ == '__main__':
    app.run()
