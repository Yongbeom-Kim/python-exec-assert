import asyncio
import pytest

pytest_plugins = ('pytest_asyncio',)

from src.exec_assert import Command

@pytest.mark.asyncio
async def test_simple_commmand() -> None:
    async with Command("echo 'Hello, World!'") as cmd:
        await cmd.wait()
        assert await cmd.read_stdout() == "Hello, World!\n"
        assert await cmd.read_stderr() == ""