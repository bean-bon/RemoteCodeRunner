from dataclasses import dataclass
from enum import Enum


class CommandExitCode(Enum):
    SUCCESS = "Code run successfully"
    UNKNOWN_ERROR = "An unknown error occurred"
    UNSUPPORTED_LANGUAGE = "The input file format does not have a supported language runner"
    TIMEOUT = "The runtime has exceeded the allowed maximum"
    STDOUT_FILE_LIMIT = "The maximum size for the stdout file is exceeded"


@dataclass
class CodeRunnerResult:
    exit_code: CommandExitCode
    output: str
    errors: str


@dataclass
class GeneratedFile:
    filename: str
    extension: str