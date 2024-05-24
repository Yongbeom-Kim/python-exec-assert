from __future__ import annotations
from subprocess import Popen, PIPE, STDOUT
from typing import List

from .condition import Condition, RuntimeCondition, RuntimeLogCondition


class WaitingCommand():
    def __init__(self, command: str) -> None:
        self.command = command
        self.runtime_conditions: List[RuntimeCondition] = []
        self.passed_assertions: List[bool] = []

    def check_for(self, condition: Condition) -> WaitingCommand:
        if isinstance(condition, RuntimeCondition):
            self.runtime_conditions.append(condition)
        else:
            raise NotImplementedError(
                f"Condition {condition} is not supported")
        return self

    def exec(self) -> CompletedCommand:
        # There is no good way to stream both stdout and stderr in Python, so this will do for now.
        self.passed_assertions = [False] * len(self.runtime_conditions)
        self.process = Popen(self.command, shell=True,
                             stdout=PIPE, stderr=STDOUT)
        stdout = self.process.stdout
        if stdout is None:
            raise RuntimeError("Failed to open stdout")

        for line_b in iter(stdout.readline, b''):
            line_str = line_b.decode('utf-8').strip()
            self._check_log_line(line_str)

        return CompletedCommand(self)

    def _check_log_line(self, line: str) -> None:
        for i, condition in enumerate(self.runtime_conditions):
            if isinstance(condition, RuntimeLogCondition):
                if condition.check(line):
                    self.passed_assertions[i] = True


Command = WaitingCommand


class CompletedCommand():
    def __init__(self, command: Command) -> None:
        self.command = command.command
        self.failed_assertions = [
            assertion for assertion, passing
            in zip(command.runtime_conditions, command.passed_assertions)
            if not passing
        ]

    def passes(self) -> bool:
        return len(self.failed_assertions) == 0
