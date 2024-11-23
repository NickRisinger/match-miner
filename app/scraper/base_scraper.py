from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import HEADLESS_MODE


class BaseScraper:
    def __init__(self):
        options = Options()
        options.page_load_strategy = 'eager'
        if HEADLESS_MODE:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def close(self):
        if self.driver:
            self.driver.quit()