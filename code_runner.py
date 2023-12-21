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


def compile_run_command(cmd: str, binary_file_name: str) -> CodeRunnerResult:
    code_exc_result = run_code_command(cmd)
    try:
        os.remove(binary_file_name)
    except FileNotFoundError:
        pass
    return code_exc_result


def run_file(file: FileStorage) -> CodeRunnerResult:
    file_name_split = file.filename.split(".")
    base_name = file.filename.replace(f".{file_name_split[-1]}", "")
    match match_extension_to_language(file_name_split[-1]):
        case "python": return run_code_command(f"python3 {file.filename}")
        case "scala": return run_code_command(f"scala {file.filename}")
        case "java": return compile_run_command(f"javac {file.filename} && java {base_name}", f"{base_name}.class")
        case "c++": return compile_run_command(f"g++ {file.filename} && ./a.out", f"a.out")
        case "c": return compile_run_command(f"gcc {file.filename} -o executable && ./executable", "executable")
        case _: return CodeRunnerResult(CommandExitCode.UNSUPPORTED_LANGUAGE, b"", b"")


def match_extension_to_language(ext: str) -> str:
    match ext:
        case "py": return "python"
        case "java": return "java"
        case "sc": return "scala"
        case "cpp": return "c++"
        case "c": return "c"
        case _: return ""
