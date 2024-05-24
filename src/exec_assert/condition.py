from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable

class Condition(ABC):
    """A condition for the execution of a command."""
    @abstractmethod
    def description(self) -> str:
        """A description of the condition."""
        pass
    pass

class RuntimeCondition(Condition):
    """A condition that can be checked during the execution of a command."""
    pass

class RuntimeLogCondition(RuntimeCondition):
    """A condition that checks a log line for a specific string."""

    __create_key = object()

    def __init__(self, fn: Callable[[str], bool], description: str, create_key: object) -> None:
        assert(create_key == RuntimeLogCondition.__create_key), \
            "LogCondition objects must be created using its class methods"
        self.check_fn = fn
        self._description = description

    def check(self, log_line: str) -> bool:
        return self.check_fn(log_line)
    
    def description(self) -> str:
        return self._description
    
    @classmethod
    def LambdaCondition(cls, fn: Callable[[str], bool], description: str = "") -> RuntimeLogCondition:
        """Create a condition using a lambda function."""
        return RuntimeLogCondition(fn, description, RuntimeLogCondition.__create_key)

    @classmethod
    def HasSubstring(cls, log_line: str, description: str = "") -> RuntimeLogCondition:
        """Create a condition that checks for a specific string in the log."""
        assert(len(log_line.splitlines()) == 1), \
            "LogCondition.HasLine only accepts a single line"
        return RuntimeLogCondition.LambdaCondition(lambda line: log_line in line, description)
    
    @classmethod
    def HasLine(cls, log_line: str, description: str = "") -> RuntimeLogCondition:
        """Create a condition that checks for an exact line in the log."""
        return RuntimeLogCondition.LambdaCondition(lambda line: line == log_line, description)