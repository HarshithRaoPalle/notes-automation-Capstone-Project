import json
import os
import platform
from pathlib import Path

import allure
import pytest

from config.environment import config as app_config
from fixtures.browser_fixture import get_driver

from utils.helpers import take_screenshot


ALLURE_RESULTS_DIR = Path("reports/allure-results")


def _write_allure_environment(allure_dir):

    allure_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    environment = {
        "Base URL": app_config.base_url,
        "API URL": app_config.api_url,
        "Browser": app_config.browser,
        "Execution": app_config.execution,
        "Grid URL": app_config.grid_url if app_config.execution.lower() == "remote" else "N/A",
        "Python": platform.python_version(),
        "OS": platform.platform(),
    }

    env_lines = [
        f"{key}={value}"
        for key, value in environment.items()
    ]

    (allure_dir / "environment.properties").write_text(
        "\n".join(env_lines),
        encoding="utf-8"
    )

    executor = {
        "name": "pytest",
        "type": "local",
        "buildName": os.getenv("BUILD_NAME", "local-run"),
        "reportName": "Notes Automation Allure Report",
    }

    (allure_dir / "executor.json").write_text(
        json.dumps(executor, indent=2),
        encoding="utf-8"
    )


def pytest_configure(config):

    allure_dir = config.getoption(
        "--alluredir",
        default=None
    )

    _write_allure_environment(
        Path(allure_dir) if allure_dir else ALLURE_RESULTS_DIR
    )


@pytest.fixture(scope="function")
def driver():

    driver = get_driver()

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)

def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            screenshot_path = take_screenshot(
                driver,
                item.name
            )

            allure.attach.file(
                screenshot_path,
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )
