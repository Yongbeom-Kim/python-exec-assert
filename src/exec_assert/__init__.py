from __future__ import annotations
from subprocess import Popen, PIPE
from traceback import TracebackException
from types import TracebackType
from typing import Optional

import asyncio


class Command:
    def __init__(self, command: str) -> None:
        self.command = command

    async def __aenter__(self) -> Command:
        self.subprocess = await asyncio.create_subprocess_shell(self.command, stdout=PIPE, stderr=PIPE)
        return self
        
    async def __aexit__(self, exc_type: Exception, exc_value: TracebackException, exc_tb: TracebackType) -> None:
        await self.subprocess.wait()
        print(exc_type, exc_value, exc_tb)
        return
    
    async def wait(self) -> None:
        process = self.subprocess.wait()


    async def read_stdout(self) -> str:
        stdout = self.subprocess.stdout
        if stdout is None:
            return ""
        return (await stdout.read()).decode('utf-8')

    async def read_stderr(self) -> str:
        stderr = self.subprocess.stderr
        if stderr is None:
            return ""
        return (await stderr.read()).decode('utf-8')