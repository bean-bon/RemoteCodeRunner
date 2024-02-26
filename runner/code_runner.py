import os
from subprocess import Popen, PIPE, TimeoutExpired

from shared_types import CodeRunnerResult, CommandExitCode


# This method is to be moved into a container.
# cwd refers to the current working directory.
def run_code_command(cwd: str, cmd: str, timeout: float = 10) -> CodeRunnerResult:
    try:
        # As this runs untrusted commands, ensure it is done so from a container or VM.
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True, cwd=cwd)
        out, errs = proc.communicate(timeout=timeout)
        return CodeRunnerResult(CommandExitCode.SUCCESS, out, errs)
    except BrokenPipeError:
        return CodeRunnerResult(CommandExitCode.STDOUT_FILE_LIMIT, "", "")
    except TimeoutExpired:
        return CodeRunnerResult(CommandExitCode.TIMEOUT, "", "")
    except Exception:
        return CodeRunnerResult(CommandExitCode.UNKNOWN_ERROR, f"CWD: {cwd}\nCMD: {cmd}", "")


def compile_run_command(cwd: str, cmd: str, binary_file_name: str) -> CodeRunnerResult:
    code_exc_result = run_code_command(cwd, cmd)
    if os.path.exists(binary_file_name):
        os.remove(binary_file_name)
    return code_exc_result


# Runs the code file at the specified path.
# Path should hold the file path without the file extension.
def run_code_file(parent_directory: str, filename: str, extension: str) -> CodeRunnerResult:
    full_name = f"{filename}.{extension}"
    match extension:
        case "py": result = run_code_command(parent_directory,
                                             f"python {full_name}")
        case "sc": result = run_code_command(parent_directory,
                                             f"scala {full_name}")
        case "java": result = compile_run_command(cwd=parent_directory,
                                                  cmd=f"javac {full_name} && java {filename}",
                                                  binary_file_name=f"{filename}.class")
        case "cpp": result = compile_run_command(cwd=parent_directory,
                                                 cmd=f"g++ {full_name} -o exc && ./exc",
                                                 binary_file_name=f"exc")
        case "c": result = compile_run_command(parent_directory,
                                               f"gcc {full_name} -o exc && ./exc",
                                               "executable")
        case _: result = CodeRunnerResult(CommandExitCode.UNSUPPORTED_LANGUAGE, "", "")
    return result
