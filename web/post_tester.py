from requests import post
from sys import argv

flask_url = "http://0.0.0.0:8080"

if __name__ == "__main__":
    lang = argv[1]
    file_name = argv[2]
    with open(file_name, "rb") as f:
        ret = post(flask_url, data={"code": f.read(), "lang": lang})
    print(ret.json())
