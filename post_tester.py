from requests import post
from sys import argv

flask_url = "http://127.0.0.1:5000"

if __name__ == "__main__":
    file_name = argv[1]
    ret = post(flask_url, files={"code": open(file_name, "rb")})
    print(ret.json()['output'])
