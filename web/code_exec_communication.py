import os
from typing import Optional
from shared_types import GeneratedFile
from requests import post

VOLUME_FILE_PATH = os.environ["VOLUME_FILE_PATH"]
__RUNNER_PATH = "http://runner:8081"


def run_code(code: str, lang: str, name: str) -> (dict[str, str], int):
    file = make_temp_code_file(code, lang, name)
    if file is None:
        return dict()
    req = post(__RUNNER_PATH, data={"filename": file.filename, "extension": file.extension})
    os.remove(f"{VOLUME_FILE_PATH}/{file.filename}.{file.extension}")
    return req.json(), req.status_code


def make_temp_code_file(code: str, lang: str, name: str) -> Optional[GeneratedFile]:
    extension = match_language_to_extension(lang)
    if extension is None:
        return None
    file_name = f"{VOLUME_FILE_PATH}/{name}.{extension}"
    with open(file_name, "w") as f:
        f.write(code)
        print(f"written code to {file_name}")
    return GeneratedFile(name, extension)


def match_language_to_extension(lang: str) -> str | None:
    match lang:
        case "python": return "py"
        case "scala": return "sc"
        case "java": return "java"
        case "c++": return "cpp"
        case "c": return "c"
        case _: return None
