import os

# Настройки для Selenium
DRIVER_PATH = os.path.join(os.getcwd(), "drivers", "chromedriver")
HEADLESS_MODE = False

# Таймауты
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# Логирование
LOG_FILE = os.path.join("out", "logs")
