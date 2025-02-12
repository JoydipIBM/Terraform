import pytest, asyncio
from unittest.mock import patch, mock_open
from code_profiler import Code_profiler


@pytest.fixture
def code_profiler():
    return Code_profiler(bucket='code-analyzer-20240627062751421300000001', file_name='text-to-sql.py')

def test_analyze_code(code_profiler, mocker):
    # Arrange
    mocker.patch('boto3.client')
    mocker.patch('boto3.resource')

    # Act
    asyncio.run(code_profiler.analyze_code())

    # Assert
    assert code_profiler.summary is not None
    assert code_profiler.documentation is not None
    assert code_profiler.bestpractices is not None
    assert code_profiler.vulnerability is not None

def test_generate_score(code_profiler, mocker):
    # Arrange
    mocker.patch('boto3.client')
    mocker.patch('boto3.resource')
    code_profiler.bestpractices = 'Best practices followed'

    # Act
    asyncio.run(code_profiler.generate_score())

    # Assert
    assert code_profiler.score is not None

def test_to_json(code_profiler):
    # Arrange
    code_profiler.summary = 'Sample summary'
    code_profiler.documentation = 'Sample documentation'
    code_profiler.bestpractices = 'Best practices followed'
    code_profiler.vulnerability = 'No vulnerabilities found'
    code_profiler.score = '90'

    # Act
    json_output = code_profiler.to_json()

    # Assert
    assert isinstance(json_output, str)
    assert '"file_name": "text-to-sql.py"' in json_output
    assert '"bucket": "code-analyzer-20240627062751421300000001"' in json_output
    assert '"summary": "Sample summary"' in json_output
    assert '"documentation": "Sample documentation"' in json_output
    assert '"bestpractices": "Best practices followed"' in json_output
    assert '"vulnerability": "No vulnerabilities found"' in json_output
    assert '"score": "90"' in json_output
