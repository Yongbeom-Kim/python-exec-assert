from src.exec_assert import Command
from src.exec_assert.condition import RuntimeLogCondition

def test_simple_commmand() -> None:
    result = Command('echo "Hello, World!"') \
            .exec()

    assert result.passes()

def test_custom_condition() -> None:
    result = Command('echo "Hello, World!"') \
            .check_for(RuntimeLogCondition.LambdaCondition(lambda line: 'Hello' in line)) \
            .exec()
    
    assert result.passes()

def test_custom_condition_fail() -> None:
    result = Command('echo "Hello, World!"') \
            .check_for(RuntimeLogCondition.LambdaCondition(lambda line: 'Goodbye' in line, 'test')) \
            .exec()
    
    assert not result.passes()
    assert len(result.failed_assertions) == 1
    assert result.failed_assertions[0].description() == 'test'

def test_has_substring_command() -> None:
    result = Command('echo "Hello, World!"') \
            .check_for(RuntimeLogCondition.HasSubstring('Hello')) \
            .exec()
    
    assert result.passes()

def test_has_substring_command_fail() -> None:
    result = Command('echo "Hello, World!"') \
            .check_for(RuntimeLogCondition.HasSubstring('Goodbye', 'test')) \
            .exec()
    
    assert not result.passes()
    assert len(result.failed_assertions) == 1
    assert result.failed_assertions[0].description() == 'test'

def test_has_line_command() -> None:
    result = Command('echo "Hello, World!"') \
            .check_for(RuntimeLogCondition.HasLine('Hello, World!')) \
            .exec()
    
    assert result.passes()

def test_has_line_command_fail() -> None:
    result = Command('echo "Hello, World!"') \
            .check_for(RuntimeLogCondition.HasLine('Goodbye, World!', 'test_has_line_command_fail')) \
            .exec()
    
    assert not result.passes()
    assert len(result.failed_assertions) == 1
    assert result.failed_assertions[0].description() == 'test_has_line_command_fail'

