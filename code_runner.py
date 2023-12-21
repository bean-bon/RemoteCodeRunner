import os
import time
from dataclasses import dataclass
from subprocess import Popen, PIPE
from enum import Enum
from typing import Optional


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


@dataclass
class GeneratedFile:
    filename: str
    extension: str


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


def run_code(code: str, lang: str) -> CodeRunnerResult:
    cf = make_temp_code_file(code, lang)
    if cf is None:
        return CodeRunnerResult(CommandExitCode.UNSUPPORTED_LANGUAGE, b"", b"")
    full_name = f"{cf.filename}.{cf.extension}"
    match cf.extension:
        case "py": result = run_code_command(f"python3 {full_name}")
        case "sc": result = run_code_command(f"scala {full_name}")
        case "java": result = compile_run_command(f"javac {full_name} && java {cf.filename}", f"{cf.filename}.class")
        case "cpp": result = compile_run_command(f"g++ {full_name} && ./a.out", f"a.out")
        case "c": result = compile_run_command(f"gcc {full_name} -o executable && ./executable", "executable")
        case _: result = CodeRunnerResult(CommandExitCode.UNSUPPORTED_LANGUAGE, b"", b"")
    os.remove(full_name)
    return result


def make_temp_code_file(code: str, lang: str) -> Optional[GeneratedFile]:
    extension = match_language_to_extension(lang)
    if extension is None:
        return None
    file_name = f"Solution.{extension}"
    with open(file_name, "w") as f:
        f.write(code)
    return GeneratedFile("Solution", extension)


def match_language_to_extension(lang: str) -> str | None:
    match lang:
        case "python": return "py"
        case "scala": return "sc"
        case "java": return "java"
        case "c++": return "cpp"
        case "c": return "c"
        case _: return None
