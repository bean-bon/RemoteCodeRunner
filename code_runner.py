import os
import time
from enum import Enum

from werkzeug.datastructures import FileStorage


class CommandExitCode(Enum):
    SUCCESS = "Code run successfully."
    UNKNOWN_ERROR = "An unknown error occurred."
    UNSUPPORTED_LANGUAGE = "The input file format does not have a supported language runner."
    TIMEOUT = "The runtime has exceeded the allowed maximum."
    STDOUT_FILE_LIMIT = "The maximum size for the stdout file is exceeded."


CODE_OUTPUT_FILE = "run_result"


def run_code_command(base: str, timeout: float = 2.0) -> CommandExitCode:
    try:
        start = time.time()
        os.system(f"timeout {timeout}s {base} -k | head -c 1M > {CODE_OUTPUT_FILE}")
        elapsed = time.time() - start
        if elapsed > timeout:
            return CommandExitCode.TIMEOUT
        else:
            return CommandExitCode.SUCCESS
    except BrokenPipeError:
        return CommandExitCode.STDOUT_FILE_LIMIT
    except Exception:
        return CommandExitCode.UNKNOWN_ERROR


def run_file(file: FileStorage) -> CommandExitCode:
    file_name_split = file.filename.split(".")
    match match_extension_to_language(file_name_split[-1]):
        case "python": return run_code_command(f"python3 {file.filename}")
        case "scala": return run_code_command(f"scala {file.filename}")
        case "java":
            base_name = file.filename.replace(f".{file_name_split[-1]}", "")
            return_code = run_code_command(f"javac {file.filename} && java {base_name}")
            os.remove(f"{base_name}.class")
            return return_code
        case _:
            return CommandExitCode.UNSUPPORTED_LANGUAGE


def match_extension_to_language(ext: str) -> str:
    match ext:
        case "py": return "python"
        case "java": return "java"
        case "sc": return "scala"
        case _: return ""
