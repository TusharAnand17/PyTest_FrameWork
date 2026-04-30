import pytest
pytest_plugins = [
    "fixtures.driver_fixture",
    "fixtures.api_fixture",
    "fixtures.hooks"
]

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests (qa/dev/prod)"
    )

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests (chrome/firefox/edge)"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )