import os
import subprocess
import time
from dataclasses import dataclass
from subprocess import Popen, PIPE
from enum import Enum

from werkzeug.datastructures import FileStorage


class CommandExitCode(Enum):
    SUCCESS = "Code run successfully"
    UNKNOWN_ERROR = "An unknown error occurred"
    UNSUPPORTED_LANGUAGE = "The input file format does not have a supported language runner"
    TIMEOUT = "The runtime has exceeded the allowed maximum"
    STDOUT_FILE_LIMIT = "The maximum size for the stdout file is exceeded"


@dataclass
class CodeRunnerResult:
    exit_code: CommandExitCode
    output: bytes
    errors: bytes


CODE_OUTPUT_FILE = "run_result"
ERROR_OUTPUT_FILE = "run_errors"


def run_code_command(base: str, timeout: float = 2.0) -> CodeRunnerResult:
    try:
        start = time.time()
        cmd = f"timeout {timeout}s {base} -k"
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, errs = proc.communicate()
        elapsed = time.time() - start
        if elapsed > timeout:
            return CodeRunnerResult(CommandExitCode.TIMEOUT, out, errs)
        else:
            return CodeRunnerResult(CommandExitCode.SUCCESS, out, errs)
    except BrokenPipeError:
        return CodeRunnerResult(CommandExitCode.STDOUT_FILE_LIMIT, b"", b"")
    except Exception:
        return CodeRunnerResult(CommandExitCode.UNKNOWN_ERROR, b"", b"")


def run_file(file: FileStorage) -> CodeRunnerResult:
    file_name_split = file.filename.split(".")
    match match_extension_to_language(file_name_split[-1]):
        case "python": return run_code_command(f"python3 {file.filename}")
        case "scala": return run_code_command(f"scala {file.filename}")
        case "java":
            base_name = file.filename.replace(f".{file_name_split[-1]}", "")
            return_code = run_code_command(f"javac {file.filename} && java {base_name}")
            try:
                os.remove(f"{base_name}.class")
            except FileNotFoundError:
                pass
            return return_code
        case _:
            return CodeRunnerResult(CommandExitCode.UNSUPPORTED_LANGUAGE, "", "")


def match_extension_to_language(ext: str) -> str:
    match ext:
        case "py": return "python"
        case "java": return "java"
        case "sc": return "scala"
        case _: return ""
