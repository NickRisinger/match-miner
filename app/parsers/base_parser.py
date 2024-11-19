from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from logger import logger

class BaseParser:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def find(self, by: str, value: str) -> WebElement | None:
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            logger.error(f"Элемент не найден: {by} - {value}")
            return None

    def find_all(self, by: str = By.ID, value: str | None = None) -> list[WebElement]:
        try:
            return self.driver.find_elements(by, value)
        except NoSuchElementException:
            return []

    def get_text(self, by, sel):
        element = self.find(by, sel)

        if not element:
            return "-"

        return element.text.strip()

    def get_link(self, by, sel):
        element = self.find(by, sel)

        if not element:
            return "-"

        return element.get_attribute("href").strip()