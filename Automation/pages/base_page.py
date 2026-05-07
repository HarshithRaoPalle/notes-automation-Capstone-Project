
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)

from config.environment import config
from utils.logger import get_logger
import time

logger = get_logger()


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            config.timeout,
            poll_frequency=1,
            ignored_exceptions=[
                StaleElementReferenceException
            ]
        )

    def open_url(self, url):

        logger.info(f"Opening URL: {url}")

        self.driver.get(url)

        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=40):

        WebDriverWait(
            self.driver,
            timeout
        ).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    def retry_action(
        self,
        action,
        retries=4,
        delay=2
    ):

        last_exception = None

        for attempt in range(retries):

            try:

                return action()

            except Exception as e:

                last_exception = e

                logger.warning(
                    f"Retry attempt "
                    f"{attempt + 1}/{retries}"
                )

                time.sleep(delay)

        raise last_exception

    def click(self, locator):

        def action():

            logger.info(
                f"Clicking element: {locator}"
            )

            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView("
                "{block: 'center'});",
                element
            )

            try:
                element.click()

            except (
                ElementClickInterceptedException,
                ElementNotInteractableException
            ):

                logger.warning(
                    "Normal click failed. "
                    "Trying JS click."
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

        return self.retry_action(action)

    def send_keys(self, locator, text):

        def action():

            logger.info(
                f"Entering text into {locator}"
            )

            element = self.wait.until(
                EC.visibility_of_element_located(
                    locator
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView("
                "{block: 'center'});",
                element
            )

            element.clear()

            element.send_keys(text)

        return self.retry_action(action)

    def get_text(self, locator):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        return element.text.strip()

    def is_visible(self, locator):

        try:

            self.wait.until(
                EC.visibility_of_element_located(
                    locator
                )
            )

            return True

        except TimeoutException:

            return False

    def wait_for_visibility(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(
                locator
            )
        )

    def wait_for_clickable(self, locator):

        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator):

        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def safe_click(self, locator):

        return self.click(locator)

    def safe_send_keys(
        self,
        locator,
        text
    ):

        return self.send_keys(
            locator,
            text
        )
